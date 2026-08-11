# Offline Evaluation Results

Synthetic bilingual CX knowledge base: 20 documents, 20 hand-authored paraphrase queries.

The initial benchmark intentionally reports all branches rather than cherry-picking the fusion result. On this tiny dataset, Arabic-tolerant character n-grams outperform the first untuned weighted fusion. That is a useful engineering signal: hybrid retrieval should be tuned on a larger dialect-stratified set, not assumed to win by default.

Current local run:

```text
word     R@1=0.750  R@3=0.900  MRR=0.832
char     R@1=0.800  R@3=0.950  MRR=0.875
hybrid   R@1=0.750  R@3=0.900  MRR=0.844
```

## Next experiment
Replace the character branch with multilingual dense embeddings, evaluate BM25/dense/hybrid + reranking, and report bootstrap confidence intervals over Recall@K/MRR across Gulf/Egyptian/MSA slices.
