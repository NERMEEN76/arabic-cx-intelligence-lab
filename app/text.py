import re
from typing import Iterable

_ARABIC_DIACRITICS = re.compile(r"[\u0617-\u061A\u064B-\u0652]")
_NON_WORD = re.compile(r"[^\w\s\u0600-\u06FF]+", re.UNICODE)
_MULTI_SPACE = re.compile(r"\s+")


def normalize_arabic(text: str) -> str:
    """Lightweight normalization suitable for Arabic CX search."""
    text = (text or "").strip().lower()
    text = _ARABIC_DIACRITICS.sub("", text)
    replacements = {
        "أ": "ا", "إ": "ا", "آ": "ا", "ى": "ي", "ؤ": "و", "ئ": "ي", "ـ": ""
    }
    for src, dst in replacements.items():
        text = text.replace(src, dst)
    text = _NON_WORD.sub(" ", text)
    return _MULTI_SPACE.sub(" ", text).strip()


def tokenize(text: str) -> list[str]:
    return [t for t in normalize_arabic(text).split() if len(t) > 1]


def join_fields(values: Iterable[str]) -> str:
    return " ".join(v for v in values if v)
