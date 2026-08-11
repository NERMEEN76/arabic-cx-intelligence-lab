# Arabic CX RAG Lab

**Author:** Dr. Nermeen Shehabeldeen  

**Senior AI/ML Engineer candidate proof-of-work** — a compact Arabic/English customer-experience retrieval, triage, grounding, and escalation service.

> Independent portfolio project. Uses synthetic data only. No proprietary company data, branding, or internal APIs.

## Why this repo exists
A CV says *what I know*. This repository shows *how I think*: measurable retrieval quality, clear interfaces, safe failure modes, API delivery, tests, and a realistic production migration path.

## Highlights
- Arabic normalization robust to common orthographic variants.
- Hybrid word + character retrieval designed for mixed Arabic/English CX queries.
- Intent, sentiment, escalation and PII-redaction guardrails.
- Grounded answers with evidence IDs and low-confidence abstention.
- FastAPI service with typed request/response models.
- Deterministic synthetic benchmark: Recall@1, Recall@3, MRR.
- Production architecture note covering dense retrieval, reranking, vector DB, caching, observability and evaluation.

## Run
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
python scripts/benchmark.py
pytest -q
uvicorn app.api:app --reload
```
Then open `http://127.0.0.1:8000/docs`.

## Example
```bash
curl -X POST http://127.0.0.1:8000/answer \
  -H "Content-Type: application/json" \
  -d '{"query":"اتخصم مني المبلغ مرتين من البطاقة ومحتاج حل","top_k":3}'
```

## Design choice: runnable before flashy
The local demo deliberately avoids downloading large embedding/LLM models so a reviewer can clone and run it immediately. The retriever interface is designed so the lexical character branch can be replaced by multilingual dense embeddings in production; see `docs/ARCHITECTURE.md`.

## Repository map
- `app/retrieval.py` — hybrid retrieval.
- `app/guardrails.py` — triage and PII protection.
- `app/engine.py` — orchestration and grounded response.
- `app/api.py` — FastAPI endpoints.
- `scripts/benchmark.py` — retrieval evaluation.
- `tests/` — unit tests.
- `docs/ARCHITECTURE.md` — production design.
- `docs/ROLE_ALIGNMENT.md` — capability-to-evidence matrix.

## Browser demo
After starting the API, open `http://127.0.0.1:8000/demo` for a recruiter-friendly interactive screen, or `/docs` for the API contract.

## Evaluation integrity
The current synthetic benchmark is intentionally not cherry-picked: the character branch wins over the first untuned fusion configuration. That result is documented in `docs/RESULTS.md` together with the next experiment. Showing an honest negative/neutral experiment is part of the engineering signal.
