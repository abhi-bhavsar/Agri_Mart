import os
from pathlib import Path

from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
)

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
)

from langchain_core.prompts import ChatPromptTemplate


# ============================================================
# Environment
# ============================================================

load_dotenv(override=True)


# ============================================================
# Paths
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

KNOWLEDGE_DIR = BASE_DIR / "data" / "knowledge"
VECTORSTORE_DIR = BASE_DIR / "vectorstore"

KNOWLEDGE_DIR.mkdir(
    parents=True,
    exist_ok=True
)

VECTORSTORE_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# Embedding Model
# ============================================================

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# ============================================================
# Built-in Knowledge
# ============================================================

BUILT_IN_KNOWLEDGE = """
AGRI-MARKET INTELLIGENCE KNOWLEDGE BASE

MANDI:
A mandi is a wholesale agricultural market where agricultural
commodities are brought by producers and traded with buyers.

MODAL PRICE:
Modal price is the representative price reported for a commodity
in a market and is commonly used as an indicator of the prevailing
market price.

MINIMUM PRICE:
The minimum price represents the lowest reported price for a
commodity during the relevant market observation period.

MAXIMUM PRICE:
The maximum price represents the highest reported price for a
commodity during the relevant market observation period.

ARRIVAL:
Arrival refers to the quantity of agricultural produce reaching
a mandi during a particular period.

ARRIVAL VOLUME:
Arrival volume represents the quantity of agricultural produce
arriving at a mandi. In this project it is expressed in Metric Tons.

STAR SCHEMA:
The agricultural market warehouse uses a Star Schema.

The central fact table is:
fact_mandi_daily

The dimensions include:
dim_location
dim_crop
dim_weather
dim_date

FACT TABLE:
fact_mandi_daily contains daily agricultural market measurements
such as prices and crop arrival quantities.

LOCATION DIMENSION:
dim_location contains geographical information such as state,
district and market name.

CROP DIMENSION:
dim_crop contains information about agricultural commodities
such as crop names and categories.

DATE DIMENSION:
dim_date contains date-related information such as date,
month, year and season.

WEATHER DIMENSION:
dim_weather contains weather-related measurements associated
with agricultural market locations and dates.

BUSINESS INTELLIGENCE:
The system combines mandi prices, crop arrivals, locations,
dates and weather information to support agricultural market
analysis.

PRICE DISCREPANCIES:
Comparing prices for the same crop across different markets
can reveal differences in market conditions.

SUPPLY VOLUME:
Crop arrival volumes provide information about the quantity
of produce reaching a particular mandi.

WEATHER DISRUPTION:
Rainfall and extreme weather can affect agricultural harvesting,
transportation, supply and market arrivals. Such effects should
be treated as contextual explanations unless supported by actual
observations in the database.

IMPORTANT:
Numerical values such as actual prices, rainfall measurements,
arrival volumes and dates must be obtained from the database
when the user asks for current or historical market data.
The knowledge base should not be used to invent numerical
market observations.
"""


# ============================================================
# Load Documents
# ============================================================

def load_knowledge_documents():

    documents = []

    # Built-in knowledge
    from langchain_core.documents import Document

    documents.append(
        Document(
            page_content=BUILT_IN_KNOWLEDGE,
            metadata={
                "source": "built-in-agri-market-knowledge"
            },
        )
    )

    # External knowledge files
    if KNOWLEDGE_DIR.exists():

        for file_path in KNOWLEDGE_DIR.rglob("*"):

            if not file_path.is_file():
                continue

            suffix = file_path.suffix.lower()

            try:

                if suffix in [".txt", ".md"]:

                    loader = TextLoader(
                        str(file_path),
                        encoding="utf-8"
                    )

                    documents.extend(
                        loader.load()
                    )

                elif suffix == ".pdf":

                    loader = PyPDFLoader(
                        str(file_path)
                    )

                    documents.extend(
                        loader.load()
                    )

            except Exception as e:

                print(
                    f"Could not load {file_path}: {e}"
                )

    return documents


# ============================================================
# Create / Load Vector Database
# ============================================================

def create_vectorstore():

    vectorstore = Chroma(
        collection_name="agri_market_knowledge",
        embedding_function=embeddings,
        persist_directory=str(VECTORSTORE_DIR),
    )

    existing = vectorstore.get(
        limit=1
    )

    # Only create embeddings when collection is empty
    if not existing.get("ids"):

        documents = load_knowledge_documents()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=150,
        )

        chunks = splitter.split_documents(
            documents
        )

        if chunks:

            vectorstore.add_documents(
                documents=chunks
            )

            print(
                f"Added {len(chunks)} knowledge chunks."
            )

    return vectorstore


vectorstore = create_vectorstore()


# ============================================================
# Retriever
# ============================================================

retriever = vectorstore.as_retriever(
    search_kwargs={
        "k": 4
    }
)


# ============================================================
# Groq LLM
# ============================================================

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY"),
)


# ============================================================
# RAG Prompt
# ============================================================

rag_prompt = ChatPromptTemplate.from_template(
    """
You are the knowledge assistant for an Indian agricultural
market intelligence system.

Use ONLY the supplied knowledge context to answer the question.

Rules:

1. Do not invent facts.

2. Do not invent prices, rainfall values, arrival volumes,
   dates or other numerical market observations.

3. If the knowledge context does not contain enough information,
   say that the knowledge base does not contain enough information.

4. Use clear and concise language.

5. This component handles definitions, documentation,
   terminology and general agricultural-market knowledge.

Knowledge Context:
------------------
{context}
------------------

User Question:
{question}

Answer:
"""
)


# ============================================================
# RAG Query
# ============================================================

def ask_rag(question: str) -> str:

    try:

        documents = retriever.invoke(
            question
        )

        if not documents:

            return (
                "The knowledge base does not contain "
                "enough information to answer this question."
            )

        context = "\n\n".join(
            document.page_content
            for document in documents
        )

        messages = rag_prompt.format_messages(
            context=context,
            question=question,
        )

        response = llm.invoke(
            messages
        )

        return response.content

    except Exception as e:

        return f"Error executing RAG query: {str(e)}"