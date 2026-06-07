"""
apis/rapid_api.py — RapidAPI Fake News / Misinformation Detection integration
AI-Driven Digital Evidence Integrity Monitoring System
"""

import logging
import time
import requests

from fake_news_module.config import (
    RAPID_API_KEY,
    RAPID_API_URL,
    RAPID_API_HOST,
    REQUEST_TIMEOUT,
    MAX_RETRIES,
)

logger = logging.getLogger(__name__)

# Fallback endpoints to try if the primary one fails
_FALLBACK_ENDPOINTS = [
    {
        "url": "https://fake-news-detection3.p.rapidapi.com/predict",
        "host": "fake-news-detection3.p.rapidapi.com",
        "body_key": "news",
        "method": "POST",
    },
    {
        "url": "https://news-article-data-extract-and-summarization1.p.rapidapi.com/classify",
        "host": "news-article-data-extract-and-summarization1.p.rapidapi.com",
        "body_key": "text",
        "method": "POST",
    },
]


def _try_endpoint(endpoint: dict, text: str) -> str | None:
    """
    Attempt a single RapidAPI endpoint. Returns a label or None on failure.
    """
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": endpoint["host"],
    }
    payload = {endpoint["body_key"]: text[:1500]}

    try:
        if endpoint["method"] == "POST":
            resp = requests.post(endpoint["url"], headers=headers, json=payload, timeout=REQUEST_TIMEOUT)
        else:
            resp = requests.get(endpoint["url"], headers=headers, params=payload, timeout=REQUEST_TIMEOUT)

        # Skip non-actionable errors silently
        if resp.status_code in (400, 401, 403, 404, 422):
            logger.debug("Endpoint %s returned %d — skipping.", endpoint["url"], resp.status_code)
            return None

        # 429 = rate-limited, skip
        if resp.status_code == 429:
            logger.warning("Endpoint %s rate-limited (429) — skipping.", endpoint["url"])
            return None

        resp.raise_for_status()
        data = resp.json()
        label = _extract_label(data)
        logger.info("RapidAPI result from %s: '%s'", endpoint["url"], label)
        return label

    except requests.exceptions.Timeout:
        logger.warning("Timeout on endpoint %s", endpoint["url"])
        return None
    except requests.exceptions.HTTPError as exc:
        logger.warning("HTTP error on %s: %s", endpoint["url"], exc)
        return None
    except Exception as exc:                       # noqa: BLE001
        logger.warning("Error on %s: %s", endpoint["url"], exc)
        return None


def call_rapid_api(text: str) -> str:
    """
    Try multiple RapidAPI endpoints in sequence. Returns first successful result.
    Falls back to 'Unknown' if all fail.

    Args:
        text: The claim or headline text to evaluate.

    Returns:
        One of: 'Real', 'Fake', 'Unknown'
    """
    if not text or not text.strip():
        logger.warning("call_rapid_api: empty text, returning Unknown.")
        return "Unknown"

    # Build endpoint list: configured primary + fallbacks
    primary = {
        "url": RAPID_API_URL,
        "host": RAPID_API_HOST,
        "body_key": "text",
        "method": "POST",
    }
    endpoints = [primary] + _FALLBACK_ENDPOINTS

    for endpoint in endpoints:
        label = _try_endpoint(endpoint, text)
        if label is not None:
            return label

    logger.warning(
        "All RapidAPI endpoints failed. Applying local keyword heuristic as fallback."
    )
    return _local_heuristic(text)


def _local_heuristic(text: str) -> str:
    """
    Fast offline keyword heuristic used when all API endpoints are unavailable.
    Returns 'Fake', 'Real', or 'Uncertain'.
    """
    lower = text.lower()

    fake_signals = [
        "breaking:", "shocking", "you won't believe", "secret", "they don't want you",
        "exposed", "banned", "cover-up", "conspiracy", "hoax", "satire",
        "miracle cure", "100%", "guaranteed", "share now", "go viral",
        "deep state", "illuminati", "chemtrails", "flat earth", "crisis actor",
        "fake news", "plandemic", "rigged",
    ]
    real_signals = [
        "according to", "study shows", "researchers found", "per the report",
        "official statement", "confirmed by", "published in", "data shows",
        "statistics indicate", "governments announced", "who said", "cdc confirmed",
        "reuters", "associated press", "bbc", "nyt", "peer-reviewed",
    ]

    fake_hits = sum(1 for s in fake_signals if s in lower)
    real_hits = sum(1 for s in real_signals if s in lower)

    if fake_hits > real_hits:
        logger.info("Local heuristic → Fake (fake=%d, real=%d)", fake_hits, real_hits)
        return "Fake"
    if real_hits > fake_hits:
        logger.info("Local heuristic → Real (fake=%d, real=%d)", fake_hits, real_hits)
        return "Real"

    logger.info("Local heuristic → Uncertain (fake=%d, real=%d)", fake_hits, real_hits)
    return "Uncertain"


# ── Response parsing ─────────────────────────────────────────

def _extract_label(data: dict) -> str:
    """
    Parse the RapidAPI response and normalize to a canonical label.
    Handles many response schemas.
    """
    if not isinstance(data, dict):
        logger.warning("Unexpected RapidAPI response type: %s", type(data))
        return "Unknown"

    # Try common field names
    for field in ("label", "prediction", "result", "class", "output",
                  "verdict", "classification", "category", "fake", "real",
                  "isReal", "isFake", "is_fake", "is_real", "score"):
        value = data.get(field)
        if value is not None:
            return _normalize_label(str(value))

    # Try nested under 'data' or 'response'
    for key in ("data", "response", "result"):
        nested = data.get(key)
        if isinstance(nested, dict):
            label = _extract_label(nested)
            if label != "Unknown":
                return label

    # Try list response (some APIs return [{"label": ...}])
    for key in ("results", "items", "predictions"):
        items = data.get(key)
        if isinstance(items, list) and items:
            first = items[0]
            if isinstance(first, dict):
                return _extract_label(first)

    logger.warning("Cannot parse RapidAPI response: %s", data)
    return "Unknown"


def _normalize_label(raw: str) -> str:
    """Convert raw string or numeric code to a canonical label."""
    lower = raw.lower().strip().rstrip(".")

    # Numeric booleans
    if lower in ("1", "true", "yes"):
        # Check field name context — ambiguous, default to Fake
        # (most APIs use 1=fake convention)
        return "Fake"
    if lower in ("0", "false", "no"):
        return "Real"

    if any(k in lower for k in ("fake", "false", "mislead", "fabricat", "not real", "hoax", "satire")):
        return "Fake"
    if any(k in lower for k in ("real", "true", "fact", "credible", "legit", "reliable", "verified")):
        return "Real"

    # Score-based (some APIs return a float 0-1 where >0.5 = fake)
    try:
        score = float(raw)
        if 0.0 <= score <= 1.0:
            return "Fake" if score >= 0.5 else "Real"
    except ValueError:
        pass

    logger.warning("RapidAPI unrecognized label: '%s'", raw)
    return "Unknown"
