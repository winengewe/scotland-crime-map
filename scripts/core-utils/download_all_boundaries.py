import requests
import json
import os
import time

BASE_URL = "https://maps.gov.scot/server/rest/services/ScotGov/StatisticalUnits/MapServer/2/query"
OUTPUT_FILE = r"C:\Users\vince\OneDrive\Documents\Antigravity Skills\scotland-crime-map\data_zones.json"

def download_all():
    all_features = []
    offset = 0
    limit = 250 # Reduced from 1000 for better reliability

    print("[*] Starting robust multi-page boundary download (250 per page)...")

    while True:
        params = {
            'where': '1=1',
            'outFields': '*',
            'f': 'geojson',
            'resultOffset': offset,
            'resultRecordCount': limit,
            'outSR': '4326'
        }

        print(f"  [>] Fetching offset {offset}...")
        try:
            r = requests.get(BASE_URL, params=params, timeout=120) # Increased timeout
            r.raise_for_status()

            if 'html' in r.headers.get('Content-Type', '').lower():
                print(f"      [!] Received HTML. Server is overloaded at offset {offset}. Retrying in 15s...")
                time.sleep(15)
                continue

            data = r.json()
            features = data.get('features', [])
            if not features:
                print("      [*] No more features found.")
                break

            all_features.extend(features)
            print(f"      Got {len(features)} features. (Total: {len(all_features)})")

            if len(features) < limit:
                break

            offset += limit
            # Moderate delay to prevent rate-limiting
            time.sleep(2)
        except Exception as e:
            print(f"      [!] Error at offset {offset}: {e}. Retrying in 20s...")
            time.sleep(20)
            continue
    full_geojson = {
        "type": "FeatureCollection",
        "features": all_features
    }

    with open(OUTPUT_FILE, 'w') as f:
        json.dump(full_geojson, f)

    print(f"\n[!] SUCCESS: Downloaded {len(all_features)} boundaries to {OUTPUT_FILE}")
if __name__ == '__main__':
    download_all()
