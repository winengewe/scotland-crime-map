import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_SERVICE_ROLE_KEY')
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def repair_city_coords():
    print("[*] Fetching cities...")
    cities = supabase.table('regions').select('id, name').is_('parent_id', 'null').execute().data
    
    for city in cities:
        if city['name'] == 'Scotland': continue
        
        print(f"  [>] Calculating center for {city['name']}...")
        # Get all zones in this city
        zones = supabase.table('regions').select('latitude, longitude').eq('parent_id', city['id']).not_.is_('latitude', 'null').execute().data
        
        if zones:
            avg_lat = sum(z['latitude'] for z in zones) / len(zones)
            avg_lng = sum(z['longitude'] for z in zones) / len(zones)
            
            print(f"      Center: {avg_lat}, {avg_lng} (based on {len(zones)} zones)")
            supabase.table('regions').update({
                'latitude': avg_lat,
                'longitude': avg_lng
            }).eq('id', city['id']).execute()
        else:
            print(f"      [!] No zones found for {city['name']}. Skipping.")

if __name__ == '__main__':
    repair_city_coords()
