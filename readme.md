```markdown
# Agri-Market Intelligence & Price Tracker

### A Business Intelligence and Conversational AI Platform for Indian Wholesale Mandis

Agri-Market Intelligence & Price Tracker is an end-to-end Business Intelligence and Conversational AI platform designed to transform fragmented agricultural market information into a structured, queryable, and decision-support system.

The project integrates agricultural mandi prices, crop arrival volumes, weather information, ETL processing, a PostgreSQL-based Star Schema data warehouse, Business Intelligence dashboards, and a conversational AI layer.

The conversational layer allows users to ask natural-language questions about agricultural markets without manually writing SQL queries. It combines an LLM-powered SQL Agent, Retrieval-Augmented Generation (RAG), semantic search, and intelligent SQL/RAG/Hybrid query routing.

---

## Table of Contents

- [Overview](#overview)
- [Problem Statement](#problem-statement)
- [Business Challenges](#business-challenges)
- [Project Objectives](#project-objectives)
- [Proposed Solution](#proposed-solution)
- [System Architecture](#system-architecture)
- [Implemented Architecture](#implemented-architecture)
- [Data Sources](#data-sources)
- [Data Engineering and ETL](#data-engineering-and-etl)
- [Data Warehouse](#data-warehouse)
- [Star Schema](#star-schema)
- [Business Intelligence Layer](#business-intelligence-layer)
- [Conversational AI Layer](#conversational-ai-layer)
- [SQL Agent](#sql-agent)
- [RAG Knowledge Base](#rag-knowledge-base)
- [Embeddings and ChromaDB](#embeddings-and-chromadb)
- [Query Router](#query-router)
- [Hybrid Question Answering](#hybrid-question-answering)
- [Answer Synthesis](#answer-synthesis)
- [FastAPI Backend](#fastapi-backend)
- [React Frontend](#react-frontend)
- [End-to-End Request Flow](#end-to-end-request-flow)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Environment Configuration](#environment-configuration)
- [Installation](#installation)
- [Running the Backend](#running-the-backend)
- [Running the Frontend](#running-the-frontend)
- [API Documentation](#api-documentation)
- [Example Queries](#example-queries)
- [SQL vs RAG vs Hybrid](#sql-vs-rag-vs-hybrid)
- [Data Safety](#data-safety)
- [Current Implementation](#current-implementation)
- [Current Limitations](#current-limitations)
- [Future Enhancements](#future-enhancements)
- [Project Significance](#project-significance)
- [Conclusion](#conclusion)

---

## Overview

Agricultural markets in India generate large amounts of information about crop prices, arrivals, market locations, and environmental conditions.

However, this information is often fragmented across different sources and can be difficult to compare and analyze together.

* A farmer may need to compare prices between multiple mandis before selling a crop.
* A trader may need to identify markets with favorable prices and sufficient supply.
* A logistics provider may need to understand where crop arrivals are concentrated.
* An analyst may need to study the relationship between agricultural market conditions and weather.

Agri-Market Intelligence brings these different information requirements into a unified analytical platform.

The system combines:
- Agricultural market data
- Crop arrival/supply information
- Weather information
- Data cleaning and transformation
- PostgreSQL data warehousing
- Star Schema modeling
- Business Intelligence dashboards
- Natural-language SQL querying
- Retrieval-Augmented Generation
- Semantic search
- Intelligent query routing
- Conversational AI

The result is a system where structured agricultural data remains available for analytical queries while domain knowledge is available through a dedicated RAG knowledge base.

---

## Problem Statement

The agricultural supply chain in India suffers from fragmented market information.

A farmer growing onions in one district may sell the harvest without knowing that another nearby market is experiencing a supply shortage and offering a different price.

Similarly, traders, wholesale buyers, and logistics companies may have difficulty determining:
- Which market has better prices
- Where crop supply is concentrated
- How much produce is arriving at a particular market
- How prices vary across districts
- Whether environmental conditions may affect agricultural markets

This creates an information gap between agricultural markets and the people who depend on them. The project focuses on three major information problems:

### 1. Price Discrepancies
The same crop can have significantly different prices across different markets. The system organizes daily market-level price information so that users can compare prices across locations.

### 2. Supply Volumes
Crop arrivals provide information about the amount of agricultural produce reaching a market. Monitoring arrival volumes helps users understand where supply is concentrated.

### 3. Weather Disruptions
Weather conditions such as rainfall and temperature can influence agricultural production, transportation, supply, and market conditions. Integrating weather information with market data provides a common analytical environment for studying these relationships.

---

## Business Challenges

The project addresses several practical challenges associated with agricultural data.

### Inconsistent Names
Government and market data may contain variations in market and location names. 
For example:
```text
Nashik -> Nasik
Wagholi -> Vagholi

```

These inconsistencies can cause problems during joins and aggregation. The ETL layer therefore performs data cleaning and standardization.

### Missing Information

Market data may contain missing observations for certain dates or locations. The data pipeline is responsible for preparing the dataset for downstream analytical use.

### Multiple Data Formats

Mandi and weather data may come from different sources and structures. Weather information may arrive in nested JSON structures, while agricultural market data may be represented in tabular formats. The ETL layer transforms these sources into a common analytical structure.

### Fragmented Analysis

Without a centralized data warehouse, users may need to manually combine information from different sources. The project addresses this by integrating the information into a centralized warehouse.

### Natural-Language Accessibility

Traditional database systems require users to understand SQL. The conversational layer allows users to ask questions in natural language and have the system determine the appropriate analytical path.

---

## Project Objectives

The major objectives of the project are:

* Collect agricultural market data from external sources.
* Collect weather information for relevant locations.
* Clean and standardize agricultural market data.
* Handle inconsistent market and crop names.
* Prepare structured analytical datasets.
* Store the processed information in a PostgreSQL data warehouse.
* Organize the warehouse using a Star Schema.
* Integrate crop, location, date, and weather dimensions.
* Support Business Intelligence analysis.
* Provide natural-language access to structured data.
* Implement an LLM-powered SQL Agent.
* Implement Retrieval-Augmented Generation (RAG).
* Build a semantic knowledge retrieval layer using ChromaDB.
* Automatically classify questions as SQL, RAG, or Hybrid.
* Combine structured database evidence with contextual knowledge.
* Provide answers through a React conversational interface.

---

## Proposed Solution

The overall solution combines traditional Business Intelligence with Generative AI.

```text
                    AGRICULTURAL DATA
                           │
              ┌────────────┴────────────┐
              │                         │
        Mandi Data                 Weather Data
              │                         │
              └────────────┬────────────┘
                           │
                           ▼
                    ETL PIPELINE
                           │
              ┌────────────┴────────────┐
              │                         │
          Cleaning                 Transformation
              │                         │
              └────────────┬────────────┘
                           │
                           ▼
                 POSTGRESQL WAREHOUSE
                           │
                     STAR SCHEMA
                           │
              ┌────────────┴────────────┐
              │                         │
              ▼                         ▼
       BI DASHBOARDS             CONVERSATIONAL AI
                                        │
                                        ▼
                                  QUERY ROUTER
                                        │
                         ┌──────────────┼──────────────┐
                         │              │              │
                         ▼              ▼              ▼
                        SQL            RAG           HYBRID
                         │              │              │
                         ▼              ▼              ▼
                    PostgreSQL       ChromaDB       SQL + RAG
                         │              │              │
                         └──────────────┼──────────────┘
                                        │
                                        ▼
                                  GPT-OSS 20B
                                        │
                                        ▼
                                  FINAL ANSWER
                                        │
                                        ▼
                                  REACT FRONTEND

```

---

## System Architecture

The platform contains two major analytical paths.

**Traditional BI Path**

```text
Data Sources ──► ETL Pipeline ──► PostgreSQL ──► Star Schema ──► BI Dashboards

```

This path is responsible for structured analytical reporting.

**Conversational AI Path**

```text
User ──► React Frontend ──► FastAPI ──► Query Router
                                              │
                                              ├──── SQL ────► SQL Agent ────► PostgreSQL
                                              │
                                              ├──── RAG ────► Retriever ────► ChromaDB
                                              │
                                              └── Hybrid ───► SQL + RAG
                                                                  │
                                                                  ▼
                                                           Answer Synthesis
                                                                  │
                                                                  ▼
                                                             GPT-OSS 20B
                                                                  │
                                                                  ▼
                                                            Final Response

```

---

## Implemented Architecture

The conversational system is implemented as a modular backend.

```text
                         USER
                           │
                           ▼
                    React Frontend
                           │
                           │ HTTP POST
                           ▼
                     FastAPI API
                           │
                           ▼
                     Query Router
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
         SQL              RAG             Hybrid
          │                │                │
          ▼                ▼                │
     SQL Agent         Retriever            │
          │                │                │
          ▼                ▼                │
     PostgreSQL         ChromaDB             │
          │                │                │
          └────────────────┼────────────────┘
                           │
                           ▼
                    Answer Synthesis
                           │
                           ▼
                      GPT-OSS 20B
                           │
                           ▼
                     Final Response
                           │
                           ▼
                    React Frontend

```

The architecture intentionally separates:

**Structured Knowledge** (Stored and queried through PostgreSQL)

* Market prices
* Crop arrivals
* Crop information
* Market information
* Dates
* Weather measurements
* Aggregations

**Unstructured Knowledge** (Stored in the RAG knowledge base)

* Agricultural terminology
* Mandi concepts
* Data dictionary
* Project documentation
* Data warehouse concepts
* Domain explanations

---

## Data Sources

The original project design uses external sources rather than relying exclusively on pre-cleaned static datasets.

**Agricultural Market Data**
Government agricultural market/open-data sources are used for information such as:

* Minimum prices
* Maximum prices
* Market price information
* Crop arrivals
* Market locations
* Crop information

**Weather Data**
Weather information is obtained through Open-Meteo. The weather layer provides information such as:

* Temperature
* Rainfall
* Date
* Location-associated weather conditions

The ETL process combines the agricultural and weather datasets into a common analytical structure.

---

## Data Engineering and ETL

The ETL layer prepares raw data for analytical use.

```text
Raw Data ──► Extraction ──► Data Cleaning ──► Transformation ──► Warehouse Loading ──► PostgreSQL

```

The ETL implementation is designed around Python and data-processing libraries, including:

* Python
* pandas
* requests
* fuzzy string matching
* PostgreSQL

### Data Cleaning

Data cleaning is an important part of the project because raw agricultural datasets can contain inconsistencies:

* **Location Name Variations:** Different spellings of the same market can be standardized.
* **Missing Values:** Missing observations can be handled before loading the analytical warehouse.
* **Data Type Standardization:** Price, arrival, date, and weather fields need to be converted into consistent types.
* **Weather Transformation:** Weather API responses may contain nested structures that need to be transformed into tabular data before being associated with agricultural market records.

---

## Data Warehouse

The analytical backend uses PostgreSQL. The warehouse follows a Star Schema design, separating measurable business facts from descriptive dimensions.

### Star Schema

```text
                         dim_location
                              │
                              │
                              ▼
dim_crop ───────────► fact_mandi_daily ◄────────── dim_date
                              │
                              │
                              ▼
                         dim_weather

```

This structure allows users to analyze market observations by crop, location, date, and weather conditions.

* **Fact Table (`fact_mandi_daily`):** Contains measurable market observations (minimum price, maximum price, market price, crop arrival/supply volume, foreign keys to dimensions).
* **Location Dimension (`dim_location`):** Contains attributes such as State, District, Market name.
* **Crop Dimension (`dim_crop`):** Contains agricultural crop information.
* **Date Dimension (`dim_date`):** Provides temporal context.
* **Weather Dimension (`dim_weather`):** Stores weather-related observations associated with the relevant market/date context.

---

## Business Intelligence Layer

The project is designed as a Business Intelligence solution in addition to the conversational AI layer to support analytical activities such as:

* Market comparison
* Crop-level analysis
* Price analysis
* Arrival/supply analysis
* Geographic analysis
* Time-based analysis
* Weather-related analysis

The project contains a dedicated `dashboards/` directory for dashboard-related resources. The intended dashboard experience allows users to explore market conditions through visual analytics (market-level price comparison, crop selection, supply/arrival comparison, geographic market analysis, price range analysis, weather-related market information).

---

## Conversational AI Layer

The conversational AI layer allows users to interact with the agricultural warehouse using natural language. Instead of writing `SELECT ...`, users can ask: *"Which market has the lowest onion price?"*

The system determines the type of question and selects the appropriate information source. The conversational system supports three major routes: **SQL, RAG, and HYBRID**.

### SQL Agent

Provides natural-language access to the PostgreSQL warehouse using LangChain, LangChain Community SQL utilities, LangChain SQL Agent Toolkit, ChatGroq, GPT-OSS 20B, PostgreSQL, and psycopg2.

The SQL Agent is responsible for questions requiring structured numerical information.

```text
Natural-Language Question ──► SQL Agent ──► Inspect Database Schema ──► Generate SQL ──► Execute Database Query ──► Retrieve Results ──► Generate Natural-Language Answer

```

The SQL Agent is instructed to treat the database as the source of truth for numerical market information and avoid inventing database values.

**SQL Agent Example Questions:**

* Which mandi has the lowest onion price?
* Which market has the highest onion arrivals?
* What is the highest price of tomatoes?
* What is the average price for a particular crop?
* Compare prices between two markets.

### RAG Knowledge Base

SQL is effective for structured numerical questions but is not suitable for conceptual questions like *"What is a mandi?"* or *"What is modal price?"*. For such questions, the project implements Retrieval-Augmented Generation.

```text
Knowledge Documents ──► Document Loaders ──► Text Splitting ──► HuggingFace Embeddings ──► ChromaDB ──► Semantic Retrieval ──► Relevant Context ──► GPT-OSS 20B ──► Grounded Response

```

**Knowledge Sources:**
Agricultural terminology, mandi terminology, data dictionary, project documentation, Star Schema concepts, database terminology, market-related concepts. Supports `.txt`, `.md`, `.pdf`.

### Embeddings and ChromaDB

The RAG system uses HuggingFace sentence-transformer embeddings (`sentence-transformers/all-MiniLM-L6-v2`) to convert text into numerical vector representations stored in ChromaDB.

```text
User Question ──► Question Embedding ──► Semantic Search ──► Relevant Chunks ──► GPT-OSS 20B ──► Grounded Answer

```

---

## Query Router

The Query Router determines which processing path should handle a user question using structured output to classify incoming questions.

* **SQL Route:** Used when the question requires structured database information. (e.g., *"Which mandi has the highest onion price?"*) ➔ Routed to: `SQL Agent → PostgreSQL`
* **RAG Route:** Used when the question requires domain knowledge or project documentation. (e.g., *"What is a mandi?"*) ➔ Routed to: `Retriever → ChromaDB → GPT-OSS 20B`
* **Hybrid Route:** Used when a question requires both contextual knowledge and structured database information. (e.g., *"What is modal price and which market has the highest modal price?"*) ➔ Combines `RAG (Definition) + SQL (Actual market value)`.

---

## Hybrid Question Answering

The Hybrid architecture combines structured database evidence with retrieved contextual knowledge.

```text
                    USER QUESTION
                          │
                          ▼
                    QUERY ROUTER
                          │
                ┌─────────┴─────────┐
                │                   │
                ▼                   ▼
               SQL                 RAG
                │                   │
                ▼                   ▼
          PostgreSQL             ChromaDB
                │                   │
                ▼                   ▼
          SQL Evidence         Retrieved Context
                │                   │
                └─────────┬─────────┘
                          │
                          ▼
                   ANSWER SYNTHESIS
                          │
                          ▼
                     GPT-OSS 20B
                          │
                          ▼
                    FINAL RESPONSE

```

This architecture maintains a clear distinction between **Database Evidence** (Prices, Arrivals, Dates, Market values, Aggregations, Structured weather values) and **Retrieved Knowledge** (Definitions, Explanations, Domain concepts, Project documentation).

---

## FastAPI Backend

The conversational AI system is exposed through FastAPI.

* **Main API endpoint:** `POST /api/v1/query`

**Example Request:**

```json
{
  "question": "Which mandi has the lowest onion price?"
}

```

**Example Response:**

```json
{
  "question": "Which mandi has the lowest onion price?",
  "answer": "....",
  "source": "sql"
}

```

The `source` field identifies the processing route (`sql`, `rag`, or `hybrid`).

**FastAPI Endpoints:**

* `GET /` - Provides basic application information.
* `GET /health` - Used for basic backend health checking.
* `POST /api/v1/query` - Processes a natural-language analytical question.

---

## React Frontend

The project contains a React-based conversational interface allowing users to enter natural-language questions, send them to the FastAPI backend, display generated answers, and identify the answer source.

```text
User ──► React Chat Interface ──► POST /api/v1/query ──► FastAPI ──► Query Router ──► SQL / RAG / Hybrid ──► Answer ──► React UI

```

The interface displays the source used for the response (e.g., `Source: PostgreSQL`, `Source: Knowledge Base`, `Source: PostgreSQL + Knowledge Base`).

---

## SQL vs RAG vs Hybrid

One of the core architectural decisions of this project is that SQL and RAG solve different problems. The goal is not to replace SQL with RAG, but to combine them: **SQL = Structured Data | RAG = Unstructured Knowledge | Hybrid = Structured Data + Knowledge**

| Capability | SQL | RAG | Hybrid |
| --- | --- | --- | --- |
| Market prices | Yes | No | Yes |
| Crop arrivals | Yes | No | Yes |
| Aggregations | Yes | No | Yes |
| Market comparisons | Yes | No | Yes |
| Dates | Yes | No | Yes |
| Weather measurements | Yes | No | Yes |
| Agricultural definitions | No | Yes | Yes |
| Mandi terminology | No | Yes | Yes |
| Project documentation | No | Yes | Yes |
| Data dictionary | No | Yes | Yes |
| Numerical database evidence | Yes | No | Yes |
| Context + numerical evidence | No | No | Yes |

---

## Technology Stack

* **Programming:** Python, JavaScript, SQL
* **Data Engineering:** pandas, requests, fuzzy string matching
* **Database:** PostgreSQL, psycopg2
* **Business Intelligence:** Power BI, Tableau
* **Generative AI:** GPT-OSS 20B, Groq, LangChain
* **SQL Agent:** LangChain SQL utilities, LangChain SQL Agent Toolkit
* **RAG:** LangChain, HuggingFace Embeddings, Sentence Transformers, ChromaDB, PyPDF
* **Backend:** FastAPI, Pydantic, Uvicorn, python-dotenv
* **Frontend:** React, JavaScript, CSS

---

## Project Structure

```text
Agri_Mart/
│
├── api/                  # Conversational AI backend
│   ├── __pycache__/
│   ├── agent.py          # PostgreSQL SQL Agent configuration
│   ├── answer.py         # Final answer synthesis for Hybrid queries
│   ├── main.py           # FastAPI application and API endpoints
│   ├── models.py         # Pydantic request and response models
│   ├── rag.py            # RAG pipeline, ChromaDB retrieval, etc.
│   └── router.py         # SQL/RAG/Hybrid query classification logic
│
├── dashboards/           # Business Intelligence and dashboard resources
├── data/                 # Agricultural data and processing resources
├── database/             # Database and warehouse-related resources
├── etl/                  # ETL and data-processing components
├── frontend/             # React conversational interface
├── knowledge/            # Documents used by the RAG knowledge base
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md

```

---

## Environment Configuration

Create a `.env` file in the project root. Use `.env.example` as the template.

```env
GROQ_API_KEY=your_groq_api_key_here

PG_USER=postgres
PG_PASSWORD=your_postgres_password
PG_HOST=127.0.0.1
PG_PORT=5432
PG_DBNAME=mandi_warehouse

```

**Environment Variables:**

| Variable | Purpose |
| --- | --- |
| `GROQ_API_KEY` | API key for Groq LLM inference |
| `PG_USER` | PostgreSQL username |
| `PG_PASSWORD` | PostgreSQL password |
| `PG_HOST` | PostgreSQL host |
| `PG_PORT` | PostgreSQL port |
| `PG_DBNAME` | PostgreSQL database name |

*(Never commit the real `.env` file to GitHub.)*

---

## Installation

**1. Clone the Repository**

```bash
git clone [https://github.com/abhi-bhavsar/Agri_Mart.git](https://github.com/abhi-bhavsar/Agri_Mart.git)
cd Agri_Mart

```

**2. Create a Python Virtual Environment**
*Windows:*

```bash
python -m venv .venv
.venv\Scripts\activate

```

*Linux/macOS:*

```bash
python3 -m venv .venv
source .venv/bin/activate

```

**3. Install Dependencies**

```bash
pip install -r requirements.txt

```

**4. Configure PostgreSQL**
Create the required PostgreSQL database (`mandi_warehouse` or configure another database name through `PG_DBNAME=your_database_name`). Ensure that the required Star Schema tables are available.

**5. Configure Environment Variables**
Create `.env` and provide the required credentials.

---

## Running the Backend

Run the following command from the project root:

```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000

```

For development with automatic reload:

```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

```

* The backend will be available at: `http://127.0.0.1:8000`
* Swagger API documentation: `http://127.0.0.1:8000/docs`

---

## Running the Frontend

Open another terminal.

```bash
cd frontend
npm install
npm run dev

```

The React development server will provide the local frontend URL. The frontend communicates with the FastAPI backend.

---

## Data Safety

The system is designed primarily for analytical and read-oriented interaction with the PostgreSQL warehouse. The SQL Agent should not be used as a mechanism for modifying or deleting production data.

Sensitive credentials must remain outside the repository. The `.gitignore` prevents `.env`, `.venv/`, `frontend/node_modules/`, `frontend/dist/`, `vectorstore/`, `__pycache__/`, and `*.pyc` from being committed.

---

## Current Limitations

* **External Data Reliability:** Government and weather APIs may experience downtime, delayed updates, missing records, schema changes, or inconsistent data.
* **Data Quality:** Agricultural market data can contain missing observations, naming inconsistencies, reporting variations, and different market conventions.
* **LLM Dependence:** The conversational layer depends on an external LLM inference provider.
* **SQL Agent Reliability:** Natural-language-to-SQL systems should be carefully evaluated for complex analytical queries.
* **Predictive Analytics:** The current implementation primarily supports descriptive analysis, not machine learning forecasting.
* **Production Deployment:** Currently structured as a development/academic implementation. Production requires authentication, monitoring, scaling, secret management, connection pooling, and automated testing.

---

## Future Enhancements

1. **Agricultural Price Forecasting:** Add a machine learning forecasting layer to estimate future crop prices.
2. **Weather-Based Market Risk:** Models that study relationships between weather, crop supply, and price movement.
3. **Automated Market Alerts:** Alerts for significant price changes, unusual price differences, or extreme weather.
4. **Advanced Business Intelligence:** Interactive India maps, state-level drilldowns, crop-specific heatmaps.
5. **Conversational Analytics:** Multi-turn conversations, conversation memory, follow-up questions, and natural-language chart generation.
6. **LLM Evaluation:** Formal evaluation framework for SQL accuracy, hallucination rate, and token usage.
7. **Production Deployment:** Reverse Proxy, Monitoring Layer, Authentication.

---

## Project Significance

The project demonstrates how traditional Business Intelligence systems can be extended with Generative AI. Instead of building an isolated chatbot, the conversational AI layer is connected directly to a structured analytical warehouse.

This creates a combination of:
`Data Engineering + Data Warehousing + Business Intelligence + Natural-Language SQL + Retrieval-Augmented Generation + Generative AI`

The architecture maintains a clear separation between numerical market evidence and contextual domain knowledge. A language model should not be expected to invent or estimate database values when the required information already exists in a structured database.

---

## End-to-End Architecture

```text
                         AGRICULTURAL DATA
                                │
                  ┌─────────────┴─────────────┐
                  │                           │
             MANDI DATA                 WEATHER DATA
                  │                           │
                  └─────────────┬─────────────┘
                                │
                                ▼
                         ETL PIPELINE
                                │
                  ┌─────────────┴─────────────┐
                  │                           │
             EXTRACTION                 TRANSFORMATION
                  │                           │
                  └─────────────┬─────────────┘
                                │
                                ▼
                           CLEAN DATA
                                │
                                ▼
                      POSTGRESQL WAREHOUSE
                                │
                           STAR SCHEMA
                                │
                 ┌──────────────┴──────────────┐
                 │                             │
                 ▼                             ▼
          BI DASHBOARDS                 CONVERSATIONAL AI
                                               │
                                               ▼
                                         FASTAPI BACKEND
                                               │
                                               ▼
                                          QUERY ROUTER
                                               │
                          ┌────────────────────┼────────────────────┐
                          │                    │                    │
                          ▼                    ▼                    ▼
                         SQL                  RAG                 HYBRID
                          │                    │                    │
                          ▼                    ▼                    │
                     SQL AGENT             RETRIEVER               │
                          │                    │                    │
                          ▼                    ▼                    │
                     PostgreSQL             ChromaDB                │
                          │                    │                    │
                          └────────────────────┼────────────────────┘
                                               │
                                               ▼
                                        ANSWER SYNTHESIS
                                               │
                                               ▼
                                          GPT-OSS 20B
                                               │
                                               ▼
                                        FINAL RESPONSE
                                               │
                                               ▼
                                         REACT FRONTEND

```

---

## Conclusion

Agri-Market Intelligence & Price Tracker combines agricultural data engineering, data warehousing, Business Intelligence, and Generative AI into a unified market intelligence platform.

The system transforms fragmented agricultural market information into a structured PostgreSQL warehouse and provides two complementary methods of intelligent interaction:

1. SQL-based analytical querying for structured market data.
2. RAG-based knowledge retrieval for agricultural and project-domain information.

A Query Router determines whether a question should use SQL, RAG, or both. The Hybrid architecture then combines structured database evidence with retrieved contextual knowledge when required. The resulting platform provides a foundation for conversational exploration of agricultural market information while maintaining the structured architecture required for Business Intelligence.

---

## Authors

## Author

**Abhishek Bhavsar**
* GitHub: [@abhi-bhavsar](https://github.com/abhi-bhavsar)

**Your Name**
* GitHub: [@PravinWankhare](https://github.com/PravinWankhare)
