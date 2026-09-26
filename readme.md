# 🌾 Agri-Market Intelligence Data Warehouse & Analytics Pipeline

## Project Overview

An end-to-end data engineering and business intelligence solution designed to track, analyze, and visualize Indian agricultural market (Mandi) trends. This project integrates automated ETL workflows, dual-architecture data warehousing in PostgreSQL, a FastAPI backend, a React frontend, and interactive Power BI dashboards to provide actionable insights into commodity prices, arrival volumes, and weather impacts.

## System Architecture & Pipelines

This repository implements a complete data pipeline consisting of five primary components:

1. **ETL Pipeline (Extract, Transform, Load):**
* **Extraction:** Python scripts (`extract_mandi.py`, `extract_weather.py`) pull raw agricultural pricing and regional weather data.
* **Transformation:** Data cleaning, type casting, and anomaly handling via `transform_data.py`.
* **Loading:** Processed data is pushed to a PostgreSQL database (`load_to_db.py`).


2. **Data Warehousing (PostgreSQL):**
* Implements two distinct schema architectures side-by-side: a **Star Schema** optimized for high-performance Business Intelligence reading, and a **Snowflake Schema** (3NF) ensuring stringent data normalization and zero redundancy.


3. **Backend API (FastAPI):**
* Serves as the communication layer, exposing endpoints for the frontend application to interact with the underlying PostgreSQL warehouse.


4. **Frontend UI (React + Vite):**
* A modern, fast web application providing an intuitive user interface for end-users to query and view market data.


5. **Business Intelligence (Power BI):**
* Pre-configured `.pbix` files offering interactive geospatial maps, price volatility tracking, and KPI summaries linked directly to the warehouse.



## Database Schema Architectures

The project demonstrates advanced dimensional modeling by implementing both industry-standard architectures:

| Feature | Star Schema | Snowflake Schema |
| --- | --- | --- |
| **Primary Use Case** | BI Dashboards & Analytical Queries | Database Normalization & Storage Optimization |
| **Fact Table** | `fact_mandi_daily` | `fact_mandi_snowflake` |
| **Dimensions** | `dim_crop`, `dim_location`, `dim_weather`, `dim_date` | `snow_dim_crop`, `snow_dim_category`, `snow_dim_market`, `snow_dim_district`, `snow_dim_state` |
| **Normalization** | Denormalized (Faster read times) | 3rd Normal Form (3NF) |
| **Relationship** | Single-hop (1-to-Many) | Multi-tiered hierarchy |

## Repository Structure

```text
Agri_Mart/
│
├── api/                        # FastAPI Backend
│   ├── main.py                 # Application entry point
│   └── models.py               # Pydantic data validation models
│
├── dashboards/                 # Power BI Reports
│   ├── Agri_Mart_Star_Schema.pbix
│   └── Agri_Mart_Snowflake_Schema.pbix
│
├── data/                       # Local Data Storage
│   ├── processed/              # Transformed, load-ready data
│   └── raw/                    # Initial raw data extracts
│
├── database/                   # Database DDL & Configuration
│   ├── load_to_db.py           # Database connection and insertion logic
│   └── schema.sql              # SQL scripts for Star & Snowflake schemas
│
├── etl/                        # Data Engineering Scripts
│   ├── extract_mandi.py
│   ├── extract_weather.py
│   └── transform_data.py
│
├── frontend/                   # React/Vite User Interface
│   ├── src/
│   │   ├── App.jsx             # Main UI component
│   │   └── App.css             # UI styling
│   └── package.json
│
├── .env                        # Environment variables (excluded from git)
├── requirements.txt            # Python dependencies
└── README.md

```

## Technology Stack

* **Language:** Python 3.x, JavaScript (ES6+), SQL
* **Database:** PostgreSQL
* **Backend:** FastAPI, Uvicorn, Pydantic
* **Frontend:** React, Vite
* **ETL Processing:** Pandas, Psycopg2
* **Business Intelligence:** Microsoft Power BI

## Local Setup & Installation

### 1. Environment Preparation

Clone the repository and install the required Python dependencies:

```bash
git clone <repository-url>
cd Agri_Mart
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

```

### 2. Database Configuration

Ensure PostgreSQL is running locally on port `5432`. Create a `.env` file in the root directory:

```env
PG_HOST=127.0.0.1
PG_PORT=5432
PG_USER=postgres
PG_PASSWORD=your_password
PG_DBNAME=mandi_warehouse

```

Run the DDL scripts to build the schemas:

```bash
psql -U postgres -d mandi_warehouse -f database/schema.sql

```

### 3. Run the ETL Pipeline

Extract, transform, and load the dataset into the warehouse:

```bash
python etl/extract_mandi.py
python etl/extract_weather.py
python etl/transform_data.py
python database/load_to_db.py

```

### 4. Start the Application

You will need two terminal windows to run the frontend and backend simultaneously.

**Terminal 1: FastAPI Backend**

```bash
python -m api.main

```

**Terminal 2: React Frontend**

```bash
cd frontend
npm install
npm run dev

```

Navigate to `http://localhost:5173/` in your browser to view the application.

## Author

**Abhishek Sanjay Bhavsar**