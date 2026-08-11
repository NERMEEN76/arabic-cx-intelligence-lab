from app.guardrails import detect_triage, redact_pii


def test_escalates_fraud_complaint():
    t = detect_triage("دي كارثة وهقدم شكوى رسمية بسبب احتيال")
    assert t.escalation is True
    assert t.sentiment == "negative"


def test_redacts_card_number():
    assert "4111111111111111" not in redact_pii("card 4111111111111111")
