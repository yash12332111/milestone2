"""
models.py — Pydantic request/response schemas for the Chat API.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Request Models
# ---------------------------------------------------------------------------
class ChatRequest(BaseModel):
    """Incoming chat message."""
    query: str = Field(..., min_length=1, max_length=500, description="User's question")


# ---------------------------------------------------------------------------
# Response Models
# ---------------------------------------------------------------------------
class ChatResponse(BaseModel):
    """Response to a chat message."""
    thread_id: str
    query: str
    response: str
    blocked: bool
    block_reason: Optional[str] = None
    timestamp: datetime


class ThreadInfo(BaseModel):
    """Summary info for a single thread."""
    thread_id: str
    created_at: datetime
    message_count: int
    last_message_preview: Optional[str] = None


class ThreadCreateResponse(BaseModel):
    """Response when a new thread is created."""
    thread_id: str
    created_at: datetime


class ThreadListResponse(BaseModel):
    """Response listing all threads."""
    threads: list[ThreadInfo]


class ThreadHistoryMessage(BaseModel):
    """A single message in thread history."""
    role: str  # "user" or "assistant"
    content: str
    blocked: bool = False
    block_reason: Optional[str] = None
    timestamp: datetime


class ThreadHistoryResponse(BaseModel):
    """Full history of a thread."""
    thread_id: str
    messages: list[ThreadHistoryMessage]
