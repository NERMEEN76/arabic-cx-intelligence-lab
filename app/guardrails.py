from dataclasses import dataclass
import re
from .text import normalize_arabic


@dataclass(frozen=True)
class Triage:
    intent: str
    sentiment: str
    escalation: bool


INTENT_RULES = {
    "refund": ["استرجاع", "استرداد", "refund", "فلوسي", "المبلغ"],
    "billing": ["فاتوره", "فاتورة", "billing", "خصم", "دفع", "بطاقه", "بطاقة"],
    "delivery": ["توصيل", "شحن", "delivery", "shipment", "وصل", "تاخر", "متاخر"],
    "account": ["حساب", "دخول", "password", "كلمه المرور", "رمز التحقق", "otp"],
    "cancellation": ["الغاء", "إلغاء", "cancel", "الغيت"],
    "technical": ["خطا", "error", "لا يعمل", "مش شغال", "تعطل", "api"],
}

NEGATIVE = ["غاضب", "زعلان", "سيئ", "سيئة", "كارثه", "كارثة", "مشكله", "مشكلة", "متاخر", "متأخر", "فشل", "مش راضي"]
URGENT = ["شكوي رسميه", "شكوى رسمية", "محامي", "احتيال", "fraud", "سرقه", "سرقة", "بياناتي", "data leak", "طوارئ"]
PII_PATTERNS = [
    re.compile(r"\b\d{16}\b"),
    re.compile(r"\b05\d{8}\b"),
    re.compile(r"\b01\d{9}\b"),
]


def detect_triage(text: str) -> Triage:
    n = normalize_arabic(text)
    intent = "general"
    best = 0
    for name, terms in INTENT_RULES.items():
        score = sum(1 for t in terms if normalize_arabic(t) in n)
        if score > best:
            intent, best = name, score
    neg = sum(1 for t in NEGATIVE if normalize_arabic(t) in n)
    sentiment = "negative" if neg else "neutral"
    escalation = any(normalize_arabic(t) in n for t in URGENT) or neg >= 2
    return Triage(intent, sentiment, escalation)


def redact_pii(text: str) -> str:
    out = text
    for p in PII_PATTERNS:
        out = p.sub("[REDACTED]", out)
    return out
