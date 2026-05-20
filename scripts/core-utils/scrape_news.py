import requests
from bs4 import BeautifulSoup
from supabase import create_client, Client
import os
import re
from geopy.geocoders import Nominatim
import time
from dotenv import load_dotenv

# Load .env if it exists
load_dotenv()

# Configuration
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_SERVICE_ROLE_KEY')
NEWS_URL = 'https://www.scotland.police.uk/what-s-happening/news/'

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY) if SUPABASE_URL and SUPABASE_KEY else None
geolocator = Nominatim(user_agent='scotland_precise_crime_tracker_v7')

def classify_incident(title, content):
    text = (title + " " + content).lower()
    
    # 1. Violence
    if any(k in text for k in ['assault', 'murder', 'stab', 'knife', 'weapon', 'attack', 'robbery', 'serious', 'death']):
        return 'Violence'
    
    # 2. Dishonesty
    if any(k in text for k in ['theft', 'stolen', 'housebreaking', 'burglary', 'shoplift', 'fraud', 'bank']):
        return 'Dishonesty'
    
    # 3. Society / Antisocial
    if any(k in text for k in ['drugs', 'cannabis', 'cocaine', 'antisocial', 'noise', 'disorder', 'disperse', 'alcohol']):
        return 'Society'

    # 4. Damage
    if any(k in text for k in ['fire', 'vandalism', 'damage', 'wilful']):
        return 'Damage'

    # 5. Sexual Crimes
    if any(k in text for k in ['sexual', 'indecent', 'rape', 'lewd']):
        return 'Sexual Crimes'

    return 'Total Crimes' # Default / Miscellaneous

def geocode_location(location_name, city):
    queries = [
        f"{location_name}, {city}, Scotland",
        f"{location_name}, Scotland",
        f"{city}, Scotland"
    ]

    for query in queries:
        try:
            time.sleep(1) # Respect API limits
            location = geolocator.geocode(query, timeout=10, addressdetails=True)
            if location:
                addr = location.raw.get('address', {})
                if 'Scotland' in addr.get('state', '') or 'Scotland' in addr.get('country', ''):
                    return location.latitude, location.longitude
        except Exception as e:
            print(f"  [!] Geocoding error for {query}: {e}")
    return None, None

def extract_precise_location(text):
    patterns = [
        r'(?:in the\s+)([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)(?:\s+area)',
        r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:Street|Road|Avenue|Close|Drive|Lane|Way|Crescent|Terrace|Square|Court|Grove|Hill|View|Wynd|Gardens))',
        r'(?:near\s+)([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            loc = match.group(1) if len(match.groups()) >= 1 else match.group(0)
            if loc and len(loc) > 3:
                return loc.strip()
    return None

def scrape_police_news():
    print(f"Fetching news from {NEWS_URL}...")
    try:
        response = requests.get(NEWS_URL, timeout=30)
        response.raise_for_status()
    except Exception as e:
        print(f"Failed to fetch news: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    links = []
    for a in soup.find_all('a', href=True):
        href = a['href']
        # Accept 2026 and 2025 news for better density
        if ('/news/2026/' in href or '/news/2025/' in href) and len(href.split('/')) > 5:
            if not href.startswith('http'):
                href = 'https://www.scotland.police.uk' + href
            if href not in links:
                links.append(href)

    print(f"Processing up to {len(links)} articles...")

    for link in links:
        try:
            detail_res = requests.get(link, timeout=30)
            detail_soup = BeautifulSoup(detail_res.text, 'html.parser')

            title_elem = detail_soup.find('h1', class_='news-h1') or detail_soup.find('h1') or detail_soup.find('h2')
            title = title_elem.text.strip() if title_elem else "Untitled"

            content_elem = detail_soup.select_one('.article-content') or detail_soup.select_one('article') or detail_soup.select_one('main')
            content = ""
            if content_elem:
                for s in content_elem(['script', 'style', 'nav', 'header']):
                    s.decompose()
                content = content_elem.get_text(separator=' ').strip()

            crime_category = classify_incident(title, content)

            city = "Scotland"
            known_cities = ["Glasgow", "Edinburgh", "Aberdeen", "Dundee", "Inverness", "Perth", "Stirling", "Broxburn", "Falkirk", "Paisley", "Hamilton", "Livingston", "Motherwell", "Cumbernauld", "Kirkcaldy", "Dunfermline", "Ayr", "Kilmarnock", "Dumfries", "Greenock"]
            for c in known_cities:
                if c in title or c in content[:500]:
                    city = c
                    break

            location_name = extract_precise_location(content) or extract_precise_location(title)

            lat, lon = (None, None)
            if location_name:
                lat, lon = geocode_location(location_name, city)

            data = {
                'title': title,
                'url': link,
                'summary': (content[:500] + '...').replace('\n', ' '),
                'city': city,
                'location_name': location_name,
                'crime_type': crime_category,
                'latitude': lat,
                'longitude': lon,
                'coordinates': f'POINT({lon} {lat})' if lat and lon else None
            }

            if supabase:
                supabase.table('incidents').upsert(data, on_conflict='url').execute()
                print(f"DONE: [{crime_category}] {title} ({city})")
            else:
                print(f"DRY RUN: [{crime_category}] {title}")

        except Exception as e:
            print(f"Error on {link}: {e}")

if __name__ == '__main__':
    scrape_police_news()
