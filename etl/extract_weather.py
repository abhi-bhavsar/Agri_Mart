import os
import json
import requests
from pathlib import Path
from datetime import datetime, timedelta

# Setup directories
RAW_DATA_DIR = Path("data/raw")
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

# Sample coordinates for major Maharashtra Mandis
LOCATIONS = {
    "Pune": {"lat": 18.5204, "lon": 73.8567},
    "Nashik": {"lat": 20.0110, "lon": 73.7903},
    "Lasalgaon": {"lat": 20.1415, "lon": 74.2255},
    "Wagholi": {"lat": 18.5794, "lon": 73.9822}
}

def fetch_weather_data():
    print("Fetching weather data from Open-Meteo...")
    
    # Get data for the last 7 days
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=7)
    
    weather_results = []
    
    for market, coords in LOCATIONS.items():
        url = (
            f"https://archive-api.open-meteo.com/v1/archive?"
            f"latitude={coords['lat']}&longitude={coords['lon']}"
            f"&start_date={start_date}&end_date={end_date}"
            f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&timezone=auto"
        )
        
        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            # Attach the market name to the response for easier merging later
            data["market_name"] = market
            weather_results.append(data)
            print(f"Fetched weather for {market}")
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather for {market}: {e}")
            
    output_file = RAW_DATA_DIR / "weather_raw.json"
    with open(output_file, "w") as f:
        json.dump(weather_results, f, indent=4)
        
    print(f"Success! Weather data saved to {output_file}")

if __name__ == "__main__":
    fetch_weather_data()