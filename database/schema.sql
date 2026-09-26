-- Drop existing tables to allow for clean testing
DROP TABLE IF EXISTS fact_mandi_daily CASCADE;
DROP TABLE IF EXISTS dim_weather CASCADE;
DROP TABLE IF EXISTS dim_crop CASCADE;
DROP TABLE IF EXISTS dim_location CASCADE;
DROP TABLE IF EXISTS dim_date CASCADE;

-- 1. Date Dimension
CREATE TABLE dim_date (
    date_key INT PRIMARY KEY,
    full_date DATE NOT NULL UNIQUE,
    day_name VARCHAR(15),
    month_name VARCHAR(15),
    month_num INT,
    quarter INT,
    year INT,
    season VARCHAR(20)
);

-- 2. Location Dimension (Can be normalized further into a Snowflake schema by splitting State and District)
CREATE TABLE dim_location (
    location_key SERIAL PRIMARY KEY,
    market_name VARCHAR(100) NOT NULL,
    district VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    latitude DECIMAL(9, 6),
    longitude DECIMAL(9, 6),
    UNIQUE(market_name, district, state)
);

-- 3. Crop Dimension
CREATE TABLE dim_crop (
    crop_key SERIAL PRIMARY KEY,
    crop_name VARCHAR(100) NOT NULL UNIQUE,
    crop_category VARCHAR(50)
);

-- 4. Weather Dimension
CREATE TABLE dim_weather (
    weather_key SERIAL PRIMARY KEY,
    date_key INT REFERENCES dim_date(date_key),
    location_key INT REFERENCES dim_location(location_key),
    temperature_max_c DECIMAL(5, 2),
    temperature_min_c DECIMAL(5, 2),
    precipitation_sum_mm DECIMAL(6, 2),
    disruption_alert VARCHAR(50),
    UNIQUE(date_key, location_key)
);

-- 5. Central Fact Table
CREATE TABLE fact_mandi_daily (
    transaction_id SERIAL PRIMARY KEY,
    date_key INT REFERENCES dim_date(date_key),
    location_key INT REFERENCES dim_location(location_key),
    crop_key INT REFERENCES dim_crop(crop_key),
    weather_key INT REFERENCES dim_weather(weather_key),
    min_price DECIMAL(10, 2),
    max_price DECIMAL(10, 2),
    modal_price DECIMAL(10, 2),
    arrival_volume_tons DECIMAL(10, 2),
    price_spread DECIMAL(10, 2),
    data_delayed_flag SMALLINT DEFAULT 0
);