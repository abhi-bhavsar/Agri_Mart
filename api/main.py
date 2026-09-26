import uvicorn
from fastapi import FastAPI, HTTPException

from fastapi.middleware.cors import CORSMiddleware

from api.models import (
    QueryRequest,
    QueryResponse,
)

from api.agent import (
    ask_mandi_database,
)

from api.rag import (
    ask_rag,
)

from api.router import (
    route_question,
)

from api.answer import (
    combine_answers,
)


# ============================================================
# FastAPI Application
# ============================================================

app = FastAPI(
    title="Agri-Market Intelligence AI",
    version="1.0.0",
    description=(
        "Conversational BI system combining "
        "PostgreSQL analytics with RAG."
    ),
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# Health Check
# ============================================================

@app.get("/")
async def root():

    return {
        "status": "running",
        "service": "Agri-Market Intelligence AI",
    }


@app.get("/health")
async def health():

    return {
        "status": "healthy"
    }


# ============================================================
# Main Query Endpoint
# ============================================================

@app.post(
    "/api/v1/query",
    response_model=QueryResponse,
)
async def query_database(
    request: QueryRequest
):

    if not request.question.strip():

        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty.",
        )

    question = request.question.strip()

    # --------------------------------------------------------
    # Determine Route
    # --------------------------------------------------------

    route = route_question(
        question
    )

    # --------------------------------------------------------
    # SQL
    # --------------------------------------------------------

    if route.route == "sql":

        answer = ask_mandi_database(
            question
        )

    # --------------------------------------------------------
    # RAG
    # --------------------------------------------------------

    elif route.route == "rag":

        answer = ask_rag(
            question
        )

    # --------------------------------------------------------
    # Hybrid
    # --------------------------------------------------------

    else:

        sql_answer = ask_mandi_database(
            question
        )

        rag_answer = ask_rag(
            question
        )

        answer = combine_answers(
            question=question,
            sql_answer=sql_answer,
            rag_answer=rag_answer,
        )

    # --------------------------------------------------------
    # Response
    # --------------------------------------------------------

    return QueryResponse(
        question=question,
        answer=answer,
        source=route.route,
    )


# ============================================================
# Run Server
# ============================================================

if __name__ == "__main__":

    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )