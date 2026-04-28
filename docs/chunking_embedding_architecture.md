# Chunking & Embedding Architecture — Detailed Design

This document provides the detailed technical design for how mutual fund data flows from raw scraped text into queryable vectors inside ChromaDB.

> **Refer to:** [architecture.md](file:///Users/eslavathyaswanthvenkatasai/M-2/docs/architecture.md) for the overall system design.

---

## 1. Pipeline Overview

```
Scraped Data (per URL)           Chunking              Embedding               Vector Store
┌──────────────────┐      ┌──────────────────┐    ┌─────────────────┐     ┌──────────────┐
│  Raw sections:   │      │                  │    │                 │     │              │
│  - Basic Info    │─────▶│  Section-Aware   │───▶│  OpenAI API     │────▶│   ChromaDB   │
│  - Expense/Loads │      │  Chunker         │    │  text-embedding │     │   Upsert     │
│  - Holdings etc. │      │                  │    │  -3-small       │     │              │
└──────────────────┘      └──────────────────┘    └─────────────────┘     └──────────────┘
                                 │                        │                       │
                          Metadata attached         1536-dim vector         Deterministic
                          to every chunk            per chunk              ID per chunk
```

---

## 2. Input: What the Chunker Receives

The Scraping Service (`backend/scraper/`) outputs a structured dictionary per URL:

```python
{
  "scheme_name": "HDFC Large Cap Fund",
  "source_url": "https://groww.in/mutual-funds/hdfc-large-cap-fund-direct-growth",
  "scraped_at": "2026-04-22T09:15:00+05:30",
  "sections": [
    {
      "title": "Basic Info",
      "content": "Fund Name: HDFC Large Cap Fund. Category: Large Cap. NAV: ₹923.45. AUM: ₹35,280 Cr. Fund Manager: Roshi Jain. Benchmark: NIFTY 100 TRI. Riskometer: Very High."
    },
    {
      "title": "Expense & Loads",
      "content": "Expense Ratio: 1.07%. Exit Load: 1% if redeemed within 1 year. No entry load."
    },
    {
      "title": "Investment Details",
      "content": "Minimum SIP: ₹500. Minimum Lumpsum: ₹5,000. SIP Date Options: 1st, 5th, 10th, 15th, 20th, 25th."
    },
    {
      "title": "Top Holdings",
      "content": "ICICI Bank - 9.8%. HDFC Bank - 8.5%. Infosys - 7.2%. ..."
    },
    {
      "title": "ELSS / Lock-In",
      "content": "Lock-in Period: N/A (only ELSS funds have 3-year lock-in)."
    }
  ]
}
```

Each URL produces **~4-8 sections** depending on the page structure.

---

## 3. Chunking Strategy (`backend/ingestion/chunker.py`)

### 3A. Design Philosophy

> Mutual fund facts are **short and self-contained** (expense ratio, SIP amount, etc.). The chunking strategy prioritizes **keeping related facts together** rather than splitting arbitrarily by token count.

### 3B. Chunking Rules

| Rule                        | Detail                                                                 |
| --------------------------- | ---------------------------------------------------------------------- |
| **Primary split**           | Each section from the scraper becomes **one chunk**                     |
| **Max chunk size**          | 500 tokens. If a section exceeds this, split by sentence boundary.     |
| **Min chunk size**          | 30 tokens. If a section is shorter, merge it with the next section.    |
| **Overlap**                 | 1 sentence overlap between sub-chunks (only when a section is split).  |
| **Sentence splitter**       | Use `nltk.sent_tokenize()` or regex-based sentence boundary detection. |
| **Token counter**           | Use `tiktoken` with encoding `cl100k_base` (matches OpenAI models).    |

### 3C. Chunking Algorithm (Pseudocode)

```python
def chunk_sections(sections: list[dict], max_tokens=500, min_tokens=30) -> list[dict]:
    chunks = []
    buffer = ""
    buffer_title = ""

    for section in sections:
        text = section["content"]
        title = section["title"]
        token_count = count_tokens(text)

        # Case 1: Section fits within limit
        if token_count <= max_tokens:
            if count_tokens(buffer + text) <= max_tokens:
                # Merge small sections together
                buffer += f" {text}"
                buffer_title = buffer_title or title
            else:
                # Flush buffer, start new
                if buffer:
                    chunks.append({"title": buffer_title, "text": buffer.strip()})
                buffer = text
                buffer_title = title

        # Case 2: Section exceeds max — split by sentences
        else:
            if buffer:
                chunks.append({"title": buffer_title, "text": buffer.strip()})
                buffer = ""
                buffer_title = ""

            sentences = sent_tokenize(text)
            current_chunk = []
            current_tokens = 0

            for i, sentence in enumerate(sentences):
                s_tokens = count_tokens(sentence)
                if current_tokens + s_tokens > max_tokens and current_chunk:
                    chunks.append({
                        "title": title,
                        "text": " ".join(current_chunk)
                    })
                    # Overlap: keep last sentence
                    current_chunk = [current_chunk[-1]] if current_chunk else []
                    current_tokens = count_tokens(current_chunk[0]) if current_chunk else 0

                current_chunk.append(sentence)
                current_tokens += s_tokens

            if current_chunk:
                chunks.append({"title": title, "text": " ".join(current_chunk)})

    # Flush remaining buffer
    if buffer:
        chunks.append({"title": buffer_title, "text": buffer.strip()})

    return chunks
```

### 3D. Metadata Attached to Every Chunk

After chunking, the system attaches full metadata:

```python
{
  "id":                "a3f8c2...",                          # Deterministic hash
  "text":              "Expense Ratio: 1.07%. Exit Load...", # The chunk content
  "metadata": {
    "source_url":      "https://groww.in/mutual-funds/...",
    "last_updated_date": "2026-04-22",                       # Date of scrape
    "document_type":   "scheme_page",
    "scheme_name":     "HDFC Large Cap Fund",
    "section_title":   "Expense & Loads",
    "chunk_index":     0,                                    # Position if section was split
    "token_count":     47                                    # For debugging
  }
}
```

### 3E. Expected Chunk Volume

| Source                         | Est. Sections | Est. Chunks per URL | Total (5 URLs) |
| ------------------------------ | ------------- | ------------------- | -------------- |
| Basic Info                     | 1             | 1                   | 5              |
| Expense & Loads                | 1             | 1                   | 5              |
| Investment Details             | 1             | 1                   | 5              |
| Top Holdings                   | 1             | 1-2 (may split)     | 5-10           |
| Category-Specific (ELSS etc.)  | 0-1           | 0-1                 | 0-5            |
| **Total**                      |               |                     | **20-30 chunks** |

---

## 4. Embedding Strategy (`backend/ingestion/embedder.py`)

### 4A. Model Selection

| Property        | Value                                                 |
| --------------- | ----------------------------------------------------- |
| Model           | `BAAI/bge-large-en-v1.5`                              |
| Provider        | HuggingFace (via `sentence-transformers`)             |
| Dimensions      | 1024                                                  |
| Max Input       | 512 tokens                                            |
| Cost            | Open-source / Free to run locally                     |
| Why this model  | Highly optimized for cosine similarity search, state-of-the-art for factual retrieval |

### 4B. Embedding Process

```python
from sentence_transformers import SentenceTransformer

def embed_chunks(chunks: list[dict]) -> list[dict]:
    """
    Takes chunked documents, returns the same list enriched with 'embedding' field.
    Uses sentence-transformers which handles batching automatically.
    """
    texts = [chunk["text"] for chunk in chunks]

    model = SentenceTransformer("BAAI/bge-large-en-v1.5")
    
    # BGE models should be normalized for cosine similarity matching
    embeddings = model.encode(texts, normalize_embeddings=True)

    for i, chunk in enumerate(chunks):
        chunk["embedding"] = embeddings[i].tolist()  # 1024-dim list

    return chunks
```

### 4C. Embedding Design Decisions

| Decision                        | Rationale                                                    |
| ------------------------------- | ------------------------------------------------------------ |
| **Batch automatically via library** | `sentence-transformers` automatically batches inputs. Default batch size (32) is perfectly fine for our corpus. |
| **Embed raw chunk text only**    | Do NOT embed metadata. Metadata is used for filtering, not similarity matching. |
| **No prefix for document encoding**| `bge-large-en-v1.5` requires a prefix (`Represent this sentence for searching relevant passages: `) for *queries*, but NOT for the document chunks being indexed. |
| **Re-embed on every run**        | Since the daily pipeline upserts with deterministic IDs, re-embedding ensures data freshness without stale vectors. |

### 4D. Cost Estimate (Daily Run)

| Metric                 | Value                                         |
| ---------------------- | --------------------------------------------- |
| Chunks per run         | ~25                                           |
| Avg tokens per chunk   | ~80                                           |
| Total tokens per run   | ~2,000                                        |
| Cost per run           | ~$0.00004 (effectively free)                  |
| Cost per month (30d)   | ~$0.001                                       |

---

## 5. Vector Storage & Upsert (`backend/ingestion/vector_store.py`)

### 5A. ChromaDB Configuration

| Property             | Value                                                  |
| -------------------- | ------------------------------------------------------ |
| Client type          | `HttpClient` (hosted cloud database)                   |
| Hosted endpoint      | `api.trychroma.com`                                    |
| Collection name      | `mutual_fund_facts`                                    |
| Distance metric      | Cosine similarity (default)                            |
| Max collection size   | No hard limit needed (~30 vectors)                    |

### 5B. Deterministic ID Generation

To avoid duplicates on daily re-runs, each chunk gets a **deterministic ID**:

```python
import hashlib

def generate_chunk_id(source_url: str, section_title: str, chunk_index: int) -> str:
    """
    Same URL + section + index always produces the same ID.
    Daily upserts overwrite existing data transparently.
    """
    raw = f"{source_url}|{section_title}|{chunk_index}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]
```

**Example IDs:**
| source_url (truncated)     | section_title    | chunk_index | Generated ID     |
| -------------------------- | ---------------- | ----------- | ---------------- |
| `.../hdfc-large-cap-fund...` | Basic Info       | 0           | `a3f8c2b901e4d7f2` |
| `.../hdfc-large-cap-fund...` | Expense & Loads  | 0           | `7b2e1d9f03c8a5b1` |
| `.../hdfc-elss-tax-saver...` | Basic Info       | 0           | `e9d4f6a2c7b3e8d0` |

### 5C. Upsert Logic

```python
import chromadb
import os

def upsert_to_chroma(chunks: list[dict]):
    client = chromadb.HttpClient(
        host=os.getenv("CHROMA_CLOUD_ENDPOINT", "api.trychroma.com"),
        ssl=True,
        headers={"X-Chroma-Token": os.getenv("CHROMA_CLOUD_API_KEY")}
    )
    
    collection = client.get_or_create_collection(
        name="mutual_fund_facts",
        metadata={"hnsw:space": "cosine"}
    )

    collection.upsert(
        ids=[chunk["id"] for chunk in chunks],
        embeddings=[chunk["embedding"] for chunk in chunks],
        documents=[chunk["text"] for chunk in chunks],
        metadatas=[chunk["metadata"] for chunk in chunks]
    )

    print(f"Upserted {len(chunks)} chunks. Collection total: {collection.count()}")
```

**Why upsert (not add)?**
- `upsert` = if ID exists, **overwrite**. If new, **insert**.
- This means the daily scheduled run replaces yesterday's data with today's data seamlessly.
- No need for manual cleanup, deduplication, or deletion logic.

### 5D. Querying at Retrieval Time (Preview)

At retrieval time (Phase 2), the vector store is queried like this:

```python
results = collection.query(
    query_embeddings=[user_query_embedding],
    n_results=5,
    include=["documents", "metadatas", "distances"]
)

# Filter out low-relevance results
relevant = [
    (doc, meta, dist)
    for doc, meta, dist in zip(results["documents"][0], results["metadatas"][0], results["distances"][0])
    if dist < 0.75  # Cosine distance threshold
]
```

---

## 6. Full Pipeline Orchestration (`backend/ingestion/run_pipeline.py`)

```python
"""
Entry point for the ingestion pipeline.
Called by GitHub Actions daily or manually via workflow_dispatch.
"""

def run_ingestion_pipeline():
    urls = load_target_urls()          # From config.py
    all_chunks = []

    for url in urls:
        try:
            # Step 1: Scrape
            raw_data = scrape_url(url)

            # Step 2: Chunk
            chunks = chunk_sections(raw_data["sections"])

            # Step 3: Attach metadata
            for i, chunk in enumerate(chunks):
                chunk["id"] = generate_chunk_id(url, chunk["title"], i)
                chunk["metadata"] = {
                    "source_url": url,
                    "last_updated_date": datetime.now().strftime("%Y-%m-%d"),
                    "document_type": "scheme_page",
                    "scheme_name": raw_data["scheme_name"],
                    "section_title": chunk["title"],
                    "chunk_index": i,
                    "token_count": count_tokens(chunk["text"])
                }

            all_chunks.extend(chunks)
            logger.info(f"✅ {raw_data['scheme_name']}: {len(chunks)} chunks")

        except Exception as e:
            logger.error(f"❌ Failed to process {url}: {e}")
            continue  # Don't block other URLs

    # Step 4: Batch embed all chunks
    all_chunks = embed_chunks(all_chunks)

    # Step 5: Upsert to ChromaDB
    upsert_to_chroma(all_chunks)

    logger.info(f"Pipeline complete. Total chunks: {len(all_chunks)}")

if __name__ == "__main__":
    run_ingestion_pipeline()
```

---

## 7. Validation & Testing

| Test Case                                      | Expected Result                                    |
| ---------------------------------------------- | -------------------------------------------------- |
| Run pipeline for 1 URL                         | ~4-5 chunks upserted with correct metadata         |
| Run pipeline for all 5 URLs                    | ~20-30 chunks total in collection                  |
| Query "expense ratio HDFC Large Cap"           | Returns chunk containing "1.07%" with correct URL  |
| Re-run pipeline (same day)                     | Collection count unchanged (upsert overwrites)     |
| One URL is unreachable                         | Pipeline continues for other 4 URLs, logs error    |
| Section with >500 tokens                       | Correctly split with 1-sentence overlap            |
| Section with <30 tokens                        | Merged with adjacent section                       |
