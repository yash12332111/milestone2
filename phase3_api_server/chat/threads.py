"""
threads.py — SQLite-backed thread manager for multi-thread chat support.

Handles creation, retrieval, listing, and deletion of chat threads,
as well as persisting individual messages within each thread.
"""

from __future__ import annotations

import logging
import sqlite3
import uuid
from datetime import datetime, timezone
from typing import Optional

from phase1_data_ingestion.config import SQLITE_DB_PATH

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Database Initialization
# ---------------------------------------------------------------------------
_connection: Optional[sqlite3.Connection] = None


def _get_db() -> sqlite3.Connection:
    """Get or create a SQLite connection (with WAL mode for concurrent reads)."""
    global _connection
    if _connection is None:
        import os
        os.makedirs(os.path.dirname(SQLITE_DB_PATH), exist_ok=True)
        _connection = sqlite3.connect(SQLITE_DB_PATH, check_same_thread=False)
        _connection.row_factory = sqlite3.Row
        _connection.execute("PRAGMA journal_mode=WAL")  # Better concurrency
        _init_tables(_connection)
        logger.info(f"SQLite connected at {SQLITE_DB_PATH}")
    return _connection


def _init_tables(conn: sqlite3.Connection) -> None:
    """Create tables if they don't exist."""
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS threads (
            id TEXT PRIMARY KEY,
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            thread_id TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('user', 'assistant')),
            content TEXT NOT NULL,
            blocked INTEGER NOT NULL DEFAULT 0,
            block_reason TEXT,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (thread_id) REFERENCES threads(id) ON DELETE CASCADE
        );

        CREATE INDEX IF NOT EXISTS idx_messages_thread ON messages(thread_id);
    """)
    conn.commit()


# ---------------------------------------------------------------------------
# Thread CRUD
# ---------------------------------------------------------------------------
def create_thread() -> dict:
    """Create a new chat thread. Returns {thread_id, created_at}."""
    db = _get_db()
    thread_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()

    db.execute("INSERT INTO threads (id, created_at) VALUES (?, ?)", (thread_id, now))
    db.commit()

    logger.info(f"Created thread {thread_id}")
    return {"thread_id": thread_id, "created_at": now}


def get_thread(thread_id: str) -> Optional[dict]:
    """Get a single thread by ID. Returns None if not found."""
    db = _get_db()
    row = db.execute("SELECT id, created_at FROM threads WHERE id = ?", (thread_id,)).fetchone()
    if row is None:
        return None
    return {"thread_id": row["id"], "created_at": row["created_at"]}


def list_threads() -> list[dict]:
    """List all threads with message counts and last message preview."""
    db = _get_db()
    rows = db.execute("""
        SELECT
            t.id,
            t.created_at,
            COUNT(m.id) as message_count,
            (SELECT content FROM messages WHERE thread_id = t.id ORDER BY id DESC LIMIT 1) as last_message_preview
        FROM threads t
        LEFT JOIN messages m ON m.thread_id = t.id
        GROUP BY t.id
        ORDER BY t.created_at DESC
    """).fetchall()

    threads = []
    for row in rows:
        preview = row["last_message_preview"]
        if preview and len(preview) > 80:
            preview = preview[:80] + "..."
        threads.append({
            "thread_id": row["id"],
            "created_at": row["created_at"],
            "message_count": row["message_count"],
            "last_message_preview": preview,
        })
    return threads


def delete_thread(thread_id: str) -> bool:
    """Delete a thread and all its messages. Returns True if found and deleted."""
    db = _get_db()
    # Delete messages first (in case FK cascade not supported)
    db.execute("DELETE FROM messages WHERE thread_id = ?", (thread_id,))
    cursor = db.execute("DELETE FROM threads WHERE id = ?", (thread_id,))
    db.commit()

    if cursor.rowcount > 0:
        logger.info(f"Deleted thread {thread_id}")
        return True
    return False


# ---------------------------------------------------------------------------
# Message CRUD
# ---------------------------------------------------------------------------
def add_message(
    thread_id: str,
    role: str,
    content: str,
    blocked: bool = False,
    block_reason: Optional[str] = None,
) -> dict:
    """Add a message to a thread. Returns the message dict."""
    db = _get_db()
    now = datetime.now(timezone.utc).isoformat()

    db.execute(
        "INSERT INTO messages (thread_id, role, content, blocked, block_reason, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
        (thread_id, role, content, int(blocked), block_reason, now),
    )
    db.commit()

    return {
        "role": role,
        "content": content,
        "blocked": blocked,
        "block_reason": block_reason,
        "timestamp": now,
    }


def get_thread_history(thread_id: str) -> list[dict]:
    """Get all messages for a thread, ordered chronologically."""
    db = _get_db()
    rows = db.execute(
        "SELECT role, content, blocked, block_reason, timestamp FROM messages WHERE thread_id = ? ORDER BY id ASC",
        (thread_id,),
    ).fetchall()

    return [
        {
            "role": row["role"],
            "content": row["content"],
            "blocked": bool(row["blocked"]),
            "block_reason": row["block_reason"],
            "timestamp": row["timestamp"],
        }
        for row in rows
    ]


def get_recent_context(thread_id: str, max_pairs: int = 5) -> list[dict]:
    """
    Get the last N message pairs (user + assistant) for conversation context.
    Returns messages in chronological order for LLM context injection.
    """
    db = _get_db()
    # Get the last max_pairs*2 messages (each pair = 1 user + 1 assistant)
    rows = db.execute(
        "SELECT role, content FROM messages WHERE thread_id = ? AND blocked = 0 ORDER BY id DESC LIMIT ?",
        (thread_id, max_pairs * 2),
    ).fetchall()

    # Reverse to get chronological order
    messages = [{"role": row["role"], "content": row["content"]} for row in reversed(rows)]
    return messages


def close_db() -> None:
    """Close the database connection."""
    global _connection
    if _connection is not None:
        _connection.close()
        _connection = None
        logger.info("SQLite connection closed.")
