import os
import json
import requests
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv(override=True)

# Setup directories
RAW_DATA_DIR = Path("data/raw")
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

API_KEY = os.getenv("GOV_DATA_API_KEY")
# Using the standard Agmarknet daily price resource ID
RESOURCE_ID = "9ef84268-d588-465a-a308-a864a43d0070" 
def fetch_mandi_data(limit=500): # Reduced limit to ease server load
    if not API_KEY:
        raise ValueError("GOV_DATA_API_KEY is missing from the .env file.")
        
    print("Fetching raw mandi data from data.gov.in (this may take up to 60 seconds)...")
    
    # Added a filter for Maharashtra to narrow down the query and speed up the response
    url = f"https://api.data.gov.in/resource/{RESOURCE_ID}?api-key={API_KEY}&format=json&limit={limit}&filters[state]=Maharashtra"
    
    try:
        # Increased timeout from 20 to 90 seconds
        response = requests.get(url, timeout=90) 
        response.raise_for_status()
        data = response.json()
        
        records = data.get("records", [])
        output_file = RAW_DATA_DIR / "mandi_raw.json"
        
        with open(output_file, "w") as f:
            json.dump(records, f, indent=4)
            
        print(f"Success! {len(records)} records saved to {output_file}")
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching API data: {e}")

if __name__ == "__main__":
    fetch_mandi_data()