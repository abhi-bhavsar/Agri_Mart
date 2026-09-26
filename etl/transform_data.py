import json
import pandas as pd
from rapidfuzz import process
from pathlib import Path

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

STANDARD_MANDIS = ["Nashik", "Pune", "Wagholi", "Lasalgaon", "Baramati", "Mumbai"]

def standardize_location(name: str) -> str:
    if pd.isna(name):
        return name
    match, score, _ = process.extractOne(str(name), STANDARD_MANDIS)
    return match if score >= 80 else str(name).title()

def transform_mandi_data():
    print("Transforming Mandi Data...")
    csv_file = RAW_DIR / "Mandi_dataset.csv"
    if not csv_file.exists():
        print(f"Error: {csv_file} not found!")
        return None

    df = pd.read_csv(csv_file)
    df.columns = df.columns.str.strip().str.lower()

   # 2. Rename columns to match database schema
    column_mapping = {
        "market": "market_name",
        "commodity": "crop_name",
        "arrival_date": "full_date",
        "min_x0020_price": "min_price",
        "max_x0020_price": "max_price",
        "modal_x0020_price": "modal_price"
    }
    df.rename(columns=column_mapping, inplace=True)
    df.rename(columns=column_mapping, inplace=True)

    df["market_name"] = df["market_name"].apply(standardize_location)
    df["crop_name"] = df["crop_name"].astype(str).str.title()
    
    numeric_cols = ["min_price", "max_price", "modal_price"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
            
    if "arrivals_in_qtl" in df.columns:
        df["arrival_volume_tons"] = pd.to_numeric(df["arrivals_in_qtl"], errors="coerce") / 10.0
    else:
        df["arrival_volume_tons"] = 0.0

    df["full_date"] = pd.to_datetime(df["full_date"], format="mixed", dayfirst=True, errors="coerce")
    df.sort_values(by=["crop_name", "market_name", "full_date"], inplace=True)
    
    df["modal_price"] = df.groupby(["crop_name", "market_name"])["modal_price"].transform(
        lambda group: group.ffill().bfill()
    )
    
    df["price_spread"] = df["max_price"] - df["min_price"]

    expected_cols = ["state", "district", "market_name", "crop_name", "full_date", 
                     "min_price", "max_price", "modal_price", "arrival_volume_tons", "price_spread"]
    final_cols = [c for c in expected_cols if c in df.columns]
    df = df[final_cols]

    output_path = PROCESSED_DIR / "mandi_cleaned.csv"
    df.to_csv(output_path, index=False)
    print(f"Mandi data saved to {output_path}")
    return df

def transform_weather_data():
    print("Transforming Weather Data...")
    weather_json_file = RAW_DIR / "weather_raw.json"
    if not weather_json_file.exists():
        print("Warning: weather_raw.json not found. Run extract_weather.py first.")
        return None

    with open(weather_json_file, "r") as f:
        weather_payload = json.load(f)

    weather_rows = []
    for entry in weather_payload:
        market = entry.get("market_name")
        daily = entry.get("daily", {})
        dates = daily.get("time", [])
        t_max = daily.get("temperature_2m_max", [])
        t_min = daily.get("temperature_2m_min", [])
        precipitation = daily.get("precipitation_sum", [])

        for d, mx, mn, pr in zip(dates, t_max, t_min, precipitation):
            alert = "Heavy Rain" if (pr and pr > 30) else ("Heatwave" if (mx and mx > 40) else "Normal")
            weather_rows.append({
                "market_name": market,
                "full_date": d,
                "temperature_max_c": mx,
                "temperature_min_c": mn,
                "precipitation_sum_mm": pr,
                "disruption_alert": alert
            })

    df_weather = pd.DataFrame(weather_rows)
    df_weather["full_date"] = pd.to_datetime(df_weather["full_date"])
    
    output_path = PROCESSED_DIR / "weather_cleaned.csv"
    df_weather.to_csv(output_path, index=False)
    print(f"Weather data saved to {output_path}")
    return df_weather

if __name__ == "__main__":
    transform_mandi_data()
    transform_weather_data()