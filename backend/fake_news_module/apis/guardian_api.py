import os
import logging
import requests
from fake_news_module.config import GUARDIAN_API_KEY, GUARDIAN_API_URL

logger = logging.getLogger(__name__)

def call_guardian_api(claim: str) -> str:
    """Query The Guardian content API for the claim and return a simple label.

    The API returns a list of matching articles. If any article is found we
    return "True" (indicating the claim appears in reputable sources), otherwise
    "False". Errors are logged and result in "Unknown".
    """
    if not GUARDIAN_API_KEY:
        logger.error("Guardian API key not configured")
        return "Unknown"
    params = {
        "q": claim,
        "api-key": GUARDIAN_API_KEY,
        "page-size": 5,
    }
    try:
        response = requests.get(GUARDIAN_API_URL, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        results = data.get("response", {}).get("results", [])
        if results:
            return "True"
        return "False"
    except Exception as exc:
        logger.error("Guardian API exception: %s", exc)
        return "Unknown"
