import os
import json
import logging
from typing import Dict, Any
import requests

logger = logging.getLogger(__name__)

# Environment variable for Gemini API key; fallback to config if set elsewhere
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_API_URL = os.getenv("GEMINI_API_URL", "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent")

def call_gemini_api(claim: str) -> str:
    """Send a claim to Gemini model and return a short verification label.

    The Gemini API expects a JSON payload with a `contents` field. We request a
    concise answer (e.g., "True", "False", "Uncertain").
    """
    if not GEMINI_API_KEY:
        logger.error("Gemini API key not configured")
        return "Unknown"

    headers = {
        "Content-Type": "application/json",
    }
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": f"Is the following claim true? {claim}"}]
            }
        ]
    }
    try:
        response = requests.post(
            f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
            headers=headers,
            json=payload,
            timeout=15,
        )
        response.raise_for_status()
        data = response.json()
        # Extract the first text response if available
        candidates = data.get("candidates", [])
        if not candidates:
            return "Unknown"
        parts = candidates[0].get("content", {}).get("parts", [])
        if not parts:
            return "Unknown"
        text = parts[0].get("text", "").strip().lower()
        # Simple heuristic to map common answers to standardized labels
        if "true" in text:
            return "True"
        if "false" in text:
            return "False"
        if "uncertain" in text or "cannot" in text:
            return "Uncertain"
        return "Unknown"
    except Exception as exc:
        logger.error("Gemini API exception: %s", exc)
        return "Unknown"
