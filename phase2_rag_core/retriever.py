"""
retriever.py — Similarity search against Chroma Cloud + query embedding.

Embeds the user query using the same BGE-Large model,
searches ChromaDB for the top-K nearest chunks,
and filters out low-relevance results.
"""

from __future__ import annotations

import logging
from typing import Optional

from phase1_data_ingestion.config import RETRIEVER_TOP_K, RETRIEVER_DISTANCE_THRESHOLD
from phase1_data_ingestion.ingestion.embedder import get_model
from phase1_data_ingestion.ingestion.vector_store import query_collection
from phase2_rag_core.prompts import NO_RESULTS_RESPONSE

logger = logging.getLogger(__name__)


def retrieve_context(query: str) -> dict:
    """
    Embed the user query and retrieve the most relevant chunks from ChromaDB.

    Returns:
        {
            "found": bool,
            "chunks": list[dict],       # each: {document, metadata, distance}
            "context_text": str,         # formatted text block for the LLM prompt
            "best_source_url": str,      # URL from the top-scoring chunk
            "latest_date": str,          # most recent last_updated_date
        }
    """
    model = get_model()

    # BGE models need "Represent this sentence..." prefix for QUERIES (not documents)
    prefixed_query = f"Represent this sentence for searching relevant passages: {query}"
    query_embedding = model.encode(prefixed_query, normalize_embeddings=True).tolist()

    logger.info(f"Querying ChromaDB for: '{query[:80]}...'")

    results = query_collection(
        query_embedding=query_embedding,
        n_results=RETRIEVER_TOP_K,
        distance_threshold=RETRIEVER_DISTANCE_THRESHOLD,
    )

    if not results:
        logger.info("No relevant chunks found above threshold.")
        return {
            "found": False,
            "chunks": [],
            "context_text": "",
            "best_source_url": "",
            "latest_date": "",
            "no_results_response": NO_RESULTS_RESPONSE,
        }

    # Sort by distance ascending (most relevant first), then by date descending
    results.sort(key=lambda r: (r["distance"], -_date_sort_key(r["metadata"].get("last_updated_date", ""))))

    # Build context text for the LLM prompt
    context_parts = []
    for i, r in enumerate(results):
        meta = r["metadata"]
        context_parts.append(
            f"[Source {i+1}: {meta.get('scheme_name', 'Unknown')} — {meta.get('section_title', 'Unknown')}]\n"
            f"{r['document']}"
        )

    context_text = "\n\n".join(context_parts)

    # Pick best citation (top-scoring chunk)
    best_source_url = results[0]["metadata"].get("source_url", "")

    # Pick latest date across all retrieved chunks
    dates = [r["metadata"].get("last_updated_date", "") for r in results]
    latest_date = max(dates) if dates else ""

    logger.info(f"Retrieved {len(results)} relevant chunks. Best source: {best_source_url}")

    return {
        "found": True,
        "chunks": results,
        "context_text": context_text,
        "best_source_url": best_source_url,
        "latest_date": latest_date,
    }


def _date_sort_key(date_str: str) -> int:
    """Convert YYYY-MM-DD to sortable int. Returns 0 if unparseable."""
    try:
        return int(date_str.replace("-", ""))
    except (ValueError, AttributeError):
        return 0
