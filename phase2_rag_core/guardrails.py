"""
guardrails.py — PII scanner + Advisory intent classifier.

Execution order: PII check first → Advisory check second → proceed to retrieval.
Both guardrails return a dict with {blocked, reason, response} keys.
"""

from __future__ import annotations

import re
import logging

from phase2_rag_core.prompts import PII_REFUSAL, ADVISORY_REFUSAL

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# PII Patterns
# ---------------------------------------------------------------------------
PII_PATTERNS = {
    "PAN": r"[A-Z]{5}[0-9]{4}[A-Z]{1}",
    "Aadhaar": r"\b\d{4}\s?\d{4}\s?\d{4}\b",
    "Phone": r"\b[6-9]\d{9}\b",
    "Email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
    "Account": r"\b\d{9,18}\b",
}

# ---------------------------------------------------------------------------
# Advisory Intent Keywords
# ---------------------------------------------------------------------------
ADVISORY_KEYWORDS = [
    "should i invest",
    "should i buy",
    "should i sell",
    "is it good",
    "is it safe",
    "is it worth",
    "which is better",
    "which fund is best",
    "recommend",
    "suggest",
    "compare returns",
    "compare performance",
    "predict",
    "will it go up",
    "will it go down",
    "future returns",
    "expected returns",
    "good investment",
    "bad investment",
    "buy or sell",
    "hold or sell",
    "invest in",
    "worth investing",
    "best fund",
    "worst fund",
    "better option",
    "better choice",
    "outperform",
    "underperform",
    "beat the market",
    "market prediction",
    "guaranteed returns",
]


# ---------------------------------------------------------------------------
# Guardrail Functions
# ---------------------------------------------------------------------------
def check_pii(query: str) -> dict:
    """
    Scan the user query for personally identifiable information.
    Returns a guardrail result dict.
    """
    for pii_type, pattern in PII_PATTERNS.items():
        if re.search(pattern, query):
            logger.warning(f"PII detected ({pii_type}) in query.")
            return {
                "blocked": True,
                "reason": "pii_detected",
                "response": PII_REFUSAL,
            }
    return {"blocked": False, "reason": None, "response": None}


def check_advisory_intent(query: str) -> dict:
    """
    Check if the user query is requesting investment advice.
    Uses keyword matching on a curated list of advisory phrases.
    """
    query_lower = query.lower()
    for keyword in ADVISORY_KEYWORDS:
        if keyword in query_lower:
            logger.warning(f"Advisory intent detected (matched: '{keyword}').")
            return {
                "blocked": True,
                "reason": "advisory_query",
                "response": ADVISORY_REFUSAL,
            }
    return {"blocked": False, "reason": None, "response": None}


def run_guardrails(query: str) -> dict:
    """
    Execute all guardrails in order: PII → Advisory.
    Returns the first blocking result, or a pass-through if none triggered.
    """
    # Step 1: PII check
    pii_result = check_pii(query)
    if pii_result["blocked"]:
        return pii_result

    # Step 2: Advisory intent check
    advisory_result = check_advisory_intent(query)
    if advisory_result["blocked"]:
        return advisory_result

    # All clear
    return {"blocked": False, "reason": None, "response": None}
