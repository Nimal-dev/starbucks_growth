import os
import urllib.request
import ssl

# Bypass SSL verification for legacy reasons if needed
ssl._create_default_https_context = ssl._create_unverified_context

DATA_DIR = r"C:\Users\nimal\.gemini\antigravity\brain\d8ef292e-b575-4487-87cd-95e8682534ea\data\raw"
os.makedirs(DATA_DIR, exist_ok=True)

URLS = {
    # Prioritize datasets with population and lat/lng
    "world_cities.csv": [
        "https://raw.githubusercontent.com/dr5hn/countries-states-cities-database/master/csv/cities.csv",
        "https://raw.githubusercontent.com/datasets/world-cities/master/data/world-cities.csv",
    ],
    "starbucks_locations.csv": [
        "https://raw.githubusercontent.com/Namratha2301/starbucks_global_presence/master/starbucks.csv",
        "https://raw.githubusercontent.com/mmcloughlin/starbucks/master/locations.csv", 
        "https://raw.githubusercontent.com/chrismeller/StarbucksLocations/master/directory.csv"
    ]
}

def download_file(url, filename):
    print(f"Attempting to download {filename} from {url}...")
    try:
        # Use a custom opener to handle some anti-bot headers if needed (basic User-Agent)
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)
        
        file_path = os.path.join(DATA_DIR, filename)
        urllib.request.urlretrieve(url, file_path)
        
        # Check if file has content and is not a 404 text response
        if os.path.getsize(file_path) > 1000:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                header = f.readline()
                if "404: Not Found" in header:
                    print(f"Warning: Downloaded 404 page from {url}")
                    return False
            print(f"Success: {filename}")
            return True
        else:
            print(f"Warning: File too small ({os.path.getsize(file_path)} bytes).")
            return False
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return False

for name, sent_urls in URLS.items():
    if isinstance(sent_urls, list):
        success = False
        for url in sent_urls:
            if download_file(url, name):
                success = True
                break
        if not success:
            print(f"Error: Could not download {name} from any source.")
    else:
        download_file(sent_urls, name)
