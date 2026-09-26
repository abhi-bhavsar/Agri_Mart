import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv(override= True)

# Build connection string from .env variables
USER = os.getenv("PG_USER", "postgres")
PASSWORD = os.getenv("PG_PASSWORD")
HOST = os.getenv("PG_HOST", "localhost")
PORT = os.getenv("PG_PORT", "5432")
DBNAME = os.getenv("PG_DBNAME", "mandi_warehouse")

engine = create_engine(f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}")

def load_data():
    print("Loading cleaned data into PostgreSQL Star Schema...")
    
    # Load processed CSVs
    try:
        df_mandi = pd.read_csv("data/processed/mandi_cleaned.csv")
        df_weather = pd.read_csv("data/processed/weather_cleaned.csv")
    except FileNotFoundError as e:
        print(f"Error loading CSVs: {e}")
        return

    # Convert dates safely
    df_mandi["full_date"] = pd.to_datetime(df_mandi["full_date"]).dt.date
    df_weather["full_date"] = pd.to_datetime(df_weather["full_date"]).dt.date

    with engine.begin() as conn:
        # 1. Load Dim_Crop
        print("Loading dim_crop...")
        dim_crop = pd.DataFrame({'crop_name': df_mandi['crop_name'].dropna().unique()})
        dim_crop['crop_category'] = 'Uncategorized' 
        # Using ON CONFLICT DO NOTHING to prevent errors if you run this multiple times
        dim_crop.to_sql('dim_crop_staging', conn, if_exists='replace', index=False)
        conn.exec_driver_sql("""
            INSERT INTO dim_crop (crop_name, crop_category)
            SELECT crop_name, crop_category FROM dim_crop_staging
            ON CONFLICT (crop_name) DO NOTHING;
        """)

        # 2. Load Dim_Location
        print("Loading dim_location...")
        dim_loc = df_mandi[['market_name', 'district', 'state']].drop_duplicates().dropna()
        dim_loc.to_sql('dim_location_staging', conn, if_exists='replace', index=False)
        conn.exec_driver_sql("""
            INSERT INTO dim_location (market_name, district, state)
            SELECT market_name, district, state FROM dim_location_staging
            ON CONFLICT (market_name, district, state) DO NOTHING;
        """)

        # 3. Load Dim_Date
        print("Loading dim_date...")
        all_dates = pd.concat([pd.Series(df_mandi["full_date"]), pd.Series(df_weather["full_date"])]).dropna().unique()
        dim_date = pd.DataFrame({'full_date': all_dates})
        dim_date['date_key'] = pd.to_datetime(dim_date['full_date']).dt.strftime('%Y%m%d').astype(int)
        dim_date['day_name'] = pd.to_datetime(dim_date['full_date']).dt.day_name()
        dim_date['month_name'] = pd.to_datetime(dim_date['full_date']).dt.month_name()
        dim_date['month_num'] = pd.to_datetime(dim_date['full_date']).dt.month
        dim_date['quarter'] = pd.to_datetime(dim_date['full_date']).dt.quarter
        dim_date['year'] = pd.to_datetime(dim_date['full_date']).dt.year
        dim_date['season'] = 'General'
        
        dim_date.to_sql('dim_date_staging', conn, if_exists='replace', index=False)
        conn.exec_driver_sql("""
            INSERT INTO dim_date (date_key, full_date, day_name, month_name, month_num, quarter, year, season)
            SELECT date_key, full_date, day_name, month_name, month_num, quarter, year, season FROM dim_date_staging
            ON CONFLICT (full_date) DO NOTHING;
        """)

        # 4. Extract Keys for Fact Table and Weather
        print("Mapping keys for Fact Table...")
        # Write mandi to staging
        df_mandi.to_sql('mandi_staging', conn, if_exists='replace', index=False)
        
        # Write weather to staging
        df_weather.to_sql('weather_staging', conn, if_exists='replace', index=False)
        
        # 5. Insert into Dim_Weather
        print("Loading dim_weather...")
        conn.exec_driver_sql("""
            INSERT INTO dim_weather (date_key, location_key, temperature_max_c, temperature_min_c, precipitation_sum_mm, disruption_alert)
            SELECT 
                d.date_key, 
                l.location_key, 
                w.temperature_max_c, 
                w.temperature_min_c, 
                w.precipitation_sum_mm, 
                w.disruption_alert
            FROM weather_staging w
            JOIN dim_date d ON w.full_date = d.full_date
            JOIN dim_location l ON w.market_name = l.market_name
            ON CONFLICT (date_key, location_key) DO NOTHING;
        """)

        # 6. Insert into Fact Table
        print("Loading fact_mandi_daily...")
        conn.exec_driver_sql("""
            INSERT INTO fact_mandi_daily (date_key, location_key, crop_key, min_price, max_price, modal_price, arrival_volume_tons, price_spread)
            SELECT 
                d.date_key,
                l.location_key,
                c.crop_key,
                s.min_price,
                s.max_price,
                s.modal_price,
                s.arrival_volume_tons,
                s.price_spread
            FROM mandi_staging s
            JOIN dim_date d ON s.full_date = d.full_date
            JOIN dim_location l ON s.market_name = l.market_name AND s.district = l.district AND s.state = l.state
            JOIN dim_crop c ON s.crop_name = c.crop_name;
        """)
        
        # Cleanup staging tables
        conn.exec_driver_sql("DROP TABLE IF EXISTS dim_crop_staging, dim_location_staging, dim_date_staging, mandi_staging, weather_staging;")

    print("Success! Star Schema fully populated.")

if __name__ == "__main__":
    load_data()