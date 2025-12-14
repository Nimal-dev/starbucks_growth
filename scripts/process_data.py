import csv
import math
import os
import json

# Configuration
RAW_DIR = r"data/raw"
PROCESSED_DIR = r"data/processed"
os.makedirs(PROCESSED_DIR, exist_ok=True)

CITY_POP_THRESHOLD = 50000 
SEARCH_RADIUS_KM = 10.0

def haversine(lat1, lon1, lat2, lon2):
    try:
        R = 6371  # Earth radius in km
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        return R * c
    except:
        return 99999

def processed_data():
    print("Loading and cleaning data (Standard Libs)...")
    
    cities = []
    stores = []

    # Read Cities
    try:
        with open(os.path.join(RAW_DIR, "world_cities.csv"), 'r', encoding='utf-8', errors='ignore') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Check required fields
                if not row.get('latitude') or not row.get('longitude') or not row.get('population'):
                    continue
                
                try:
                    pop = float(row.get('population', 0))
                    if pop < CITY_POP_THRESHOLD:
                        continue
                        
                    cities.append({
                        'city': row.get('name'),
                        'country': row.get('country_name'),
                        'lat': float(row.get('latitude')),
                        'lng': float(row.get('longitude')),
                        'population': pop
                    })
                except ValueError:
                    continue
    except Exception as e:
        print(f"Error reading cities: {e}")
        return

    print(f"Filtered to {len(cities)} cities with pop >= {CITY_POP_THRESHOLD}")

    # Read Starbucks
    try:
        with open(os.path.join(RAW_DIR, "starbucks_locations.csv"), 'r', encoding='utf-8', errors='ignore') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get('Brand') != 'Starbucks':
                    continue
                
                if not row.get('Latitude') or not row.get('Longitude'):
                    continue
                    
                try:
                    stores.append({
                        'store_name': row.get('Store Name'),
                        'lat': float(row.get('Latitude')),
                        'lng': float(row.get('Longitude'))
                    })
                except ValueError:
                    continue
    except Exception as e:
        print(f"Error reading stores: {e}")
        return

    print(f"Processing {len(stores)} Starbucks locations")

    # Spatial Join using Grid Bucketing
    print("Building spatial grid...")
    grid = {}
    for store in stores:
        grid_key = (int(store['lat'] * 10), int(store['lng'] * 10))
        if grid_key not in grid:
            grid[grid_key] = []
        grid[grid_key].append(store)

    print("Matching cities to stores...")
    results = []
    
    for city in cities:
        c_lat, c_lng = city['lat'], city['lng']
        c_key_lat, c_key_lng = int(c_lat * 10), int(c_lng * 10)
        
        store_count = 0
        
        # Check 3x3 neighbor grids
        for d_lat in [-1, 0, 1]:
            for d_lng in [-1, 0, 1]:
                key = (c_key_lat + d_lat, c_key_lng + d_lng)
                if key in grid:
                    for store in grid[key]:
                        dist = haversine(c_lat, c_lng, store['lat'], store['lng'])
                        if dist <= SEARCH_RADIUS_KM:
                            store_count += 1
        
        stores_per_100k = (store_count / city['population']) * 100000 if city['population'] > 0 else 0
        
        results.append({
            'city': city['city'],
            'country': city['country'],
            'population': city['population'],
            'lat': c_lat,
            'lng': c_lng,
            'store_count': store_count,
            'stores_per_100k': round(stores_per_100k, 2)
        })

    # Sort by Opportunity (High Pop, Low Stores)
    # Simple metric: Pop / (StoreCount + 1)
    results.sort(key=lambda x: x['population'] / (x['store_count'] + 1), reverse=True)

    print("Saving processed data...")
    
    # CSV Output
    with open(os.path.join(PROCESSED_DIR, "city_analysis.csv"), 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['city', 'country', 'population', 'lat', 'lng', 'store_count', 'stores_per_100k']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
        
    # JSON Output
    with open(os.path.join(PROCESSED_DIR, "city_analysis.json"), 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
        
    print("Done.")

if __name__ == "__main__":
    processed_data()
