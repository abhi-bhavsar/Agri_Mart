from typing import Literal

from pydantic import BaseModel, Field


class QueryRequest(BaseModel):

    question: str = Field(
        ...,
        description=(
            "The natural language question to ask "
            "the agricultural market intelligence system."
        )
    )


class QueryResponse(BaseModel):

    question: str

    answer: str

    source: Literal[
        "sql",
        "rag",
        "hybrid"
    ]