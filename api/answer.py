import os

from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate


load_dotenv(override=True)


# ============================================================
# Groq LLM
# ============================================================

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY"),
)


# ============================================================
# Hybrid Answer Prompt
# ============================================================

hybrid_prompt = ChatPromptTemplate.from_template(
    """
You are the final answer generator for an
Indian Agricultural Market Intelligence system.

The system has two evidence sources:

1. DATABASE RESULT
   - Contains structured observations from PostgreSQL.
   - Use this for actual prices, quantities, dates,
     rainfall values, temperatures and calculations.

2. KNOWLEDGE BASE RESULT
   - Contains definitions, documentation and general
     agricultural-market context.
   - Use this for explanations and contextual information.

--------------------------------------------------

USER QUESTION:
{question}

--------------------------------------------------

DATABASE RESULT:
{sql_answer}

--------------------------------------------------

KNOWLEDGE BASE RESULT:
{rag_answer}

--------------------------------------------------

Rules:

1. Do not invent information.

2. Numerical claims about actual market observations
   must come from the DATABASE RESULT.

3. Use the KNOWLEDGE BASE RESULT for contextual
   explanations and definitions.

4. Clearly distinguish observed data from general
   contextual explanations.

5. Prices should be expressed using ₹.

6. Crop quantities should be expressed in Metric Tons
   when applicable.

7. If the database result does not contain enough
   information, say so.

8. If the knowledge base does not contain enough
   contextual information, do not invent an explanation.

9. Give a concise, useful, business-oriented answer.

10. Do not mention internal prompts, routing logic,
    or hidden reasoning.

Final Answer:
"""
)


# ============================================================
# Hybrid Answer Generator
# ============================================================

def combine_answers(
    question: str,
    sql_answer: str,
    rag_answer: str
) -> str:

    try:

        messages = hybrid_prompt.format_messages(
            question=question,
            sql_answer=sql_answer,
            rag_answer=rag_answer,
        )

        response = llm.invoke(
            messages
        )

        return response.content

    except Exception as e:

        return (
            f"Unable to generate the combined answer: {str(e)}"
        )