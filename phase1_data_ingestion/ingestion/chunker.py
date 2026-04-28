"""
chunker.py — Section-aware text chunking for scraped mutual fund data.

Rules (from chunking_embedding_architecture.md):
- Each section from the scraper becomes one chunk (if under max_tokens).
- Sections exceeding 500 tokens are split by sentence boundary with 1-sentence overlap.
- Sections under 30 tokens are merged with the next section.
- Deterministic IDs ensure daily upserts overwrite rather than duplicate.
"""

from __future__ import annotations

import hashlib
import logging
import re
from datetime import datetime, timezone, timedelta

from phase1_data_ingestion.config import CHUNK_MAX_TOKENS, CHUNK_MIN_TOKENS, CHUNK_OVERLAP_SENTENCES

logger = logging.getLogger(__name__)

IST = timezone(timedelta(hours=5, minutes=30))


# ---------------------------------------------------------------------------
# Token counting
# ---------------------------------------------------------------------------
def _count_tokens(text: str) -> int:
    """Use tiktoken if available, else word-based estimate."""
    try:
        import tiktoken
        enc = tiktoken.encoding_for_model("gpt-4o-mini")
        return len(enc.encode(text))
    except ImportError:
        # ~1 token per 0.75 words
        return int(len(text.split()) / 0.75)


# ---------------------------------------------------------------------------
# Sentence splitting
# ---------------------------------------------------------------------------
def _sent_tokenize(text: str) -> list[str]:
    """Use nltk if available, else regex fallback."""
    try:
        import nltk
        nltk.download("punkt_tab", quiet=True)
        return nltk.sent_tokenize(text)
    except ImportError:
        sentences = re.split(r"(?<=[.!?])\s+", text)
        return [s.strip() for s in sentences if s.strip()]


# ---------------------------------------------------------------------------
# Deterministic ID
# ---------------------------------------------------------------------------
def _generate_chunk_id(source_url: str, section_title: str, chunk_index: int) -> str:
    """Same URL + section + index always produces the same ID."""
    raw = f"{source_url}|{section_title}|{chunk_index}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


# ---------------------------------------------------------------------------
# Core chunking
# ---------------------------------------------------------------------------
def chunk_sections(
    sections: list[dict],
    source_url: str,
    scheme_name: str,
    max_tokens: int = CHUNK_MAX_TOKENS,
    min_tokens: int = CHUNK_MIN_TOKENS,
) -> list[dict]:
    """
    Convert a list of scraped sections into metadata-enriched chunks.

    Returns list of dicts each with: id, text, metadata.
    """
    raw_chunks: list[dict] = []
    buffer_text = ""
    buffer_title = ""

    for section in sections:
        text = section["content"]
        title = section["title"]
        token_count = _count_tokens(text)

        # Case 1: fits within limit
        if token_count <= max_tokens:
            combined = (buffer_text + " " + text).strip() if buffer_text else text
            if _count_tokens(combined) <= max_tokens:
                buffer_text = combined
                buffer_title = buffer_title or title
            else:
                if buffer_text:
                    raw_chunks.append({"title": buffer_title, "text": buffer_text})
                buffer_text = text
                buffer_title = title

        # Case 2: exceeds max — split by sentences
        else:
            if buffer_text:
                raw_chunks.append({"title": buffer_title, "text": buffer_text})
                buffer_text = ""
                buffer_title = ""

            sentences = _sent_tokenize(text)
            current_chunk_sents: list[str] = []
            current_tokens = 0

            for sentence in sentences:
                s_tokens = _count_tokens(sentence)
                if current_tokens + s_tokens > max_tokens and current_chunk_sents:
                    raw_chunks.append({
                        "title": title,
                        "text": " ".join(current_chunk_sents)
                    })
                    # Overlap: keep last N sentences
                    overlap = current_chunk_sents[-CHUNK_OVERLAP_SENTENCES:]
                    current_chunk_sents = list(overlap)
                    current_tokens = sum(_count_tokens(s) for s in current_chunk_sents)

                current_chunk_sents.append(sentence)
                current_tokens += s_tokens

            if current_chunk_sents:
                raw_chunks.append({
                    "title": title,
                    "text": " ".join(current_chunk_sents)
                })

    # Flush remaining buffer
    if buffer_text:
        raw_chunks.append({"title": buffer_title, "text": buffer_text})

    # Filter empties
    raw_chunks = [c for c in raw_chunks if _count_tokens(c["text"]) >= min_tokens // 2]

    # Enrich with metadata and deterministic IDs
    enriched: list[dict] = []
    today = datetime.now(IST).strftime("%Y-%m-%d")

    for i, chunk in enumerate(raw_chunks):
        enriched.append({
            "id": _generate_chunk_id(source_url, chunk["title"], i),
            "text": chunk["text"],
            "metadata": {
                "source_url": source_url,
                "last_updated_date": today,
                "document_type": "scheme_page",
                "scheme_name": scheme_name,
                "section_title": chunk["title"],
                "chunk_index": i,
                "token_count": _count_tokens(chunk["text"]),
            },
        })

    return enriched


# ---------------------------------------------------------------------------
# Batch helper
# ---------------------------------------------------------------------------
def chunk_scraped_data(scraped_data: list[dict]) -> list[dict]:
    """Process all scraped URL results and return a flat list of chunks."""
    all_chunks: list[dict] = []

    for data in scraped_data:
        chunks = chunk_sections(
            sections=data["sections"],
            source_url=data["source_url"],
            scheme_name=data["scheme_name"],
        )
        all_chunks.extend(chunks)
        logger.info(f"  {data['scheme_name']}: {len(chunks)} chunks")

    return all_chunks
