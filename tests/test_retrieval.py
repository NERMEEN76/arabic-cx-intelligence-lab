from pathlib import Path
from app.engine import CXEngine

ROOT = Path(__file__).resolve().parents[1]
engine = CXEngine(ROOT / "data" / "kb.json")


def test_refund_query_hits_refund_policy():
    _, hits = engine.search("الغيت العملية واريد استرجاع المبلغ", 3)
    assert hits[0].doc.id in {"KB-001", "KB-018"}


def test_api_error_query_hits_technical_policy():
    _, hits = engine.search("API 500 timeout", 3)
    assert hits[0].doc.id == "KB-010"
