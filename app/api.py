from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from .engine import CXEngine
from .schemas import SearchRequest, SearchResponse, SearchHit, AnswerResponse
from .demo import DEMO_HTML

BASE = Path(__file__).resolve().parents[1]
engine = CXEngine(BASE / "data" / "kb.json")
app = FastAPI(title="Arabic CX RAG Lab", version="0.1.0")


def hit_to_model(hit):
    body = hit.doc.body
    return SearchHit(
        id=hit.doc.id,
        title=hit.doc.title,
        category=hit.doc.category,
        score=round(hit.score, 4),
        snippet=(body[:180] + "…") if len(body) > 180 else body,
    )




@app.get("/demo", response_class=HTMLResponse)
def demo():
    return DEMO_HTML


@app.get("/health")
def health():
    return {"status": "ok", "documents": len(engine.docs)}


@app.post("/search", response_model=SearchResponse)
def search(req: SearchRequest):
    triage, hits = engine.search(req.query, req.top_k)
    return SearchResponse(
        query=req.query,
        intent=triage.intent,
        sentiment=triage.sentiment,
        escalation=triage.escalation,
        hits=[hit_to_model(h) for h in hits],
    )


@app.post("/answer", response_model=AnswerResponse)
def answer(req: SearchRequest):
    result = engine.grounded_answer(req.query, req.top_k)
    triage = result["triage"]
    return AnswerResponse(
        query=req.query,
        intent=triage.intent,
        sentiment=triage.sentiment,
        escalation=triage.escalation,
        hits=[hit_to_model(h) for h in result["hits"]],
        answer=result["answer"],
        citations=result["citations"],
        grounded=result["grounded"],
    )
