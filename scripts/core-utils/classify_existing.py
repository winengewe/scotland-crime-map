import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_SERVICE_ROLE_KEY')
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def classify_incident_logic(title, summary):
    text = (title + " " + (summary or "")).lower()
    if any(k in text for k in ['assault', 'murder', 'stab', 'knife', 'weapon', 'attack', 'robbery', 'serious', 'death']):
        return 'Violence'
    if any(k in text for k in ['theft', 'stolen', 'housebreaking', 'burglary', 'shoplift', 'fraud', 'bank']):
        return 'Dishonesty'
    if any(k in text for k in ['drugs', 'cannabis', 'cocaine', 'antisocial', 'noise', 'disorder', 'disperse', 'alcohol']):
        return 'Society'
    if any(k in text for k in ['fire', 'vandalism', 'damage', 'wilful']):
        return 'Damage'
    if any(k in text for k in ['sexual', 'indecent', 'rape', 'lewd']):
        return 'Sexual Crimes'
    return 'Total Crimes'

def backfill_classification():
    print("[*] Fetching all incidents...")
    res = supabase.table('incidents').select('id, title, summary').execute()
    incidents = res.data
    
    print(f"[*] Classifying {len(incidents)} incidents...")
    for inc in incidents:
        new_type = classify_incident_logic(inc['title'], inc['summary'])
        supabase.table('incidents').update({'crime_type': new_type}).eq('id', inc['id']).execute()
    
    print("[!] SUCCESS: All incidents categorized.")

if __name__ == '__main__':
    backfill_classification()
