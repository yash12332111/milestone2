"""
prompts.py — All prompt templates for the RAG generator.

Contains the system prompt, user prompt template, and canned refusal messages.
"""

# ---------------------------------------------------------------------------
# System Prompt (injected as the "system" role message to the LLM)
# ---------------------------------------------------------------------------
SYSTEM_PROMPT = """You are a facts-only mutual fund FAQ assistant for HDFC mutual fund schemes listed on Groww.

STRICT RULES:
1. Answer ONLY using the provided context below. Do NOT use any external knowledge.
2. Your answer must be 3 sentences or fewer.
3. Do NOT provide investment advice, opinions, comparisons, or return predictions.
4. If the context does not contain the answer, say: "I don't have this information in my current sources."
5. Be precise with numbers — quote exact figures from context (NAV, expense ratio, etc.)
6. Do NOT generate any disclaimers beyond what is appended by the system.
"""

# ---------------------------------------------------------------------------
# User Prompt Template (filled with retrieved chunks and the user's question)
# ---------------------------------------------------------------------------
USER_PROMPT_TEMPLATE = """Context:
---
{context}
---

User Question: {question}

Answer (3 sentences max, facts only):"""

# ---------------------------------------------------------------------------
# Refusal Messages
# ---------------------------------------------------------------------------
PII_REFUSAL = (
    "I cannot process queries containing personal information like PAN, Aadhaar, "
    "phone numbers, or email addresses. Please remove any personal details and try again."
)

ADVISORY_REFUSAL = (
    "I can only answer factual questions about mutual fund schemes. "
    "I cannot provide investment advice or recommendations.\n\n"
    "For investment guidance, please visit: "
    "https://www.amfiindia.com/investor-corner/knowledge-center.html"
)

NO_RESULTS_RESPONSE = (
    "I don't have information about that in my current knowledge base. "
    "Please try rephrasing your question or check the official HDFC MF page directly."
)
