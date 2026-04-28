# Mutual Fund FAQ Assistant — Detailed Phase-Wise Architecture

---

## 1. System Overview

The FAQ Assistant is a **Retrieval-Augmented Generation (RAG)** system that answers strictly factual questions about HDFC mutual fund schemes sourced from Groww. It enforces a hard boundary: **no investment advice, no opinions, no comparisons**. Every response is ≤ 3 sentences with exactly one citation link and a "last updated" footer.

### 1.1 High-Level Data Flow

```
┌─────────────┐   9:15 AM Daily    ┌──────────────────┐      Embed       ┌────────────┐
│  Scheduler   │ ──────────────────▶│  Scraping Service │ ──────────────▶ │  ChromaDB  │
│ (APScheduler)│                    │  (BeautifulSoup)  │   + Upsert      │ (Vector DB)│
└─────────────┘                    └──────────────────┘                  └─────┬──────┘
                                                                              │
                    ┌─────────────────────────────────────────────────────────┘
                    │  Similarity Search
                    ▼
┌──────────┐   Query   ┌───────────────┐  Guardrails OK   ┌───────────────┐  Context  ┌─────────┐
│ Frontend │ ────────▶ │  FastAPI       │ ───────────────▶ │  RAG Pipeline │ ────────▶ │  LLM    │
│(Streamlit)│  HTTP    │  (API Server)  │                  │  (Retriever)  │           │(OpenAI) │
└──────────┘          └───────────────┘                  └───────────────┘          └────┬────┘
| Database     | **ChromaDB (Cloud Hosted)**                                               |
| Setup        | `HttpClient` connecting to `api.trychroma.com`                            |
| Persistence  | Managed cloud storage (No local `data/chroma_db/` folder needed)          |       │                                                          │
     └───────────────────────┴──────────── Formatted Response ◀─────────────────────────┘
```

### 1.2 Core Design Principles

| Principle             | Implementation                                                         |
| --------------------- | ---------------------------------------------------------------------- |
| Facts-only            | LLM system prompt + advisory intent classifier reject non-factual Qs   |
| Source transparency    | Every chunk carries `source_url` and `last_updated_date` metadata      |
| Data freshness         | GitHub Actions cron triggers daily scrape at 9:15 AM IST and upserts to vector DB |
| Privacy compliance     | PII regex scanner blocks queries containing PAN, Aadhaar, phone, email |
| Conciseness            | LLM prompt hard-caps responses at 3 sentences                         |

---

## 2. Project Structure

```
M-2/
├── .github/
│   └── workflows/
│       └── daily_ingest.yml     # GitHub Actions: daily 9:15 AM IST cron
├── backend/
│   ├── main.py                  # FastAPI application entry point
│   ├── config.py                # Environment variables, constants, URL list
│   ├── scraper/
│   │   ├── scraper.py           # Core scraping logic (requests + BeautifulSoup)
│   │   └── parser.py            # HTML parsing helpers, section extractors
│   ├── ingestion/
│   │   ├── chunker.py           # Text chunking strategies
│   │   ├── embedder.py          # OpenAI embedding wrapper
│   │   ├── vector_store.py      # ChromaDB collection management (upsert, query)
│   │   └── run_pipeline.py      # Orchestrator script: scrape → chunk → embed → upsert
│   ├── rag/
│   │   ├── guardrails.py        # PII filter + advisory intent classifier
│   │   ├── retriever.py         # Similarity search + metadata filtering
│   │   ├── generator.py         # LLM prompt builder + response formatter
│   │   └── prompts.py           # All prompt templates (system, user, refusal)
│   └── chat/
│       ├── threads.py           # Thread manager (SQLite-backed)
│       └── models.py            # Pydantic request/response schemas
├── frontend/
│   └── app.py                   # Streamlit UI
├── data/
│   └── chroma_db/               # Persisted ChromaDB storage
├── docs/
│   ├── architecture.md          # This file (main architecture)
│   ├── chunking_embedding_architecture.md  # Detailed chunking & embedding design
│   └── Problem_statement.md
├── .env.example                 # Template for environment variables
├── requirements.txt
└── README.md
```

---

## 3. Phased Architecture

---

### Phase 1: Knowledge Base Factory (Data Ingestion & Extraction)

**Goal:** Automate the collection, parsing, chunking, embedding, and storage of mutual fund facts from Groww into a searchable vector database — refreshed daily.

#### 1A. Scheduler — GitHub Actions (`.github/workflows/daily_ingest.yml`)

| Detail           | Value                                                                       |
| ---------------- | --------------------------------------------------------------------------- |
| Platform         | **GitHub Actions** (free for public repos, 2000 min/month for private)      |
| Trigger          | `cron: '45 3 * * *'` (3:45 AM UTC = **9:15 AM IST**)                       |
| Job              | Checks out repo → installs deps → runs `python -m backend.ingestion.run_pipeline` |
| Manual Trigger   | `workflow_dispatch` event — allows manual "Run workflow" button in GitHub UI |
| Secrets          | `OPENAI_API_KEY` stored as a GitHub Actions secret                          |
| Artifact Upload  | After pipeline run, uploads the updated `data/chroma_db/` as a build artifact or commits it back to the repo |

**Workflow YAML Structure:**
```yaml
name: Daily Knowledge Base Refresh

on:
  schedule:
    - cron: '45 3 * * *'    # 3:45 AM UTC = 9:15 AM IST
  workflow_dispatch:          # Manual trigger button

jobs:
  ingest:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install Dependencies
        run: pip install -r requirements.txt

      - name: Run Ingestion Pipeline
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: python -m backend.ingestion.run_pipeline

      - name: Commit Updated Vector DB
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add data/chroma_db/
          git diff --cached --quiet || git commit -m "chore: daily knowledge base refresh $(date +%Y-%m-%d)"
          git push
```

**How it works:**
1. GitHub Actions triggers the workflow at 9:15 AM IST (3:45 AM UTC) every day.
2. The runner checks out the repo, installs Python dependencies.
3. Runs `backend.ingestion.run_pipeline` which orchestrates: scrape → chunk → embed → upsert into ChromaDB.
4. The updated ChromaDB files are committed back to the repository automatically.
5. On the next deployment or server restart, the backend picks up the latest vector DB state.
6. A manual "Run workflow" button is also available in the GitHub Actions tab for on-demand triggers.
7. Logs for each run (success/failure per URL, chunk counts) are visible in the Actions tab.

#### 1B. Scraping Service (`backend/scraper/`)

**Target URLs (Corpus):**

| # | Scheme                          | URL                                                                     | Category   |
|---|----------------------------------|-------------------------------------------------------------------------|------------|
| 1 | HDFC Large Cap Fund              | `https://groww.in/mutual-funds/hdfc-large-cap-fund-direct-growth`       | Large Cap  |
| 2 | HDFC ELSS Tax Saver Fund         | `https://groww.in/mutual-funds/hdfc-elss-tax-saver-fund-direct-plan-growth` | ELSS   |
| 3 | HDFC Focused Fund                | `https://groww.in/mutual-funds/hdfc-focused-fund-direct-growth`         | Focused    |
| 4 | HDFC Equity Fund                 | `https://groww.in/mutual-funds/hdfc-equity-fund-direct-growth`          | Multi Cap  |
| 5 | HDFC Mid-Cap Opportunities Fund  | `https://groww.in/mutual-funds/hdfc-mid-cap-fund-direct-growth`         | Mid Cap    |

**Scraping Strategy:**
- **Primary Method:** `requests` + `BeautifulSoup` for static HTML extraction.
- **Fallback Method:** `Playwright` (headless browser) if Groww pages require JavaScript rendering.
- **Parser Logic (`parser.py`):** Extract specific data sections from the page:
  - Scheme name, NAV, AUM
  - Expense ratio, exit load, lock-in period
  - Minimum SIP/lumpsum amounts
  - Benchmark index, riskometer category
  - Fund manager name
  - Sectoral/holding allocation (top holdings)
- **Rate Limiting:** 2-second delay between requests to avoid being blocked.
- **User-Agent Rotation:** Use realistic browser user-agent strings.

**Output per URL:** A structured dictionary:
```python
{
  "scheme_name": "HDFC Large Cap Fund",
  "source_url": "https://groww.in/mutual-funds/hdfc-large-cap-fund-direct-growth",
  "scraped_at": "2026-04-22T09:15:00+05:30",
  "sections": [
    {"title": "Basic Info", "content": "NAV: ₹923.45. AUM: ₹35,280 Cr. ..."},
    {"title": "Expense & Loads", "content": "Expense Ratio: 1.07%. Exit Load: 1% if redeemed within 1 year. ..."},
    {"title": "Investment Details", "content": "Min SIP: ₹500. Min Lumpsum: ₹5,000. ..."},
    ...
  ]
}
```

#### 1C. Chunking (`backend/ingestion/chunker.py`)

| Parameter        | Value                                                                 |
| ---------------- | --------------------------------------------------------------------- |
| Strategy         | Section-aware chunking: each logical section becomes 1 chunk          |
| Chunk Size       | Target ~300-500 tokens per chunk                                      |
| Overlap          | 50 tokens overlap between adjacent chunks from the same section       |
| Splitting Fallback| If a section exceeds 500 tokens, split by sentence boundaries        |

**Metadata attached to every chunk:**
```python
{
  "source_url": "https://groww.in/mutual-funds/hdfc-large-cap-fund-direct-growth",
  "last_updated_date": "2026-04-22",    # Date of scrape
  "document_type": "scheme_page",
  "scheme_name": "HDFC Large Cap Fund",
  "section_title": "Expense & Loads",    # Which section this chunk came from
  "chunk_index": 0                       # Position within section
}
```

#### 1D. Embedding & Vector Storage (`backend/ingestion/`)

| Component    | Choice                                                                    |
| ------------ | ------------------------------------------------------------------------- |
| Embedding    | OpenAI `text-embedding-3-small` (1536 dimensions, cost-effective)         |
| Vector DB    | ChromaDB with persistent storage at `data/chroma_db/`                     |
| Collection   | Single collection: `mutual_fund_facts`                                    |
| Upsert Logic | Use `source_url + section_title + chunk_index` as deterministic ID so daily runs replace stale data instead of duplicating |
| Distance     | Cosine similarity (ChromaDB default)                                      |

**Upsert flow:**
```
For each chunk:
  1. Generate deterministic ID = hash(source_url + section_title + chunk_index)
  2. Embed chunk text via OpenAI
  3. Upsert (id, embedding, text, metadata) into ChromaDB
```

#### Phase 1 — Validation Checklist
- [ ] Run `python -m backend.scheduler.scheduler` — confirm it triggers at 9:15 AM.
- [ ] Run `POST /admin/ingest` — confirm all 5 URLs are scraped without error.
- [ ] Inspect ChromaDB collection count — should have ~50-100 chunks.
- [ ] CLI similarity search for "expense ratio HDFC Large Cap" — should return the correct chunk with source URL.

---

### Phase 2: RAG Logic Core & Guardrails

**Goal:** Build the query processing pipeline that takes a user question, validates it through safety layers, retrieves relevant chunks, and generates a strictly constrained response with citation.

#### 2A. Guardrail Layer (`backend/rag/guardrails.py`)

**Guardrail 1 — PII Scanner:**
```
Input: raw user query string
Process:
  - Regex patterns for:
    - PAN:       [A-Z]{5}[0-9]{4}[A-Z]{1}
    - Aadhaar:   \b\d{4}\s?\d{4}\s?\d{4}\b
    - Phone:     \b[6-9]\d{9}\b
    - Email:     standard email regex
    - Account:   \b\d{9,18}\b
  - If ANY match found → immediately return:
    {
      "blocked": true,
      "reason": "pii_detected",
      "response": "I cannot process queries containing personal information like PAN, Aadhaar, phone numbers, or email addresses. Please remove any personal details and try again."
    }
```

**Guardrail 2 — Advisory Intent Filter:**
```
Input: raw user query string
Process:
  - Keyword/phrase scanning for advisory patterns:
    - "should I invest", "should I buy", "is it good", "which is better",
    - "recommend", "suggest", "compare returns", "predict", "will it go up"
  - Optional: use a zero-shot classifier (e.g., OpenAI function call or small model)
    with labels: ["factual_query", "advisory_query", "off_topic"]
  - If advisory detected → return:
    {
      "blocked": true,
      "reason": "advisory_query",
      "response": "I can only answer factual questions about mutual fund schemes. I cannot provide investment advice or recommendations.\n\nFor investment guidance, please visit: https://www.amfiindia.com/investor-corner/knowledge-center.html"
    }
```

**Guardrail execution order:** PII check first → Advisory check second → proceed to retrieval.

#### 2B. Retriever (`backend/rag/retriever.py`)

| Parameter        | Value                                                          |
| ---------------- | -------------------------------------------------------------- |
| Top-K            | `k=5` (retrieve 5 most similar chunks)                        |
| Similarity       | Cosine distance via ChromaDB                                   |
| Relevance Filter | Discard chunks with distance > 0.75 (too dissimilar)           |
| Tie-breaking     | If two chunks have similar scores, prefer the one with the most recent `last_updated_date` |

**Retrieval flow:**
```
1. Embed the user query using text-embedding-3-small
2. Query ChromaDB for top-5 nearest neighbors
3. Filter out any chunk with distance > 0.75
4. Sort remaining by (score ASC, last_updated_date DESC)
5. Return list of (chunk_text, metadata) pairs
```

**Edge case — No relevant chunks found:**
- If 0 chunks pass the relevance filter, return:
  `"I don't have information about that in my current knowledge base. Please try rephrasing your question or check the official HDFC MF page directly."`

#### 2C. Generator (`backend/rag/generator.py` + `prompts.py`)

**System Prompt Template:**
```
You are a facts-only mutual fund FAQ assistant for HDFC mutual fund schemes listed on Groww.

STRICT RULES:
1. Answer ONLY using the provided context below. Do NOT use any external knowledge.
2. Your answer must be 3 sentences or fewer.
3. Do NOT provide investment advice, opinions, comparisons, or return predictions.
4. If the context does not contain the answer, say: "I don't have this information in my current sources."
5. Be precise with numbers — quote exact figures from context (NAV, expense ratio, etc.)
6. Do NOT generate any disclaimers beyond what is appended by the system.
```

**User Prompt Template:**
```
Context:
---
{retrieved_chunks_text}
---

User Question: {user_query}

Answer (3 sentences max, facts only):
```

**Post-Processing Pipeline:**
```
1. Receive raw LLM text
2. Truncate to 3 sentences if LLM exceeds (sentence-split + rejoin first 3)
3. Select citation: pick the source_url from the chunk with the highest relevance score
4. Select date: pick the most recent last_updated_date from the retrieved metadata
5. Append footer:
   "\n\nSource: {source_url}\nLast updated from sources: {last_updated_date}"
6. Return final formatted response
```

**Model Configuration:**

| Parameter    | Value                     |
| ------------ | ------------------------- |
| Model        | `gpt-4o-mini`             |
| Temperature  | `0.0` (deterministic)     |
| Max Tokens   | `250`                     |
| Top-P        | `1.0`                     |

#### Phase 2 — Validation Checklist
- [ ] Query: "What is the expense ratio of HDFC Large Cap Fund?" → Returns ≤ 3 sentence answer with source URL + date footer.
- [ ] Query: "Should I invest in HDFC ELSS?" → Returns advisory refusal message with AMFI link.
- [ ] Query: "My PAN is ABCDE1234F and I want to know exit load" → Returns PII rejection.
- [ ] Query: "What is the weather today?" → Returns "I don't have this information" response.
- [ ] Confirm temperature=0 yields consistent answers across identical queries.

---

### Phase 3: Backend API & Thread Context (The Server)

**Goal:** Wrap the RAG pipeline in a production-ready REST API with multi-thread conversation support.

#### 3A. FastAPI Application (`backend/main.py`)

**Server Configuration:**
- Framework: `FastAPI` with `uvicorn` ASGI server.
- CORS: Allow frontend origin (`http://localhost:8501` for Streamlit).
- Lifespan: On startup, initialize ChromaDB connection and start the APScheduler.

#### 3B. API Endpoints

**`POST /chat/{thread_id}`** — Send a message

```
Request Body:
{
  "query": "What is the exit load for HDFC ELSS?"
}

Response (200):
{
  "thread_id": "abc-123",
  "query": "What is the exit load for HDFC ELSS?",
  "response": "The exit load for HDFC ELSS Tax Saver Fund is nil (0%), as ELSS funds have a mandatory 3-year lock-in period during which units cannot be redeemed. After the lock-in period, there is no exit load.\n\nSource: https://groww.in/mutual-funds/hdfc-elss-tax-saver-fund-direct-plan-growth\nLast updated from sources: 2026-04-22",
  "blocked": false,
  "block_reason": null,
  "timestamp": "2026-04-22T10:30:00+05:30"
}

Response (200, blocked):
{
  "thread_id": "abc-123",
  "query": "Should I invest in HDFC Large Cap?",
  "response": "I can only answer factual questions...",
  "blocked": true,
  "block_reason": "advisory_query",
  "timestamp": "..."
}
```

**`POST /threads`** — Create a new thread
```
Response (201):
{
  "thread_id": "generated-uuid",
  "created_at": "2026-04-22T10:30:00+05:30"
}
```

**`GET /threads`** — List all threads
```
Response (200):
{
  "threads": [
    {"thread_id": "abc-123", "created_at": "...", "message_count": 5, "last_message_preview": "What is the..."},
    ...
  ]
}
```

**`GET /threads/{thread_id}/history`** — Get full history
```
Response (200):
{
  "thread_id": "abc-123",
  "messages": [
    {"role": "user", "content": "...", "timestamp": "..."},
    {"role": "assistant", "content": "...", "timestamp": "...", "blocked": false}
  ]
}
```

**`DELETE /threads/{thread_id}`** — Delete a thread

**`POST /admin/ingest`** — Manually trigger scraping pipeline (protected)

#### 3C. Thread Manager (`backend/chat/threads.py`)

| Detail          | Value                                                               |
| --------------- | ------------------------------------------------------------------- |
| Storage         | SQLite (`data/threads.db`) for persistence across restarts          |
| Tables          | `threads(id, created_at)`, `messages(id, thread_id, role, content, blocked, timestamp)` |
| Context Window  | Pass the last 5 message pairs (user + assistant) as conversation history to the LLM for follow-up questions |
| Isolation       | Each `thread_id` has completely independent context — no cross-contamination |

**Follow-up handling:**
```
1. User asks: "What is the SIP amount for HDFC Large Cap?"
   → Normal retrieval + generation
2. User follows up: "And what about its exit load?"
   → Thread history provides context that "its" = HDFC Large Cap Fund
   → Retriever searches with expanded context from conversation history
```

#### 3D. Pydantic Models (`backend/chat/models.py`)

```python
class ChatRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=500)

class ChatResponse(BaseModel):
    thread_id: str
    query: str
    response: str
    blocked: bool
    block_reason: Optional[str]
    timestamp: datetime

class ThreadInfo(BaseModel):
    thread_id: str
    created_at: datetime
    message_count: int
    last_message_preview: Optional[str]
```

#### Phase 3 — Validation Checklist
- [ ] `POST /threads` → creates a new thread successfully.
- [ ] `POST /chat/{thread_id}` with factual query → returns correct response.
- [ ] `POST /chat/{thread_id}` with advisory query → returns blocked response.
- [ ] `GET /threads/{thread_id}/history` → returns the full conversation.
- [ ] Two different `thread_id`s maintain completely independent histories.
- [ ] Follow-up query in same thread correctly resolves context (e.g., "it", "this fund").
- [ ] `POST /admin/ingest` → triggers full scraping pipeline.

---

### Phase 4: The Frontend Experience

**Goal:** Build a clean, minimal chat UI matching the deliverable specification.

#### 4A. Technology

| Detail     | Value                                                         |
| ---------- | ------------------------------------------------------------- |
| Framework  | `Streamlit` (Python-native, rapid prototyping)                |
| Entry      | `frontend/app.py`                                             |
| API Calls  | `requests` library hitting FastAPI at `http://localhost:8000`  |

#### 4B. UI Layout Specification

```
┌──────────────────────────────────────────────────────────────┐
│  SIDEBAR                          │  MAIN CHAT AREA          │
│                                   │                          │
│  ┌─────────────────────────────┐  │  ┌────────────────────┐  │
│  │  + New Thread               │  │  │  💬 MF FAQ Asst.   │  │
│  ├─────────────────────────────┤  │  │                    │  │
│  │  🗨 Thread 1 (Apr 22)      │  │  │  "Facts-only.      │  │
│  │  🗨 Thread 2 (Apr 21)      │  │  │   No investment    │  │
│  │  🗨 Thread 3 (Apr 20)      │  │  │   advice."         │  │
│  └─────────────────────────────┘  │  ├────────────────────┤  │
│                                   │  │  Welcome! Try:     │  │
│                                   │  │  • "Expense ratio  │  │
│                                   │  │    of HDFC Large    │  │
│                                   │  │    Cap Fund?"       │  │
│                                   │  │  • "Min SIP for    │  │
│                                   │  │    HDFC ELSS?"      │  │
│                                   │  │  • "Exit load of   │  │
│                                   │  │    HDFC Mid-Cap?"   │  │
│                                   │  ├────────────────────┤  │
│                                   │  │  Chat messages...  │  │
│                                   │  │                    │  │
│                                   │  ├────────────────────┤  │
│                                   │  │  [  Type here...  ]│  │
│                                   │  └────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

#### 4C. UI Components Detail

**Disclaimer Banner (Top of Main Area):**
- Always visible, non-dismissable.
- Text: `"⚠️ Facts-only. No investment advice."`
- Styling: Yellow/amber background to draw attention.

**Welcome State (When thread has no messages):**
- Greeting: "Welcome! I can answer factual questions about HDFC mutual fund schemes."
- 3 clickable example buttons:
  1. "What is the expense ratio of HDFC Large Cap Fund?"
  2. "What is the minimum SIP amount for HDFC ELSS Tax Saver?"
  3. "What is the exit load for HDFC Mid-Cap Opportunities Fund?"
- Clicking a button auto-submits it as a query.

**Chat Messages:**
- User messages: right-aligned, blue bubble.
- Assistant messages: left-aligned, gray bubble.
- Blocked/refusal messages: left-aligned, red-tinted bubble with ⚠️ icon.
- Citation footer rendered in smaller, muted text below message.

**Sidebar — Thread Manager:**
- "+ New Thread" button at top.
- List of existing threads sorted by most recent activity.
- Each thread shows: truncated last message preview + date.
- Clicking a thread switches context.
- Delete thread button (🗑️ icon) per thread.

#### 4D. State Management

```
Streamlit Session State:
  - st.session_state.current_thread_id   → active thread UUID
  - st.session_state.threads             → list of ThreadInfo from GET /threads
  - st.session_state.messages            → current thread's message history
```

#### Phase 4 — Validation Checklist
- [ ] App loads with disclaimer visible and 3 example questions.
- [ ] Clicking example question sends it as a query and displays response.
- [ ] Typing a custom question works end-to-end.
- [ ] Refusal messages render with distinct styling.
- [ ] Creating a "New Thread" clears chat and starts fresh context.
- [ ] Switching threads loads correct conversation history.
- [ ] Deleting a thread removes it from the sidebar.

---

## 4. Recommended Tech Stack (Summary)

| Layer          | Technology                          | Why                                           |
| -------------- | ----------------------------------- | --------------------------------------------- |
| Frontend       | Streamlit                           | Python-native, rapid, no JS build step        |
| Backend API    | FastAPI + Uvicorn                   | Async, fast, auto-docs (Swagger)              |
| Scheduler      | APScheduler                         | Lightweight, integrates with FastAPI lifespan  |
| Scraping       | Requests + BeautifulSoup (+ Playwright fallback) | Simple static scraping with JS fallback |
| Embeddings     | OpenAI `text-embedding-3-small`     | Cost-effective, 1536-dim, good accuracy        |
| LLM            | OpenAI `gpt-4o-mini`               | Cheap, fast, excellent instruction-following   |
| Vector DB      | ChromaDB (persistent local)          | Zero infrastructure, file-based persistence    |
| Thread Storage | SQLite                              | Zero-config, persistent, good for single-server|
| Orchestration  | LangChain (optional) or raw SDK     | Flexible RAG chain composition                 |

---

## 5. Environment Variables

```env
# .env.example
OPENAI_API_KEY=sk-...
CHROMA_PERSIST_DIR=./data/chroma_db
SQLITE_DB_PATH=./data/threads.db
SCRAPE_SCHEDULE_HOUR=9
SCRAPE_SCHEDULE_MINUTE=15
FASTAPI_HOST=0.0.0.0
FASTAPI_PORT=8000
LOG_LEVEL=INFO
```

---

## 6. Error Handling & Logging Strategy

| Scenario                      | Handling                                                            |
| ----------------------------- | ------------------------------------------------------------------- |
| URL unreachable during scrape | Log warning, skip URL, continue with remaining URLs                 |
| OpenAI API rate limit         | Exponential backoff with `tenacity` retry (max 3 attempts)          |
| ChromaDB write failure        | Log error, raise alert, skip chunk upsert                           |
| No relevant chunks retrieved  | Return "I don't have this information" message                      |
| LLM returns > 3 sentences    | Post-processor truncates to first 3 sentences                       |
| Invalid thread_id             | Return 404 with descriptive error                                   |
| Malformed user input          | Pydantic validation returns 422 with field-level errors             |

**Logging:** Use Python `logging` module with structured JSON output. Log every query (anonymized), guardrail triggers, retrieval scores, and LLM token usage.
