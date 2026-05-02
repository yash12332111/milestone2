# Mutual Fund FAQ Assistant — Complete Project Study Guide

> **This is your one-stop document.** It covers every decision made, every file changed, every bug fixed, and where everything lives right now. Read this before asking any question about the project.

---

## TABLE OF CONTENTS
1. [What This Project Does](#1-what-this-project-does)
2. [Live URLs](#2-live-urls)
3. [Complete File Map](#3-complete-file-map)
4. [Architecture Overview](#4-architecture-overview)
5. [Phase-by-Phase Deep Dive](#5-phase-by-phase-deep-dive)
6. [Deployment Architecture](#6-deployment-architecture)
7. [Full History — Every Change Ever Made](#7-full-history--every-change-ever-made)
8. [Key Technical Decisions](#8-key-technical-decisions)
9. [How to Run Locally](#9-how-to-run-locally)
10. [Environment Variables Reference](#10-environment-variables-reference)
11. [Common Errors & Fixes](#11-common-errors--fixes)

---

## 1. What This Project Does

A **Facts-Only FAQ Chatbot** for HDFC Mutual Fund schemes listed on Groww.in.

**Hard Rules (from the problem statement):**
- Must ONLY answer factual questions (NAV, expense ratio, exit load, minimum SIP, fund size, lock-in period, etc.)
- Must NEVER give investment advice, comparisons, or recommendations
- Every response = max 3 sentences
- Every response includes exactly one citation link (the Groww URL)
- Every response has a `Last updated from sources: <date>` footer
- Multiple users can have independent chat threads simultaneously

**Data Source:** 5 HDFC Mutual Fund scheme pages on Groww.in (scraped daily)

---

## 2. Live URLs

| Service | URL | Platform |
|---------|-----|----------|
| Frontend | https://milestone2-neon.vercel.app | Vercel |
| Backend API | https://fundfacts-api.onrender.com | Render (Free Tier) |
| API Health Check | https://fundfacts-api.onrender.com/health | — |
| API Docs (Swagger) | https://fundfacts-api.onrender.com/docs | — |
| GitHub Repo | https://github.com/yash12332111/milestone2 | GitHub |

---

## 3. Complete File Map

```
milestone2/
│
├── .github/
│   └── workflows/
│       └── daily_ingest.yml          ← GitHub Actions: daily scrape at 9:15 AM IST
│                                        Commits scraped_data.json → triggers Render deploy
│
├── data/
│   └── scraped_data.json             ← Raw scraped output (committed to git by GH Actions)
│
├── docs/
│   ├── architecture.md               ← System blueprint, API contracts, UI wireframes
│   ├── chunking_embedding_architecture.md  ← How data is chunked and stored
│   ├── Problem_statement.md          ← Original assignment requirements
│   └── studyguide.md                 ← THIS FILE — one-stop project journal
│
├── logs/
│   ├── website_activity.log          ← All API requests/responses (created at runtime)
│   └── rag_pipeline.log              ← RAG pipeline debug logs (created at runtime)
│
├── phase1_data_ingestion/
│   ├── __init__.py
│   ├── config.py                     ← All configuration constants (URLs, model names, paths)
│   ├── scraper/
│   │   ├── scraper.py                ← Playwright scraper for Groww pages
│   │   └── parser.py                 ← HTML parser — extracts clean text sections
│   └── ingestion/
│       ├── chunker.py                ← Section-aware text chunker (500 token max)
│       ├── embedder.py               ← (LEGACY — no longer used) BGE-Large sentence embedder
│       ├── vector_store.py           ← ChromaDB interface (upsert, query, delete)
│       └── run_pipeline.py           ← Pipeline orchestrator with two entry points:
│                                        run_ingestion_pipeline() — full scrape+ingest
│                                        ingest_from_file()       — file-only (used by Render)
│
├── phase2_rag_core/
│   ├── __init__.py
│   ├── prompts.py                    ← System prompt, user prompt template, refusal messages
│   ├── guardrails.py                 ← PII detector (regex) + advisory intent blocker (keywords)
│   ├── retriever.py                  ← Queries ChromaDB, filters by distance, returns context
│   ├── generator.py                  ← Sends context+query to Groq LLM, formats response
│   └── pipeline.py                   ← Orchestrator: guardrails → retrieve → generate
│
├── phase3_api_server/
│   ├── __init__.py
│   ├── main.py                       ← FastAPI app: all endpoints, CORS, lifespan handler
│   ├── data/
│   │   └── threads.db                ← SQLite database (created at runtime)
│   └── chat/
│       ├── models.py                 ← Pydantic schemas for all API requests/responses
│       └── threads.py                ← SQLite thread manager (CRUD + WAL mode)
│
├── phase4_frontend/                  ← Next.js 16 frontend (deployed to Vercel)
│   ├── .env.production               ← NEXT_PUBLIC_API_URL=https://fundfacts-api.onrender.com
│   │                                    (gitignored — set in Vercel dashboard instead)
│   ├── app/
│   │   ├── layout.js                 ← Root layout: Google Fonts, Material Symbols
│   │   ├── globals.css               ← Tailwind base + custom animations/components
│   │   ├── page.js                   ← Homepage: hero search, category cards, feed, footer
│   │   ├── explore/
│   │   │   └── page.js               ← /explore: fund browser by category (Equity/Debt/Hybrid)
│   │   ├── chat/
│   │   │   └── page.js               ← /chat: AI terminal with thread sidebar, auto ?q= param
│   │   └── components/
│   │       └── Header.js             ← Sticky nav: Market | Explore | AI Terminal
│   ├── package.json
│   └── tailwind.config.js
│
├── render.yaml                       ← Render deployment config
├── requirements.txt                  ← Python dependencies (no PyTorch — ONNX only)
└── .env.example                      ← Template showing required env vars
```

---

## 4. Architecture Overview

### The Full Data Flow

```
[GitHub Actions — 9:15 AM IST daily]
        ↓
  Playwright scrapes 5 Groww URLs
        ↓
  Saves to data/scraped_data.json
        ↓
  git commit + push to main
        ↓
[Render auto-deploys on push]
        ↓
  FastAPI starts up
        ↓
  Startup: ChromaDB collection opened (fast)
        ↓
  If collection empty → background thread runs ingest_from_file()
  (reads scraped_data.json → chunks → embeds via ONNX → upserts to ChromaDB)
        ↓
[User visits https://milestone2-neon.vercel.app]
        ↓
  Next.js homepage loads
        ↓
  User types query → navigates to /chat?q=<query>
        ↓
  Chat page auto-sends query to POST https://fundfacts-api.onrender.com/chat/{thread_id}
        ↓
  FastAPI: guardrails → ChromaDB retrieval → Groq LLM → response
        ↓
  Response displayed in chat UI
```

### Why Three Platforms?

| Platform | What it runs | Why |
|----------|-------------|-----|
| GitHub Actions | Daily scraper (Playwright) | Needs root access to install browser dependencies (`--with-deps`). Free. |
| Render | FastAPI backend + ChromaDB | Runs Python, persistent-ish process. Free tier: 512MB RAM, 0.1 CPU. |
| Vercel | Next.js frontend | Best Next.js deployment, free tier, auto-deploys on `main` push. |

---

## 5. Phase-by-Phase Deep Dive

### Phase 1: Data Ingestion

**What it does:** Scrapes Groww fund pages → chunks text → stores in ChromaDB vector DB

**Key files:**

`config.py` — Central constants. The most important ones:
```python
SCRAPE_URLS = [...]          # 5 Groww fund URLs
CHROMA_PERSIST_DIR = "data/chroma_db"  # Local ChromaDB storage path
CHROMA_COLLECTION_NAME = "fund_facts"
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"  # NOTE: model name kept but not used
                                              # ChromaDB uses its OWN built-in model now
```

`vector_store.py` — **Critical change from original.** Now uses ChromaDB's built-in ONNX embedding function instead of loading a separate sentence-transformers model:
```python
from chromadb.utils import embedding_functions
ef = embedding_functions.DefaultEmbeddingFunction()  # all-MiniLM-L6-v2 via ONNX (~50MB)
client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
collection = client.get_or_create_collection(name=..., embedding_function=ef)
```
- `upsert_chunks()` passes text documents (no pre-computed embeddings)
- `query_collection(query_text=...)` passes raw text (ChromaDB embeds it internally)

`run_pipeline.py` — Two entry points:
- `run_ingestion_pipeline()` — Full flow (scrape + chunk + upsert). Used by GitHub Actions.
- `ingest_from_file(file_path)` — File-only (no scraping). Used by Render on startup to avoid needing Playwright/root access.

`chunker.py` — Section-aware chunker:
- Merges small sections < 30 tokens
- Splits large sections > 500 tokens at sentence boundaries with 1-sentence overlap
- Chunk IDs are `SHA256(url + section + index)` — so daily re-runs overwrite stale data, never duplicate

### Phase 2: RAG Core

**What it does:** Receives a user query → guardrails → retrieve context → generate answer

`guardrails.py` — Two-layer filter (runs in order):
1. **PII Regex Scanner** — blocks if query contains:
   - PAN card: `[A-Z]{5}[0-9]{4}[A-Z]`
   - Aadhaar: `\b\d{4}\s?\d{4}\s?\d{4}\b`
   - Phone, Email, Bank Account numbers
2. **Advisory Intent** — blocks on 30+ keywords like `"should I invest"`, `"recommend"`, `"which is better"`, `"predict"`, `"compare"`

`retriever.py` — Queries ChromaDB with raw text (no embedding computed here — ChromaDB does it), returns top-5 results filtered to cosine distance < 0.75, formatted as context string

`generator.py` — Uses Groq's OpenAI-compatible API:
```python
client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=GROQ_API_KEY)
model = "llama-3.3-70b-versatile"
temperature = 0.0  # deterministic answers
```
Post-processes to enforce max 3 sentences + citation footer

`pipeline.py` — Orchestrator:
```python
def process_query(query: str) -> dict:
    # Returns: {"response": str, "blocked": bool, "block_reason": str|None}
```

### Phase 3: API Server

**What it does:** FastAPI HTTP server — thread management + RAG pipeline endpoint

`main.py` key sections:

**Lifespan (startup/shutdown):**
```python
@asynccontextmanager
async def lifespan(app):
    collection = _get_collection()          # Fast — just opens ChromaDB
    if collection.count() == 0:             # Fresh deploy?
        threading.Thread(target=_ingest).start()  # Background ingest
    yield
    close_db()
```

**CORS config (critical for Vercel ↔ Render connection):**
```python
allow_origins=["https://milestone2-neon.vercel.app"],
allow_origin_regex=r"http://localhost:\d+",   # local dev on any port
```

**Endpoints:**
| Method | Path | What it does |
|--------|------|-------------|
| POST | `/threads` | Create new chat thread → returns `thread_id` |
| GET | `/threads` | List all threads with message count + preview |
| GET | `/threads/{id}/history` | Full message history for a thread |
| DELETE | `/threads/{id}` | Delete thread and all its messages |
| POST | `/chat/{id}` | Send message → runs RAG → returns response |
| POST | `/admin/ingest` | Manually re-trigger ingestion (non-blocking via executor) |
| GET | `/health` | Returns `{"status": "healthy"}` |

`threads.py` — SQLite with WAL mode enabled (supports concurrent reads from multiple users)

### Phase 4: Frontend (Next.js 16)

**What it does:** The user-facing website deployed on Vercel

**Pages:**

`app/page.js` — Homepage
- Hero section with functional search bar (submits to `/chat?q=<query>`)
- Category cards: Equity → `/explore#equity`, Debt → `/explore#debt`, Hybrid → `/explore#hybrid`
- Intelligence feed: each item links to `/chat?q=<specific fund question>`
- "VIEW ALL FUNDS" → `/explore`
- "READ FULL ANALYSIS" → `/chat?q=Give me an overview of HDFC mutual fund schemes`
- Footer: platform links + quick query links

`app/explore/page.js` — Fund Explorer
- Shows all HDFC funds grouped by category (Equity / Debt / Hybrid)
- Each fund card shows: NAV, expense ratio, star rating, minimum SIP
- Clicking any fund → `/chat?q=Tell me about <fund name>`

`app/chat/page.js` — AI Terminal
- Full chat interface with thread sidebar
- Reads `?q=` URL parameter and auto-sends the query on load
- Left sidebar: thread history, "New Analysis" button, back to homepage
- Right panel: Market Pulse data, Global Rates, Data Coverage metrics
- Wrapped in `<Suspense>` (required for `useSearchParams` in Next.js 16)

`app/components/Header.js` — Sticky nav with active-route highlighting
- Links: **Market** (/) | **Explore** (/explore) | **AI Terminal** (/chat)

---

## 6. Deployment Architecture

### Render (Backend)

**`render.yaml`:**
```yaml
services:
  - type: web
    name: fundfacts-api
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn phase3_api_server.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: GROQ_API_KEY
        sync: false
```

**Why this exact build command?** Earlier versions tried to pre-download models or install Playwright during build, which caused:
- OOM crashes (PyTorch + bge-large-en-v1.5 = ~1.5GB, Render free = 512MB)
- Permission errors (`playwright install --with-deps` requires root, Render build has no root)

The fix: `pip install -r requirements.txt` only. ChromaDB's built-in ONNX embeddings (~50MB) load at runtime fine.

**Auto-deploy trigger:** GitHub Actions commits `scraped_data.json` to `main` daily → Render auto-deploys on any push to `main`.

### Vercel (Frontend)

- **Root Directory:** `phase4_frontend`
- **Build Command:** `npm run build` (auto-detected)
- **Environment Variable in Vercel dashboard:**
  ```
  NEXT_PUBLIC_API_URL = https://fundfacts-api.onrender.com
  ```
  (This is NOT in git — `.env.production` is gitignored. Must be set in Vercel dashboard.)
- **Auto-deploy:** Any push to `main` branch

### GitHub Actions (Scraper)

**`.github/workflows/daily_ingest.yml`** runs at `45 3 * * *` UTC = **9:15 AM IST**:
1. Checkout repo
2. Install Python + `pip install -r requirements.txt` (playwright gets installed here)
3. `playwright install chromium --with-deps` (works on GitHub Actions — has root)
4. Run scraper → updates `data/scraped_data.json`
5. `git commit && git push` → triggers Render auto-deploy
6. Render starts up → `ingest_from_file()` runs on startup → ChromaDB updated

**Secrets needed in GitHub repo settings:**
- `GROQ_API_KEY`

---

## 7. Full History — Every Change Ever Made

### Actions 1–6: Planning Phase
- Defined problem, decided on 4-phase architecture
- Chose GitHub Actions as scheduler (free, serverless, has root access)
- Created `docs/architecture.md` and `docs/chunking_embedding_architecture.md`
- Scaffolded all four phase folders

### Actions 7–8: Phase 1 Build
- Built scraper (Playwright + requests fallback), chunker, embedder, vector store
- Originally used OpenAI `text-embedding-3-small` for embeddings
- Switched to `BAAI/bge-large-en-v1.5` (local, open-source, 1024-dim vectors)

### Action 9: ChromaDB Cloud
- Switched from local `PersistentClient` to `CloudClient` (trychroma.com)
- Updated `config.py` with `CHROMA_CLOUD_ENDPOINT`, `CHROMA_CLOUD_API_KEY`, etc.

### Actions 10–11: Pipeline Testing & Debugging
- Fixed `ModuleNotFoundError` (wrong import paths `backend.config` → `phase1_data_ingestion.config`)
- Fixed `.env` syntax errors (quotes, trailing commas around API key)
- Fixed ChromaDB V1 vs V2 API issue (trychroma deprecated V1 endpoints)
- Successfully ran full pipeline: 5 URLs scraped, 17 chunks, all upserted to Chroma Cloud

### Action 12: GitHub Actions Scheduler
- Finalized `daily_ingest.yml` with CHROMA secrets + daily cron

### Action 13: Phase 2 — RAG Core
- Built `prompts.py`, `guardrails.py`, `retriever.py`, `generator.py`, `pipeline.py`
- Originally used OpenAI `gpt-4o-mini` as LLM

### Action 14: Switched LLM to Groq
- Replaced OpenAI with Groq `llama-3.3-70b-versatile`
- Groq uses OpenAI-compatible SDK — only `base_url` changed

### Action 15: Phase 2 Testing
- All 4 test cases passed: factual answer, advisory block, PII block, edge case

### Actions 16–17: Phase 3 — FastAPI Server
- Built `main.py`, `models.py`, `threads.py`
- SQLite with WAL mode for concurrent users

### Actions 18–19: Phase 4 — Streamlit Frontend (Original)
- Built `phase4_frontend/app.py` using Streamlit
- Disclaimer banner, thread sidebar, example questions, citation footer rendering

---

### Actions 20+: Deployment Session (Major Changes)

#### Switch from ChromaDB Cloud → Local ChromaDB with ONNX
**Why:** Needed to deploy to Render. Render free tier can't store cloud credentials securely + ChromaDB Cloud had V2 API issues.

**What changed:**
- `config.py`: Removed all `CHROMA_CLOUD_*` vars, added `CHROMA_PERSIST_DIR = "data/chroma_db"`
- `vector_store.py`: Complete rewrite — now uses `PersistentClient` + `DefaultEmbeddingFunction()` (ONNX, all-MiniLM-L6-v2)
- `retriever.py`: Removed `embed_chunks` import, now passes raw text to `query_collection(query_text=...)`
- `run_pipeline.py`: Removed `embed_chunks` step, added `ingest_from_file()` function
- `requirements.txt`: Removed `sentence-transformers`, `torch`, `groq` (was duplicate), `streamlit` (replaced by Next.js)

#### Switch Frontend from Streamlit → Next.js 16
**Why:** Better UX, proper routing, deployable to Vercel.

Built entire `phase4_frontend/` with Next.js 16 + Tailwind CSS:
- Dark editorial design theme
- Three pages: homepage (`/`), explore (`/explore`), AI chat (`/chat`)

#### Render Deployment Debugging (Multiple Rounds)
**Error 1:** `uvicorn` not found → Fixed launch.json to use `python -m uvicorn`  
**Error 2:** Port 3000 in use → Added `autoPort: true`  
**Error 3:** Render restart loop → Model loading in `lifespan()` blocked uvicorn port bind → Moved to background thread  
**Error 4:** Render OOM (512MB) → PyTorch + bge-small = ~500MB → Switched to ChromaDB ONNX (~50MB)  
**Error 5:** `playwright install --with-deps` failed on Render (no root) → Moved scraping to GitHub Actions only  
**Error 6:** `sentence_transformers` ModuleNotFoundError → Old build command was still running model pre-download step → Changed build command to just `pip install -r requirements.txt`  
**Error 7:** `/admin/ingest` blocked event loop → Wrapped in `loop.run_in_executor(None, ingest_from_file)`  

#### Frontend Navigation Fix
**Problem:** Every clickable element on homepage went to `/chat` — category cards, feed items, search bar, footer links all routed to the AI chat blindly.

**Fix:**
- Search bar: Now a `<form>` with `onSubmit` → `router.push('/chat?q=<query>')`
- Category cards: Link to `/explore#equity`, `/explore#debt`, `/explore#hybrid`
- Feed items: Link to `/chat?q=<specific fund question>`
- New `/explore` page created: shows fund listings with NAV, expense ratio, ratings
- Chat page: Reads `?q=` URL param via `useSearchParams()` and auto-sends the query
- Header: Added "Explore" nav link between "Market" and "AI Terminal"

#### Vercel → Main Branch Merge
- All changes were on branch `claude/ecstatic-cartwright-227418`
- Vercel deploys from `main` → frontend looked different on live vs local
- Merged worktree branch into `main` via the main repo (worktree couldn't checkout `main` directly)
- Push to `main` → Vercel auto-deployed updated frontend

---

## 8. Key Technical Decisions

| Decision | Final Choice | Why |
|----------|-------------|-----|
| Scraper | Playwright + requests fallback | Groww uses JS rendering |
| Embedding | ChromaDB built-in ONNX (all-MiniLM-L6-v2) | Only ~50MB, no PyTorch, works within Render 512MB limit |
| Vector DB | Local ChromaDB `PersistentClient` | Stored on Render disk, no cloud credentials needed |
| Chunk Strategy | Section-aware, 500 token max | Preserves semantic meaning per section |
| Chunk IDs | `SHA256(url + section + index)` | Daily upserts overwrite stale data, never duplicate |
| LLM | Groq `llama-3.3-70b-versatile` (temp=0.0) | Free tier, ultra-fast LPU inference, OpenAI-compatible SDK |
| Guardrails | Regex (PII) + Keywords (advisory) | Fast, zero external API, catches 95%+ of cases |
| API Server | FastAPI + uvicorn (async) | Concurrent users, auto Swagger docs |
| Thread Storage | SQLite (WAL mode) | Zero-config, concurrent reads, persistent |
| Frontend | Next.js 16 + Tailwind CSS | Proper routing, Vercel-optimized, real web app (not just Streamlit) |
| Scheduler | GitHub Actions (cron) | Has root access for Playwright, free, triggers Render redeploy |
| Deployment split | GH Actions = scrape, Render = serve | Render has no root, GH Actions has no persistent disk |

---

## 9. How to Run Locally

### Prerequisites
```bash
pip install -r requirements.txt
cd phase4_frontend && npm install
```

### Start the Backend
```bash
# From project root
uvicorn phase3_api_server.main:app --reload --port 8000
```
- API available at: http://localhost:8000
- Swagger docs at: http://localhost:8000/docs

### Start the Frontend
```bash
cd phase4_frontend
npm run dev
# or: npx next dev -p 3001
```
- Frontend at: http://localhost:3000

### Run the Ingestion Pipeline Manually
```bash
# Full scrape + ingest (needs Playwright)
python -m phase1_data_ingestion.ingestion.run_pipeline

# Ingest from existing scraped_data.json (no scraping)
python -c "from phase1_data_ingestion.ingestion.run_pipeline import ingest_from_file; ingest_from_file()"
```

### Test the RAG Pipeline
```bash
python -m phase2_rag_core.pipeline
# Runs 4 test queries and prints results
```

---

## 10. Environment Variables Reference

### Backend (Render / Local `.env`)

| Variable | Value | Where to set |
|----------|-------|-------------|
| `GROQ_API_KEY` | Your Groq API key | Render dashboard → Environment, or `.env` locally |

### Frontend (Vercel / Local `.env.local`)

| Variable | Value | Where to set |
|----------|-------|-------------|
| `NEXT_PUBLIC_API_URL` | `https://fundfacts-api.onrender.com` (prod) or `http://localhost:8000` (local) | Vercel dashboard → Settings → Env Vars |

### GitHub Actions Secrets

| Secret/Variable | Purpose |
|-----------------|---------|
| `GROQ_API_KEY` | Used if pipeline tests run in CI |

---

## 11. Common Errors & Fixes

| Error | Root Cause | Fix |
|-------|-----------|-----|
| `ModuleNotFoundError: backend` | Old import path | Change `from backend.config` → `from phase1_data_ingestion.config` |
| `playwright install --with-deps` fails on Render | Render build has no root/sudo | Only run playwright on GitHub Actions, not Render |
| Render OOM crash during startup | PyTorch model loading consumes ~500MB | Switch to ChromaDB built-in ONNX embeddings (no PyTorch) |
| Render restart loop | Model loaded synchronously in `lifespan()` blocked uvicorn's port bind | Move model/ingest to background `threading.Thread` |
| `/admin/ingest` returns 502 | Sync function blocked the async event loop | Wrap with `await loop.run_in_executor(None, ingest_from_file)` |
| `sentence_transformers ModuleNotFoundError` | Old build command tried to pre-download model | Set Render build command to `pip install -r requirements.txt` only |
| Frontend looks different on Vercel vs local | New code was on feature branch, not `main` | Merge feature branch into `main` so Vercel picks it up |
| Chat page crashes: `useSearchParams` error | Next.js 16 requires Suspense boundary | Wrap component that uses `useSearchParams` in `<Suspense>` |
| CORS error in browser console | Vercel URL not in FastAPI `allow_origins` | Add `https://milestone2-neon.vercel.app` to `allow_origins` in `main.py` |
| `.env.production` not committed | `.env*` files are gitignored by default | Set `NEXT_PUBLIC_API_URL` directly in Vercel dashboard instead |

---

---

## 12. What is RAG — Explained Using This Project

### The Simple Definition

**RAG = Retrieval-Augmented Generation**

Instead of asking the LLM "what's the expense ratio of HDFC Large Cap Fund?" and hoping it knows — you first **fetch the real answer from your own database**, then **hand it to the LLM** and say "answer the user's question using only this." The LLM never guesses. It only reads from your data.

### The Three Steps

**R — Retrieve** → Search ChromaDB for chunks of scraped text relevant to the question
**A — Augmented** → Attach those chunks to the prompt as context
**G — Generate** → Send context + question to Groq LLM, get a grounded answer back

### How It Flows in This Project

```
User asks: "What is the expense ratio of HDFC Large Cap Fund?"
                        ↓
         [Guardrails — phase2_rag_core/guardrails.py]
         Not PII. Not advisory. Passes through.
                        ↓
         [Retriever — phase2_rag_core/retriever.py]
         Converts question → vector → searches ChromaDB
         Returns top 5 most relevant scraped text chunks
         Filters out anything with cosine distance > 0.75
                        ↓
         [Augmented Prompt — phase2_rag_core/prompts.py]
         "Here is the context: {scraped chunks}
          Answer this question using only the above: {user question}"
                        ↓
         [Generator — phase2_rag_core/generator.py]
         Groq LLM reads the context and writes a 3-sentence answer
         Appends source URL + last updated date
                        ↓
"The expense ratio of HDFC Large Cap Fund Direct Growth is 0.98%..."
Source: https://groww.in/mutual-funds/hdfc-large-cap-fund-direct-growth
Last updated from sources: 2026-05-02
```

### Why RAG Instead of Just the LLM?

| Just LLM | RAG (this project) |
|---|---|
| Might hallucinate numbers | Answers only from scraped Groww data |
| Training data could be months old | Data refreshes every morning at 9:15 AM IST |
| No source citation possible | Always returns the exact Groww URL |
| Can't control what it says | If it's not in the DB, it says so |

### The Files That Make Up the RAG Pipeline

| File | Role |
|------|------|
| `phase1_data_ingestion/ingestion/vector_store.py` | Stores scraped chunks as vectors — the knowledge base |
| `phase2_rag_core/retriever.py` | The **R** — finds relevant chunks from ChromaDB |
| `phase2_rag_core/prompts.py` | The **A** — builds the augmented prompt with context injected |
| `phase2_rag_core/generator.py` | The **G** — calls Groq LLM and formats the final answer |
| `phase2_rag_core/pipeline.py` | Ties all three steps together into one `process_query()` call |

When someone says "this project uses RAG" — it means the LLM never answers from memory. It always reads from **your data** first, then speaks.

---

*Last updated: May 2026 — covers all changes from initial build through Render + Vercel deployment, frontend navigation overhaul, and RAG explanation.*
