"""
Central configuration for the Mutual Fund FAQ Assistant.
All environment variables, constants, and target URLs are defined here.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# LLM (Groq)
# ---------------------------------------------------------------------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
LLM_MODEL = "llama-3.3-70b-versatile"  # Groq-hosted Llama 3.3 70B
LLM_TEMPERATURE = 0.0
LLM_MAX_TOKENS = 250

# ---------------------------------------------------------------------------
# Embedding (local HuggingFace model — no API key needed)
# ---------------------------------------------------------------------------
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"

# ---------------------------------------------------------------------------
# ChromaDB (Local persistent)
# ---------------------------------------------------------------------------
CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "chroma_db"))
CHROMA_COLLECTION_NAME = "mutual_fund_facts"

# ---------------------------------------------------------------------------
# SQLite (Thread storage)
# ---------------------------------------------------------------------------
SQLITE_DB_PATH = os.getenv("SQLITE_DB_PATH", os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "threads.db"))

# ---------------------------------------------------------------------------
# Scraping
# ---------------------------------------------------------------------------
TARGET_URLS = [
    {
        "url": "https://groww.in/mutual-funds/hdfc-large-cap-fund-direct-growth",
        "scheme_name": "HDFC Large Cap Fund",
        "category": "Large Cap",
    },
    {
        "url": "https://groww.in/mutual-funds/hdfc-elss-tax-saver-fund-direct-plan-growth",
        "scheme_name": "HDFC ELSS Tax Saver Fund",
        "category": "ELSS",
    },
    {
        "url": "https://groww.in/mutual-funds/hdfc-focused-fund-direct-growth",
        "scheme_name": "HDFC Focused Fund",
        "category": "Focused",
    },
    {
        "url": "https://groww.in/mutual-funds/hdfc-equity-fund-direct-growth",
        "scheme_name": "HDFC Equity Fund",
        "category": "Multi Cap",
    },
    {
        "url": "https://groww.in/mutual-funds/hdfc-mid-cap-fund-direct-growth",
        "scheme_name": "HDFC Mid-Cap Opportunities Fund",
        "category": "Mid Cap",
    },
]

# Scraping behaviour
SCRAPE_DELAY_SECONDS = 2  # Delay between URL requests
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
]

# ---------------------------------------------------------------------------
# Chunking
# ---------------------------------------------------------------------------
CHUNK_MAX_TOKENS = 500
CHUNK_MIN_TOKENS = 30
CHUNK_OVERLAP_SENTENCES = 1

# ---------------------------------------------------------------------------
# Retriever
# ---------------------------------------------------------------------------
RETRIEVER_TOP_K = 5
RETRIEVER_DISTANCE_THRESHOLD = 0.75

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
