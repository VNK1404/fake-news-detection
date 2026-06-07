"""
apis/grok_api.py — LLM-based fake news classification
Primary:  Grok (xAI) — requires paid credits at console.x.ai
Fallback: Groq (free tier) — llama-3.3-70b-versatile

AI-Driven Digital Evidence Integrity Monitoring System
"""

import logging
import time
import requests

from fake_news_module.config import (
    GROK_API_KEY,
    GROK_API_URL,
    GROK_MODEL,
    REQUEST_TIMEOUT,
    MAX_RETRIES,
)

logger = logging.getLogger(__name__)

# ── Groq (free fallback) ─────────────────────────────────────
# Get a free key at: https://console.groq.com/keys
import os
GROQ_API_KEY  = os.environ.get("GROQ_API_KEY", "")
GROQ_API_URL  = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL    = "llama-3.3-70b-versatile"

_SYSTEM_PROMPT = (
    "You are a professional fact-checker and misinformation analyst. "
    "Your task is to evaluate whether a given claim is likely REAL (credible, factual) "
    "or FAKE (misinformation, fabricated, misleading). "
    "You must respond with EXACTLY one word: 'Real', 'Fake', or 'Uncertain'. "
    "If the claim involves very recent breaking news, highly specific events, "
    "or you lack sufficient context to be completely sure, you MUST respond 'Uncertain'. "
    "Do not provide any explanation or additional text."
)

_USER_PROMPT_TEMPLATE = (
    "Evaluate this claim and respond with ONLY 'Real' or 'Fake':\n\n{claim}"
)


def _call_llm(api_url: str, api_key: str, model: str, claim: str) -> str | None:
    """
    Generic OpenAI-compatible chat completion call.
    Returns a label string or None on failure.
    """
    if not api_key:
        return None

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "system",  "content": _SYSTEM_PROMPT},
            {"role": "user",    "content": _USER_PROMPT_TEMPLATE.format(claim=claim[:1000])},
        ],
        "temperature": 0.0,
        "max_tokens":  5,
    }

    last_error = None
    for attempt in range(1, MAX_RETRIES + 2):
        try:
            logger.debug("LLM call attempt %d (%s) …", attempt, api_url)
            resp = requests.post(api_url, headers=headers, json=payload, timeout=REQUEST_TIMEOUT)

            if resp.status_code in (401, 403):
                body = {}
                try:
                    body = resp.json()
                except Exception:
                    body = resp.text[:300]
                logger.error(
                    "LLM API auth error %d (%s) | %s",
                    resp.status_code, api_url, body,
                )
                return None            # No point retrying auth errors

            resp.raise_for_status()
            data = resp.json()
            raw  = (
                data.get("choices", [{}])[0]
                .get("message", {})
                .get("content", "")
                .strip()
            )
            label = _normalize_label(raw)
            logger.info("LLM result from %s: '%s' (raw: '%s')", api_url, label, raw)
            return label

        except requests.exceptions.Timeout:
            logger.warning("LLM timeout attempt %d (%s)", attempt, api_url)
            last_error = "Timeout"
        except requests.exceptions.HTTPError as exc:
            logger.error("LLM HTTP error: %s", exc)
            return None
        except requests.exceptions.RequestException as exc:
            logger.warning("LLM request error attempt %d: %s", attempt, exc)
            last_error = str(exc)

        if attempt <= MAX_RETRIES:
            time.sleep(1.5 * attempt)

    logger.error("LLM call failed after retries (%s): %s", api_url, last_error)
    return None


def call_grok_api(claim: str) -> str:
    """
    Classify a claim as Real/Fake using an LLM.

    Tries Grok (xAI) first; falls back to Groq (free) if Grok has no credits.

    Args:
        claim: Claim text to classify.

    Returns:
        'Real', 'Fake', or 'Unknown'
    """
    if not claim or not claim.strip():
        logger.warning("call_grok_api: empty claim, returning Unknown.")
        return "Unknown"

    # ── Try Grok (xAI) ────────────────────────────────────
    label = _call_llm(GROK_API_URL, GROK_API_KEY, GROK_MODEL, claim)
    if label is not None:
        return label

    logger.warning(
        "Grok unavailable (no credits or key invalid). "
        "Falling back to Groq free API. "
        "Add a free key at https://console.groq.com/keys → set GROQ_API_KEY in grok_api.py"
    )

    # ── Fallback: Groq (free) ──────────────────────────────
    label = _call_llm(GROQ_API_URL, GROQ_API_KEY, GROQ_MODEL, claim)
    if label is not None:
        return label

    logger.error("Both Grok and Groq failed. Returning Unknown.")
    return "Unknown"


def _normalize_label(raw: str) -> str:
    """Map raw model output to a canonical label."""
    lower = raw.lower().strip().rstrip(".")
    if lower in ("real", "true", "credible", "factual", "yes"):
        return "Real"
    if lower in ("fake", "false", "misleading", "fabricated", "no"):
        return "Fake"
    # If model returned longer text, scan for keywords
    if "real" in lower and "fake" not in lower:
        return "Real"
    if "fake" in lower or "false" in lower or "mislead" in lower:
        return "Fake"
    if any(k in lower for k in ("uncertain", "unknown", "unsure", "cannot verify")):
        return "Unknown"
    logger.warning("LLM returned unrecognized label: '%s'", raw)
    return "Unknown"
