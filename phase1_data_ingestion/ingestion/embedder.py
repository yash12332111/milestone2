"""
embedder.py — BAAI/bge-large-en-v1.5 embedding wrapper via sentence-transformers.

Uses the local HuggingFace model. Automatically handles batching and normalization.
"""

from __future__ import annotations

import logging
from typing import Any

from phase1_data_ingestion.config import EMBEDDING_MODEL

logger = logging.getLogger(__name__)

_model = None

def get_model():
    """Lazily load the embedding model to avoid slow startup for non-embedding tasks."""
    global _model
    if _model is None:
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError:
            raise ImportError("sentence-transformers not installed. Run: pip install sentence-transformers")
        logger.info(f"Loading local embedding model: {EMBEDDING_MODEL} (may take a moment)...")
        _model = SentenceTransformer(EMBEDDING_MODEL)
    return _model


def embed_chunks(chunks: list[dict]) -> list[dict]:
    """
    Takes a list of chunk dicts (each with a 'text' key),
    adds an 'embedding' key (1024-dim vector), and returns the list.
    """
    if not chunks:
        return chunks

    model = get_model()
    texts = [chunk["text"] for chunk in chunks]

    logger.info(f"Embedding {len(texts)} chunks with {EMBEDDING_MODEL}...")

    try:
        # BGE models should be normalized for cosine similarity matching
        # sentence-transformers automatically handles batch sizes (default 32)
        embeddings = model.encode(texts, normalize_embeddings=True)
    except Exception as e:
        logger.error(f"Embedding failed: {e}")
        raise

    for i, chunk in enumerate(chunks):
        chunk["embedding"] = embeddings[i].tolist()

    logger.info(f"✅ Embedded {len(chunks)} chunks successfully.")
    return chunks

