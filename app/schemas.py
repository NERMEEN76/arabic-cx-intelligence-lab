from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    query: str = Field(min_length=2, max_length=500)
    top_k: int = Field(default=3, ge=1, le=10)


class SearchHit(BaseModel):
    id: str
    title: str
    category: str
    score: float
    snippet: str


class SearchResponse(BaseModel):
    query: str
    intent: str
    sentiment: str
    escalation: bool
    hits: list[SearchHit]


class AnswerResponse(SearchResponse):
    answer: str
    citations: list[str]
    grounded: bool
