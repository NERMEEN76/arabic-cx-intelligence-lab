from __future__ import annotations
from dataclasses import dataclass
from typing import Sequence
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .text import normalize_arabic, join_fields


@dataclass(frozen=True)
class Document:
    id: str
    title: str
    category: str
    body: str
    keywords: list[str]

    @property
    def text(self) -> str:
        return join_fields([self.title, self.category, self.body, " ".join(self.keywords)])


@dataclass(frozen=True)
class Hit:
    doc: Document
    score: float


class HybridRetriever:
    """Offline hybrid retriever: word TF-IDF + Arabic-tolerant character n-grams.

    Production upgrade path: replace char branch with multilingual dense embeddings
    and preserve reciprocal/weighted fusion behind this interface.
    """

    def __init__(self, docs: Sequence[Document], alpha: float = 0.58):
        self.docs = list(docs)
        self.alpha = alpha
        corpus = [normalize_arabic(d.text) for d in self.docs]
        self.word = TfidfVectorizer(ngram_range=(1, 2), min_df=1, sublinear_tf=True)
        self.char = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), min_df=1, sublinear_tf=True)
        self.word_x = self.word.fit_transform(corpus)
        self.char_x = self.char.fit_transform(corpus)

    @staticmethod
    def _scale(v: np.ndarray) -> np.ndarray:
        v = np.asarray(v, dtype=float)
        vmax, vmin = float(v.max(initial=0)), float(v.min(initial=0))
        if vmax - vmin < 1e-12:
            return v
        return (v - vmin) / (vmax - vmin)

    def scores(self, query: str) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        q = normalize_arabic(query)
        word_s = cosine_similarity(self.word.transform([q]), self.word_x)[0]
        char_s = cosine_similarity(self.char.transform([q]), self.char_x)[0]
        fused = self.alpha * self._scale(word_s) + (1 - self.alpha) * self._scale(char_s)
        return word_s, char_s, fused

    def search(self, query: str, top_k: int = 3) -> list[Hit]:
        _, _, fused = self.scores(query)
        order = np.argsort(-fused)[:top_k]
        return [Hit(self.docs[i], float(fused[i])) for i in order]
