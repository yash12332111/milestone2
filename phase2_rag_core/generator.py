"""
generator.py — LLM response generation via Groq API with strict formatting constraints.

Takes retrieved context + user query, generates a response via Groq-hosted LLM,
then post-processes to enforce: max 3 sentences, 1 citation, date footer.
"""

from __future__ import annotations

import logging
import re

from phase1_data_ingestion.config import GROQ_API_KEY, LLM_MODEL, LLM_TEMPERATURE, LLM_MAX_TOKENS
from phase2_rag_core.prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE

logger = logging.getLogger(__name__)


def generate_response(
    query: str,
    context_text: str,
    best_source_url: str,
    latest_date: str,
) -> str:
    """
    Generate a facts-only response using Groq-hosted LLM.

    Steps:
    1. Build the system + user prompt from templates.
    2. Call Groq API (OpenAI-compatible SDK).
    3. Post-process: truncate to 3 sentences + append citation footer.
    """
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is not set. Configure it in .env.")

    try:
        import openai
    except ImportError:
        raise ImportError("openai not installed. Run: pip install openai")

    # Groq uses the OpenAI SDK with a different base_url
    client = openai.OpenAI(
        api_key=GROQ_API_KEY,
        base_url="https://api.groq.com/openai/v1"
    )

    # Build the user prompt
    user_prompt = USER_PROMPT_TEMPLATE.format(
        context=context_text,
        question=query,
    )

    logger.info(f"Generating response via Groq ({LLM_MODEL}) for: '{query[:80]}...'")

    try:
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=LLM_TEMPERATURE,
            max_tokens=LLM_MAX_TOKENS,
            top_p=1.0,
        )
    except Exception as e:
        logger.error(f"LLM generation failed: {e}")
        raise

    raw_answer = response.choices[0].message.content.strip()
    logger.info(f"Raw LLM output ({len(raw_answer)} chars): {raw_answer[:100]}...")

    # Post-process: enforce 3-sentence limit
    truncated_answer = _truncate_to_sentences(raw_answer, max_sentences=3)

    # Append citation footer
    formatted_response = _append_footer(truncated_answer, best_source_url, latest_date)

    return formatted_response


def _truncate_to_sentences(text: str, max_sentences: int = 3) -> str:
    """Split text into sentences and keep only the first N."""
    # Split by sentence-ending punctuation followed by a space or end of string
    sentences = re.split(r"(?<=[.!?])\s+", text)
    sentences = [s.strip() for s in sentences if s.strip()]

    if len(sentences) <= max_sentences:
        return text

    truncated = " ".join(sentences[:max_sentences])
    # Ensure it ends with a period
    if not truncated.endswith((".", "!", "?")):
        truncated += "."

    logger.info(f"Truncated from {len(sentences)} to {max_sentences} sentences.")
    return truncated


def _append_footer(answer: str, source_url: str, last_updated: str) -> str:
    """Append the mandatory citation footer to the response."""
    footer_parts = []
    if source_url:
        footer_parts.append(f"Source: {source_url}")
    if last_updated:
        footer_parts.append(f"Last updated from sources: {last_updated}")

    if footer_parts:
        return answer + "\n\n" + "\n".join(footer_parts)
    return answer
