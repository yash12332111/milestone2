"""
main.py — FastAPI application entry point for the Mutual Fund FAQ Assistant.

Endpoints:
  POST /threads              — Create a new chat thread
  GET  /threads              — List all threads
  GET  /threads/{id}/history — Get full thread history
  DELETE /threads/{id}       — Delete a thread
  POST /chat/{id}            — Send a message (RAG pipeline)
  POST /admin/ingest         — Manually trigger ingestion pipeline
"""

from __future__ import annotations

import logging
import sys
import os

# Ensure project root is on path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from phase1_data_ingestion.config import LOG_LEVEL
from phase3_api_server.chat.models import (
    ChatRequest,
    ChatResponse,
    ThreadCreateResponse,
    ThreadListResponse,
    ThreadHistoryResponse,
    ThreadHistoryMessage,
)
from phase3_api_server.chat.threads import (
    create_thread,
    get_thread,
    list_threads,
    delete_thread,
    add_message,
    get_thread_history,
    close_db,
)
from phase2_rag_core.pipeline import process_query

from datetime import datetime, timezone

# ---------------------------------------------------------------------------
# Logging -> Save to logs/website_activity.log
# ---------------------------------------------------------------------------
log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
os.makedirs(log_dir, exist_ok=True)
log_file_path = os.path.join(log_dir, "website_activity.log")

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(log_file_path, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)
logger.info(f"Application checking in. Logs will be recorded to: {log_file_path}")

# Phase 2 (RAG Logic Core) separate logger
rag_logger = logging.getLogger("phase2_rag_core")
rag_logger.setLevel(logging.INFO)
rag_file_path = os.path.join(log_dir, "rag_pipeline.log")
rag_handler = logging.FileHandler(rag_file_path, encoding='utf-8')
rag_handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)-8s | [%(name)s] %(message)s"))
rag_logger.addHandler(rag_handler)
rag_logger.propagate = False


# ---------------------------------------------------------------------------
# App Lifespan (startup / shutdown)
# ---------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Mutual Fund FAQ Assistant API starting up...")
    yield
    close_db()
    logger.info("🛑 API shutting down. Database connection closed.")


# ---------------------------------------------------------------------------
# FastAPI App
# ---------------------------------------------------------------------------
app = FastAPI(
    title="Mutual Fund FAQ Assistant",
    description="Facts-only RAG chatbot for HDFC mutual fund schemes on Groww.",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS — explicitly whitelist the deployed Vercel UI and local instances
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:8501",
        "https://milestone2-neon.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Thread Endpoints
# ---------------------------------------------------------------------------
@app.post("/threads", status_code=201, response_model=ThreadCreateResponse)
async def api_create_thread():
    """Create a new chat thread."""
    result = create_thread()
    logger.info(f"👤 New User Session Started -> Thread ID: {result['thread_id']}")
    return ThreadCreateResponse(
        thread_id=result["thread_id"],
        created_at=result["created_at"],
    )


@app.get("/threads", response_model=ThreadListResponse)
async def api_list_threads():
    """List all threads with message counts and previews."""
    threads = list_threads()
    return ThreadListResponse(threads=threads)


@app.get("/threads/{thread_id}/history", response_model=ThreadHistoryResponse)
async def api_get_history(thread_id: str):
    """Get full conversation history for a thread."""
    thread = get_thread(thread_id)
    if thread is None:
        raise HTTPException(status_code=404, detail=f"Thread {thread_id} not found.")

    messages = get_thread_history(thread_id)
    return ThreadHistoryResponse(
        thread_id=thread_id,
        messages=[ThreadHistoryMessage(**m) for m in messages],
    )


@app.delete("/threads/{thread_id}", status_code=200)
async def api_delete_thread(thread_id: str):
    """Delete a thread and all its messages."""
    deleted = delete_thread(thread_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Thread {thread_id} not found.")
    return {"detail": f"Thread {thread_id} deleted."}


# ---------------------------------------------------------------------------
# Chat Endpoint
# ---------------------------------------------------------------------------
@app.post("/chat/{thread_id}", response_model=ChatResponse)
async def api_chat(thread_id: str, body: ChatRequest):
    """
    Send a message to a thread. Runs the full RAG pipeline:
    guardrails → retrieval → generation.
    """
    # Verify thread exists
    thread = get_thread(thread_id)
    if thread is None:
        raise HTTPException(status_code=404, detail=f"Thread {thread_id} not found.")

    query = body.query.strip()
    now = datetime.now(timezone.utc)

    # Save user message
    add_message(thread_id=thread_id, role="user", content=query)
    logger.info(f"💬 [Thread: {thread_id}] User Query: '{query}'")

    # Process through RAG pipeline
    try:
        result = process_query(query)
    except Exception as e:
        logger.error(f"RAG pipeline error: {e}")
        raise HTTPException(status_code=500, detail="An error occurred processing your query.")

    # Save assistant response
    add_message(
        thread_id=thread_id,
        role="assistant",
        content=result["response"],
        blocked=result["blocked"],
        block_reason=result["block_reason"],
    )
    
    if result["blocked"]:
        logger.warning(f"🚫 [Thread: {thread_id}] Query Blocked: {result['block_reason']}")
    else:
        logger.info(f"🤖 [Thread: {thread_id}] AI Response generated successfully.")

    return ChatResponse(
        thread_id=thread_id,
        query=query,
        response=result["response"],
        blocked=result["blocked"],
        block_reason=result["block_reason"],
        timestamp=now,
    )


# ---------------------------------------------------------------------------
# Admin Endpoint
# ---------------------------------------------------------------------------
@app.post("/admin/ingest", status_code=200)
async def api_trigger_ingest():
    """Manually trigger the data ingestion pipeline."""
    try:
        from phase1_data_ingestion.ingestion.run_pipeline import run_ingestion_pipeline
        total = run_ingestion_pipeline()
        return {"detail": f"Ingestion complete. {total} chunks in vector store."}
    except Exception as e:
        logger.error(f"Ingestion pipeline error: {e}")
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")


# ---------------------------------------------------------------------------
# Health Check
# ---------------------------------------------------------------------------
@app.get("/health")
async def health_check():
    """Basic health check endpoint."""
    return {"status": "healthy", "service": "mutual-fund-faq-assistant"}
