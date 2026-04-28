"""
pipeline.py — Main RAG pipeline entry point for Phase 2.

Orchestrates: guardrails → retrieval → generation.
Called by the API server (Phase 3) or used directly for testing.
"""

from __future__ import annotations

import logging
import sys
import os

# Ensure project root is on the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from phase2_rag_core.guardrails import run_guardrails
from phase2_rag_core.retriever import retrieve_context
from phase2_rag_core.generator import generate_response
from phase2_rag_core.prompts import NO_RESULTS_RESPONSE

logger = logging.getLogger(__name__)


def process_query(query: str) -> dict:
    """
    Full RAG pipeline: guardrails → retrieve → generate.

    Returns:
        {
            "response": str,        # The final answer or refusal message
            "blocked": bool,        # Whether the query was blocked by guardrails
            "block_reason": str,    # "pii_detected", "advisory_query", or None
        }
    """
    logger.info(f"Processing query: '{query[:80]}...'")

    # Step 1: Run guardrails (PII → Advisory)
    guardrail_result = run_guardrails(query)
    if guardrail_result["blocked"]:
        logger.info(f"Query blocked by guardrails: {guardrail_result['reason']}")
        return {
            "response": guardrail_result["response"],
            "blocked": True,
            "block_reason": guardrail_result["reason"],
        }

    # Step 2: Retrieve relevant context from Chroma Cloud
    retrieval = retrieve_context(query)
    if not retrieval["found"]:
        logger.info("No relevant context found.")
        return {
            "response": NO_RESULTS_RESPONSE,
            "blocked": False,
            "block_reason": None,
        }

    # Step 3: Generate response via LLM
    response = generate_response(
        query=query,
        context_text=retrieval["context_text"],
        best_source_url=retrieval["best_source_url"],
        latest_date=retrieval["latest_date"],
    )

    logger.info("Response generated successfully.")
    return {
        "response": response,
        "blocked": False,
        "block_reason": None,
    }


# ---------------------------------------------------------------------------
# CLI test mode
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import logging
    from phase1_data_ingestion.config import LOG_LEVEL

    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL, logging.INFO),
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    test_queries = [
        "What is the expense ratio of HDFC Large Cap Fund?",
        "Should I invest in HDFC ELSS?",
        "My PAN is ABCDE1234F, what is the exit load?",
        "What is the minimum SIP for HDFC Focused Fund?",
    ]

    for q in test_queries:
        print(f"\n{'='*60}")
        print(f"QUERY: {q}")
        print(f"{'='*60}")
        result = process_query(q)
        print(f"BLOCKED: {result['blocked']}")
        if result["block_reason"]:
            print(f"REASON: {result['block_reason']}")
        print(f"RESPONSE:\n{result['response']}")
