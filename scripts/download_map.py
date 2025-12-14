import urllib.request
import ssl
import os

# Bypass SSL verification
ssl._create_default_https_context = ssl._create_unverified_context

URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/World_map_blank_gmt_equirectangular.svg/2560px-World_map_blank_gmt_equirectangular.svg.png"
OUTPUT_PATH = r"F:\Project Works\New folder\dashboard\world-map.png"

def download_map():
    print(f"Downloading map from {URL}...")
    try:
        req = urllib.request.Request(
            URL, 
            data=None, 
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
            }
        )
        with urllib.request.urlopen(req) as response, open(OUTPUT_PATH, 'wb') as out_file:
            data = response.read()
            out_file.write(data)
        print(f"Success: Saved to {OUTPUT_PATH}")
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    download_map()
