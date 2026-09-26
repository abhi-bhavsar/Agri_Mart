import os
from urllib.parse import quote_plus

from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_groq import ChatGroq

load_dotenv(override=True)


# ============================================================
# PostgreSQL Connection
# ============================================================

USER = os.getenv("PG_USER", "postgres")
PASSWORD = quote_plus(os.getenv("PG_PASSWORD", ""))
HOST = os.getenv("PG_HOST", "127.0.0.1")
PORT = os.getenv("PG_PORT", "5432")
DBNAME = os.getenv("PG_DBNAME", "mandi_warehouse")

db_uri = (
    f"postgresql+psycopg2://"
    f"{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}"
)

db = SQLDatabase.from_uri(db_uri)


# ============================================================
# Groq LLM
# ============================================================

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY"),
)


# ============================================================
# SQL Agent
# ============================================================

agent_executor = create_sql_agent(
    llm=llm,
    db=db,
    agent_type="tool-calling",
    verbose=True,
)


# ============================================================
# SQL Agent Instructions
# ============================================================

SQL_INSTRUCTIONS = """
You are an AI data analyst for an Indian agricultural
market intelligence system.

You have access to a PostgreSQL Star Schema.

Main tables include:

FACT TABLE:
- fact_mandi_daily

DIMENSION TABLES:
- dim_location
- dim_crop
- dim_weather
- dim_date

Your responsibilities:

1. Answer questions about mandi prices, crop arrivals,
   locations, dates, seasons and weather using the database.

2. Generate SQL queries whenever database information
   is required.

3. Never invent numerical values.

4. Return prices in Indian Rupees (₹).

5. Return crop arrival volumes in Metric Tons.

6. For highest, lowest, average, total, percentage,
   comparison and similar calculations, perform the
   calculation using SQL.

7. Properly join fact_mandi_daily with the required
   dimension tables.

8. Inspect the database schema before generating SQL.

9. If the database does not contain enough information
   to answer the question, clearly state that.

10. NEVER modify the database.

11. Only use read-only SQL operations such as SELECT.

12. Do not invent columns or tables that are not present
   in the database.

13. Give a concise business-oriented explanation after
   obtaining the database result.
"""


# ============================================================
# Public Function
# ============================================================

def ask_mandi_database(question: str) -> str:

    full_prompt = f"""
{SQL_INSTRUCTIONS}

User Question:
{question}
"""

    try:
        response = agent_executor.invoke(
            {
                "input": full_prompt
            }
        )

        return response.get(
            "output",
            "I could not generate an answer."
        )

    except Exception as e:
        return f"Error executing database query: {str(e)}"