import json
import os

PROCESSED_DIR = r"data/processed"
DASHBOARD_DIR = r"dashboard"
os.makedirs(DASHBOARD_DIR, exist_ok=True)

def generate_js_data():
    try:
        with open(os.path.join(PROCESSED_DIR, "city_analysis.json"), 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Take top 500 opportunities to keep file size light for the browser
        top_opportunities = data[:500]
        
        # Also grab a sample of existing stores for a map (optional)
        # For now, just the opportunities
        
        js_content = f"const cityData = {json.dumps(top_opportunities, indent=2)};"
        
        with open(os.path.join(DASHBOARD_DIR, "data.js"), 'w', encoding='utf-8') as f:
            f.write(js_content)
            
        print("Successfully created dashboard/data.js")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    generate_js_data()
