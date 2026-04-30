"""
run_pipeline.py — Orchestrates the full Phase 1 ingestion pipeline.

Called by GitHub Actions daily or manually.
Flow: scrape all URLs → chunk → embed → upsert into ChromaDB
"""

from __future__ import annotations

import json
import logging
import sys
import os

# Ensure project root is on the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from phase1_data_ingestion.config import LOG_LEVEL
from phase1_data_ingestion.scraper.scraper import scrape_all_urls
from phase1_data_ingestion.ingestion.chunker import chunk_scraped_data
from phase1_data_ingestion.ingestion.embedder import embed_chunks
from phase1_data_ingestion.ingestion.vector_store import upsert_to_chroma, cleanup_old_chunks

# Setup logging
log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "logs")
os.makedirs(log_dir, exist_ok=True)
log_file_path = os.path.join(log_dir, "scheduler.log")

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(log_file_path, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


def run_ingestion_pipeline() -> int:
    """
    Full pipeline: scrape → chunk → embed → upsert.
    Returns the number of active chunks in the vector store.
    Raises RuntimeError on unrecoverable failures so callers (e.g. the API
    endpoint or startup background thread) can handle them without exiting.
    """
    logger.info("=" * 60)
    logger.info("STARTING INGESTION PIPELINE")
    logger.info("=" * 60)

    # Step 1: Scrape all target URLs
    logger.info("Step 1/5: Scraping target URLs...")
    scraped_data = scrape_all_urls()

    if not scraped_data:
        raise RuntimeError("No data scraped — pipeline aborted.")

    logger.info(f"Scraped {len(scraped_data)} URLs successfully.")

    # Save raw scrape to disk for debugging/inspection
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data")
    os.makedirs(data_dir, exist_ok=True)
    raw_path = os.path.join(data_dir, "scraped_data.json")
    with open(raw_path, "w", encoding="utf-8") as f:
        json.dump(scraped_data, f, indent=4, ensure_ascii=False)
    logger.info(f"Saved raw scraped data to {raw_path}")

    # Step 2: Chunk the scraped data
    logger.info("Step 2/5: Chunking scraped data...")
    chunks = chunk_scraped_data(scraped_data)
    logger.info(f"Created {len(chunks)} chunks total.")

    if not chunks:
        raise RuntimeError("No chunks created — pipeline aborted.")

    # Step 3: Embed all chunks
    logger.info("Step 3/5: Embedding chunks...")
    embedded_chunks = embed_chunks(chunks)
    logger.info(f"Embedded {len(embedded_chunks)} chunks.")

    # Step 4: Upsert into ChromaDB
    logger.info("Step 4/5: Upserting to ChromaDB...")
    total = upsert_to_chroma(embedded_chunks)

    # Step 5: Clean up stale chunks
    logger.info("Step 5/5: Running retention policy (keeping 1 day of data)...")
    deleted = cleanup_old_chunks(days_to_keep=1)

    active = total - deleted
    logger.info("=" * 60)
    logger.info("PIPELINE COMPLETE")
    logger.info(f"Chunks upserted: {len(embedded_chunks)}")
    logger.info(f"Chunks deleted (stale): {deleted}")
    logger.info(f"Total active in vector store: {active}")
    logger.info("=" * 60)
    return active


if __name__ == "__main__":
    import sys
    try:
        run_ingestion_pipeline()
    except RuntimeError as e:
        logger.error(str(e))
        sys.exit(1)
