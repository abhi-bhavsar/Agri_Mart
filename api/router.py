import os

from dotenv import load_dotenv

from typing import Literal

from pydantic import BaseModel, Field

from langchain_groq import ChatGroq


load_dotenv(override=True)


# ============================================================
# Route Schema
# ============================================================

class QueryRoute(BaseModel):

    route: Literal[
        "sql",
        "rag",
        "hybrid"
    ] = Field(
        description=(
            "The retrieval strategy required to answer "
            "the user's question."
        )
    )

    reason: str = Field(
        description=(
            "A short explanation for why this route "
            "was selected."
        )
    )


# ============================================================
# Groq LLM
# ============================================================

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY"),
)


router_llm = llm.with_structured_output(
    QueryRoute
)


# ============================================================
# Query Router
# ============================================================

def route_question(question: str) -> QueryRoute:

    prompt = f"""
You are the query router for an agricultural
market intelligence system.

Choose exactly ONE route.

--------------------------------------------------
SQL
--------------------------------------------------

Use SQL when the question requires structured
information stored in PostgreSQL.

Examples:

- highest crop price
- lowest crop price
- average price
- total arrivals
- crop arrivals
- market comparison
- district comparison
- historical price
- date-based analysis
- weather measurements
- rainfall values
- temperature values
- numerical calculations
- trends
- rankings

--------------------------------------------------
RAG
--------------------------------------------------

Use RAG when the question requires information
from the knowledge/document collection.

Examples:

- What is a mandi?
- What is modal price?
- What does arrival volume mean?
- Explain agricultural market terminology.
- Explain the purpose of the Star Schema.
- Explain how weather can affect agricultural supply.
- Explain project documentation.

--------------------------------------------------
HYBRID
--------------------------------------------------

Use HYBRID when the question requires BOTH:

1. Numerical/observational information from PostgreSQL
2. Contextual/document information from the knowledge base

Examples:

- Why did onion prices increase after rainfall?
- Explain the relationship between rainfall and mandi prices
  using the available market data.
- What happened to prices after a weather disruption and
  what could explain the change?

Important:

Do not choose RAG for questions asking for actual numerical
market observations.

Do not choose SQL for pure definitions or documentation.

User Question:
{question}
"""

    try:

        return router_llm.invoke(
            prompt
        )

    except Exception as e:

        print(
            f"Router error: {e}"
        )

        # Hybrid is the safest fallback because it allows
        # both structured and unstructured evidence to be used.
        return QueryRoute(
            route="hybrid",
            reason="Router failed; using both data sources."
        )