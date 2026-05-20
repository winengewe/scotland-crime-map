import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
url = os.environ.get('SUPABASE_URL')
# Use the anon key from index.html
anon_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imh1bnVsd21sbWV1cmtncGRrYmhwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzg5Mzg4MDksImV4cCI6MjA5NDUxNDgwOX0.pNFwpAeocVRCE39EBZXJ7-HF-TXYBMt3ogEeANDsGsM'

print(f"Testing access to {url}")
client = create_client(url, anon_key)

tables = ['regions', 'crime_stats', 'incidents']
for table in tables:
    try:
        res = client.table(table).select('*', count='exact').limit(1).execute()
        print(f"Table '{table}': OK. Rows found: {res.count}")
    except Exception as e:
        print(f"Table '{table}': FAILED. Error: {e}")
