"""
vector_store.py — ChromaDB collection management.

Handles upserting embedded chunks and querying for retrieval.
Uses deterministic IDs so daily pipeline runs replace stale data.
"""

from __future__ import annotations

import logging
from typing import Optional
from datetime import datetime, timedelta

from phase1_data_ingestion.config import (
    CHROMA_PERSIST_DIR,
    CHROMA_COLLECTION_NAME,
)

logger = logging.getLogger(__name__)

_collection = None


def _get_collection():
    """Get or create the local persistent ChromaDB collection.

    Caches the collection globally so the client is only initialised once per process.
    """
    global _collection
    if _collection is not None:
        return _collection

    try:
        import chromadb
    except ImportError:
        raise ImportError("chromadb not installed. Run: pip install chromadb")

    import os
    from chromadb.utils import embedding_functions
    os.makedirs(CHROMA_PERSIST_DIR, exist_ok=True)
    logger.info(f"Opening local ChromaDB at {CHROMA_PERSIST_DIR} (one-time)...")
    client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
    # Use ChromaDB's built-in ONNX embedding (all-MiniLM-L6-v2, ~50MB, no PyTorch)
    ef = embedding_functions.DefaultEmbeddingFunction()
    _collection = client.get_or_create_collection(
        name=CHROMA_COLLECTION_NAME,
        embedding_function=ef,
        metadata={"hnsw:space": "cosine"},
    )
    logger.info("✅ Local ChromaDB collection ready.")
    return _collection


def upsert_to_chroma(chunks: list[dict]) -> int:
    """
    Upsert embedded chunks into ChromaDB.

    Each chunk dict must have: id, text, embedding, metadata.
    Returns the total count in the collection after upsert.
    """
    if not chunks:
        logger.warning("No chunks to upsert.")
        return 0

    collection = _get_collection()

    collection.upsert(
        ids=[chunk["id"] for chunk in chunks],
        documents=[chunk["text"] for chunk in chunks],
        metadatas=[chunk["metadata"] for chunk in chunks],
        # No embeddings — ChromaDB computes them via its built-in ONNX function
    )

    total = collection.count()
    logger.info(f"✅ Upserted {len(chunks)} chunks. Collection total: {total}")
    return total


def query_collection(
    query_text: str,
    n_results: int = 5,
    distance_threshold: Optional[float] = None,
) -> list[dict]:
    """
    Query the vector store for the most similar chunks.

    Returns list of dicts with keys: document, metadata, distance.
    Filters out results above distance_threshold if provided.
    """
    collection = _get_collection()

    results = collection.query(
        query_texts=[query_text],
        n_results=n_results,
        include=["documents", "metadatas", "distances"],
    )

    matched: list[dict] = []
    for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        if distance_threshold and dist > distance_threshold:
            continue
        matched.append({
            "document": doc,
            "metadata": meta,
            "distance": dist,
        })

    return matched


def get_collection_count() -> int:
    """Return the total number of chunks in the collection."""
    collection = _get_collection()
    return collection.count()

def cleanup_old_chunks(days_to_keep: int = 1) -> int:
    """
    Deletes chunks from ChromaDB where the 'last_updated_date' is older than `days_to_keep` days from today.
    Returns the number of deleted records.
    """
    collection = _get_collection()
    cutoff_date = (datetime.now() - timedelta(days=days_to_keep)).strftime("%Y-%m-%d")
    logger.info(f"Scanning for data older than {cutoff_date} to clean up...")

    # Fetch metadata for all documents to compare dates
    # Since ChromaDB's where-clause $lt doesn't reliably do lexigraphical string compares across all backend versions,
    # we filter in-memory with the IDs.
    results = collection.get(include=["metadatas"])
    
    if not results or not results.get("ids"):
        return 0

    ids_to_delete = []
    for id_, meta in zip(results["ids"], results["metadatas"]):
        if meta and "last_updated_date" in meta:
            if str(meta["last_updated_date"]) < cutoff_date:
                ids_to_delete.append(id_)
                
    if ids_to_delete:
        collection.delete(ids=ids_to_delete)
        logger.info(f"🗑️ Deleted {len(ids_to_delete)} stale chunks.")
    else:
        logger.info("✔️ No stale chunks found. Retention policy met.")

    return len(ids_to_delete)
