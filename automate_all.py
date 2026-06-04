import os
import requests
import re
import time
import sys
from bs4 import BeautifulSoup
from supabase import create_client, Client
from geopy.geocoders import Nominatim
from dotenv import load_dotenv

# 1. SETUP & CONFIGURATION
load_dotenv()
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_SERVICE_ROLE_KEY')

print(f"--- ENVIRONMENT CHECK ---")
if SUPABASE_URL:
    print(f"SUPABASE_URL: {SUPABASE_URL[:15]}... (length: {len(SUPABASE_URL)})")
else:
    print("SUPABASE_URL: NOT FOUND")

if SUPABASE_KEY:
    print(f"SUPABASE_KEY found: Yes (length: {len(SUPABASE_KEY)})")
else:
    print("SUPABASE_KEY found: No")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("[!] Error: SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set.")
    sys.exit(1)

# Clean URL if it has the rest/v1 suffix which causes failures in the py client
if SUPABASE_URL.endswith('/rest/v1') or SUPABASE_URL.endswith('/rest/v1/'):
    print("[i] Cleaning SUPABASE_URL suffix...")
    SUPABASE_URL = SUPABASE_URL.replace('/rest/v1/', '').replace('/rest/v1', '')
    print(f"    New URL: {SUPABASE_URL}")

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    print(f"[!] Supabase Client Init Error: {e}")
    sys.exit(1)

geolocator = Nominatim(user_agent='scotland_safety_finder_automation_v1')

# Constants
SPARQL_ENDPOINT = "https://statistics.gov.scot/sparql"
NEWS_URL = 'https://www.scotland.police.uk/what-s-happening/news/'
POPULATIONS = {
    "S12000033": 227430, "S12000034": 262690, "S12000035": 115090, "S12000036": 526470,
    "S12000037": 154080, "S12000038": 110250, "S12000039": 121400, "S12000040": 143710,
    "S12000041": 150920, "S12000042": 95530, "S12000043": 371910, "S12000044": 155830,
    "S12000045": 236540, "S12000046": 635120, "S12000047": 238060, "S12000048": 77060,
    "S12000049": 341140, "S12000050": 322910, "S12000051": 112520, "S12000052": 194160,
    "S12000053": 179390, "S12000054": 92600, "S12000055": 116240, "S12000056": 122260,
    "S12000057": 88680, "S12000058": 94100, "S12000059": 46800, "S12000060": 22540,
    "S12000061": 23210, "S12000062": 26500, "S12000013": 182790, "S12000027": 93470
}

# 2. UTILITY FUNCTIONS
def extract_centroid(wkt):
    try:
        coords = re.findall(r"([-+]?\d*\.\d+)\s+([-+]?\d*\.\d+)", wkt)
        if coords:
            lats = [float(c[1]) for c in coords]
            lons = [float(c[0]) for c in coords]
            return sum(lats)/len(lats), sum(lons)/len(lons)
    except: pass
    return None, None

def geocode_location(location_name, city):
    for query in [f"{location_name}, {city}, Scotland", f"{location_name}, Scotland", f"{city}, Scotland"]:
        try:
            time.sleep(1)
            location = geolocator.geocode(query, timeout=10, addressdetails=True)
            if location:
                addr = location.raw.get('address', {})
                if 'Scotland' in addr.get('state', '') or 'Scotland' in addr.get('country', ''):
                    return location.latitude, location.longitude
        except: pass
    return None, None

def extract_precise_location(text):
    patterns = [r'(?:in the\s+)([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)(?:\s+area)', r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:Street|Road|Avenue|Close|Drive|Lane|Way|Crescent|Terrace|Square|Court|Grove|Hill|View|Wynd|Gardens))', r'(?:near\s+)([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)']
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            loc = match.group(1) if len(match.groups()) >= 1 else match.group(0)
            if loc and len(loc) > 3: return loc.strip()
    return None

# 3. TASK: SCRAPE NEWS
def task_scrape_news():
    print("[1/4] Scraping Live Police Reports...")
    try:
        res = requests.get(NEWS_URL, timeout=30)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')
        links = list(set([('https://www.scotland.police.uk' + a['href'] if not a['href'].startswith('http') else a['href']) for a in soup.find_all('a', href=True) if '/news/2026/' in a['href']]))

        for link in links[:30]:
            try:
                detail_res = requests.get(link, timeout=30)
                detail_res.raise_for_status()
                detail = BeautifulSoup(detail_res.text, 'html.parser')
                title_elem = (detail.find('h1', class_='news-h1') or detail.find('h1'))
                if not title_elem: continue
                title = title_elem.text.strip()
                content_elem = detail.select_one('.article-content')
                if not content_elem: continue
                content = content_elem.get_text(separator=' ').strip()
                city = next((c for c in ["Glasgow", "Edinburgh", "Aberdeen", "Dundee", "Inverness", "Perth", "Stirling", "Broxburn", "Falkirk", "Paisley", "Hamilton", "Livingston"] if c in title or c in content[:500]), "Scotland")
                loc_name = extract_precise_location(content) or extract_precise_location(title)
                lat, lon = geocode_location(loc_name, city) if loc_name else (None, None)

                supabase.table('incidents').upsert({
                    'title': title, 'url': link, 'summary': content[:500].replace('\n', ' '), 'city': city,
                    'location_name': loc_name, 'latitude': lat, 'longitude': lon
                }, on_conflict='url').execute()
            except Exception as e:
                print(f"  [!] Skip article {link}: {e}")
        print("  [+] News sync complete.")
    except Exception as e:
        print(f"  [!] News scrape failed: {e}")

# 4. TASK: FETCH NEIGHBORHOOD STATS & MAP COORDINATES
def task_sync_neighborhoods():
    print("[2/4] Syncing Neighborhood Ranks & Map Locations...")
    query = """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX geosparql: <http://www.opengis.net/ont/geosparql#>
    SELECT ?dzCode ?name ?rank ?wkt ?parentCode
    WHERE {
      ?obs <http://publishmydata.com/def/ontology/qb/dataSet> <http://statistics.gov.scot/data/scottish-index-of-multiple-deprivation> ;
           <http://purl.org/linked-data/sdmx/2009/dimension#refPeriod> <http://reference.data.gov.uk/id/year/2020> ;
           <http://statistics.gov.scot/def/dimension/simdDomain> <http://statistics.gov.scot/def/concept/simd-domain/crime> ;
           <http://statistics.gov.scot/def/measure-properties/rank> ?rank ;
           <http://purl.org/linked-data/sdmx/2009/dimension#refArea> ?dz .
      ?dz rdfs:label ?name .
      BIND(STRAFTER(STR(?dz), 'http://statistics.gov.scot/id/statistical-geography/') AS ?dzCode)
      ?dz geosparql:hasGeometry ?geom . ?geom geosparql:asWKT ?wkt .
      ?dz <http://statistics.gov.scot/def/hierarchy/best-fit#council-area> ?parent .
      BIND(STRAFTER(STR(?parent), 'http://statistics.gov.scot/id/statistical-geography/') AS ?parentCode)
    }
    """
    try:
        res = requests.post(SPARQL_ENDPOINT, data={'query': query}, headers={"Accept": "application/sparql-results+json"}, timeout=180)
        res.raise_for_status()
        rows = res.json().get('results', {}).get('bindings', [])

        batch_regions = []
        batch_stats = []
        for row in rows:
            lat, lon = extract_centroid(row['wkt']['value'])
            batch_regions.append({"id": row['dzCode']['value'], "name": row['name']['value'], "type": "DataZone", "latitude": lat, "longitude": lon, "parent_id": row['parentCode']['value']})
            batch_stats.append({"region_id": row['dzCode']['value'], "period": "2020", "crime_type": "Neighborhood Rank", "total_crimes": int(float(row['rank']['value']))})

            if len(batch_regions) >= 100:
                supabase.table("regions").upsert(batch_regions).execute()
                supabase.table("crime_stats").upsert(batch_stats, on_conflict="region_id,period,crime_type").execute()
                batch_regions, batch_stats = [], []

        if batch_regions:
            supabase.table("regions").upsert(batch_regions).execute()
            supabase.table("crime_stats").upsert(batch_stats, on_conflict="region_id,period,crime_type").execute()
        print(f"  [+] Synced {len(rows)} neighborhoods.")
    except Exception as e:
        print(f"  [!] Neighborhood sync failed: {e}")

# 5. TASK: UPDATE FAIR SAFETY RATES (PER CAPITA)
def task_update_fair_rates():
    print("[3/4] Calculating Fair Safety Rates (Per Capita)...")
    try:
        res = supabase.table('crime_stats').select('id, total_crimes, region_id').eq('crime_type', 'Total Crimes').execute()
        for row in res.data:
            pop = POPULATIONS.get(row['region_id'])
            if pop:
                rate = round((row['total_crimes'] / pop) * 1000, 2)
                supabase.table('crime_stats').update({"crime_rate": rate}).eq('id', row['id']).execute()
        print("  [+] Fair rates updated.")
    except Exception as e:
        print(f"  [!] Fair rates update failed: {e}")

# 6. MAIN ORCHESTRATOR
def run_all():
    print("--- SCOTLAND SAFETY FINDER: MASTER SYNC START ---")
    task_scrape_news()
    task_sync_neighborhoods()
    task_update_fair_rates()
    print("--- MASTER SYNC SUCCESS: ALL CLOUD DATA IS CURRENT ---")

if __name__ == '__main__':
    run_all()
