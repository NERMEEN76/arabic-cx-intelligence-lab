from __future__ import annotations
import json
from pathlib import Path
from .retrieval import Document, HybridRetriever
from .guardrails import detect_triage, redact_pii


class CXEngine:
    def __init__(self, kb_path: str | Path):
        rows = json.loads(Path(kb_path).read_text(encoding="utf-8"))
        self.docs = [Document(**r) for r in rows]
        self.retriever = HybridRetriever(self.docs)

    def search(self, query: str, top_k: int = 3):
        safe_query = redact_pii(query)
        triage = detect_triage(safe_query)
        hits = self.retriever.search(safe_query, top_k)
        return triage, hits

    def grounded_answer(self, query: str, top_k: int = 3) -> dict:
        triage, hits = self.search(query, top_k)
        if not hits or hits[0].score < 0.16:
            return {
                "triage": triage,
                "hits": hits,
                "answer": "لم أجد سياسة موثوقة بما يكفي للإجابة. سيتم تحويل الطلب إلى موظف دعم بشري.",
                "citations": [],
                "grounded": False,
            }
        top = hits[0].doc
        prefix = "أفهم أن التجربة غير مرضية. " if triage.sentiment == "negative" else ""
        answer = prefix + top.body
        if triage.escalation:
            answer += " تم وضع الحالة ضمن مسار التصعيد البشري للمراجعة."
        return {
            "triage": triage,
            "hits": hits,
            "answer": answer,
            "citations": [h.doc.id for h in hits[:2]],
            "grounded": True,
        }
