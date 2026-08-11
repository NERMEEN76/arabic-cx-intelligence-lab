# Architecture

## Goal
A compact, testable Arabic/English customer-experience retrieval and triage service that demonstrates production-oriented ML engineering without requiring external APIs or proprietary data.

## Request path
`Client -> FastAPI -> PII redaction -> intent/sentiment/escalation -> hybrid retrieval -> grounded response -> citations`

## Retrieval
The executable demo fuses word-level TF-IDF with Arabic-tolerant character n-grams. This makes the repository runnable offline and exposes a clean retriever interface.

### Production upgrade
1. Replace the character branch with multilingual dense embeddings (e.g., Arabic-capable Sentence Transformers).
2. Store vectors in pgvector/OpenSearch/FAISS or a managed vector store.
3. Add BM25 + dense reciprocal-rank/weighted fusion.
4. Add a reranker for the top-N candidates.
5. Feed retrieved evidence to an LLM through a provider adapter.
6. Enforce source citations and calibrated abstention.

## Reliability and scale
- Stateless FastAPI service behind a load balancer.
- Redis cache for repeated retrieval and session metadata.
- Async provider calls; queue for long-running enrichment.
- Structured logs, trace IDs, latency histograms, retrieval metrics, grounding metrics.
- Circuit breaker, timeouts, retry with jitter, idempotency where relevant.
- Shadow evaluation and canary releases for retriever/model changes.

## Evaluation
The repo includes a deterministic synthetic benchmark with Recall@1, Recall@3 and MRR. A production evaluation suite would add faithfulness, answer relevance, intent F1, calibration, latency p50/p95/p99, and Arabic dialect slices.

## Safety / governance
- PII redaction before retrieval/logging.
- Human escalation for sensitive complaints and low-confidence answers.
- No proprietary or scraped customer data is included.
- Synthetic KB is intentionally small and auditable.
