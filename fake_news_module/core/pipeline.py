"""
core/pipeline.py — Main orchestration pipeline
AI-Driven Digital Evidence Integrity Monitoring System

Phase 1 upgrade: RoBERTa ML classifier added as primary signal (weight=0.35)
Phase 2 upgrade: FAISS similarity search added as second signal (weight=0.25)
alongside Google Fact-Check, NewsAPI, and The Guardian.

Coordinates:
    OCR → Cleaning → Validation → Claim Extraction →
    API Calls + ML Inference + Similarity Search (parallel) → Normalization → Decision → JSON Output
"""

import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Dict

from fake_news_module.ocr.extractor import extract_text
from fake_news_module.processing.text_cleaner import clean_text
from fake_news_module.processing.validator import validate_text
from fake_news_module.processing.claim_extractor import extract_main_text
from fake_news_module.apis.gemini_api import call_gemini_api
from fake_news_module.apis.google_api import call_google_fact_check
from fake_news_module.apis.news_api import call_news_api, analyze_news_results
from fake_news_module.apis.guardian_api import call_guardian_api
from fake_news_module.core.decision_engine import compute_score, final_decision
from fake_news_module.config import ROBERTA_ENABLED, SIMILARITY_ENABLED

# Phase 1: RoBERTa ML inference
try:
    from fake_news_module.ml.inference import call_roberta as _roberta_fn
    _ROBERTA_AVAILABLE = True
except ImportError:
    _ROBERTA_AVAILABLE = False

# Phase 2: FAISS similarity search
try:
    from fake_news_module.similarity.inference import call_similarity as _similarity_fn
    _SIMILARITY_AVAILABLE = True
except ImportError:
    _SIMILARITY_AVAILABLE = False

logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────
# Internal API/ML helpers
# ──────────────────────────────────────────────

def _call_roberta(claim: str) -> str:
    """Call the local RoBERTa classifier. Returns 'Unknown' if disabled or unavailable."""
    if not ROBERTA_ENABLED or not _ROBERTA_AVAILABLE:
        logger.info("RoBERTa disabled or unavailable — returning Unknown.")
        return "Unknown"
    try:
        return _roberta_fn(claim)
    except Exception as exc:                          # noqa: BLE001
        logger.error("RoBERTa inference exception: %s", exc)
        return "Unknown"


def _call_similarity(claim: str) -> str:
    """Call the FAISS similarity searcher. Returns 'Uncertain' if disabled or unavailable."""
    if not SIMILARITY_ENABLED or not _SIMILARITY_AVAILABLE:
        logger.info("Similarity search disabled or unavailable — returning Uncertain.")
        return "Uncertain"
    try:
        return _similarity_fn(claim)
    except Exception as exc:                          # noqa: BLE001
        logger.error("Similarity search exception: %s", exc)
        return "Uncertain"


def _call_google(claim: str) -> str:
    try:
        return call_google_fact_check(claim)
    except Exception as exc:                          # noqa: BLE001
        logger.error("Google Fact Check exception: %s", exc)
        return "Unknown"


def _call_news(claim: str) -> str:
    try:
        articles = call_news_api(claim)
        return analyze_news_results(articles)
    except Exception as exc:                          # noqa: BLE001
        logger.error("NewsAPI exception: %s", exc)
        return "Unknown"


def _call_guardian(claim: str) -> str:
    try:
        return call_guardian_api(claim)
    except Exception as exc:                          # noqa: BLE001
        logger.error("Guardian API exception: %s", exc)
        return "Unknown"


# Task registry: name → callable
# RoBERTa and Similarity run in the same thread pool as the API calls.
_API_TASKS: Dict[str, Any] = {
    "roberta":    _call_roberta,
    "similarity": _call_similarity,
    "google":     _call_google,
    "news":       _call_news,
    "guardian":   _call_guardian,
}


def _run_apis_parallel(claim: str) -> Dict[str, str]:
    """
    Fire all API calls AND RoBERTa inference concurrently using a thread pool.

    Returns:
        Dict of {task_name: label_string}
    """
    results: Dict[str, str] = {}

    with ThreadPoolExecutor(max_workers=5, thread_name_prefix="api_worker") as pool:
        futures = {
            pool.submit(fn, claim): name
            for name, fn in _API_TASKS.items()
        }
        for future in as_completed(futures):
            name = futures[future]
            try:
                results[name] = future.result()
            except Exception as exc:              # noqa: BLE001
                logger.error("Task '%s' raised exception: %s", name, exc)
                results[name] = "Unknown"

    return results


# ──────────────────────────────────────────────
# Main Pipeline
# ──────────────────────────────────────────────

def fake_news_pipeline(file_path: str) -> Dict[str, Any]:
    """
    End-to-end fake news detection pipeline.

    Args:
        file_path: Absolute path to an image (.jpg/.png) or PDF (.pdf) file.

    Returns:
        A JSON-serializable dict:
        {
            "extracted_text":  str,
            "claim":           str,
            "api_results": {
                "roberta":           str,   # Phase 1: local RoBERTa classifier
                "google_fact_check": str,
                "news_api":          str,
                "guardian":          str,
            },
            "score":           float,
            "final_decision":  str,
            "confidence":      str,
        }

    Raises:
        FileNotFoundError: If file does not exist.
        ValueError: If file type is unsupported or OCR output is invalid.
        RuntimeError: On unrecoverable internal error.
    """
    pipeline_start = time.perf_counter()
    logger.info("=" * 60)
    logger.info("PIPELINE START: %s", file_path)
    logger.info("=" * 60)

    # ── STEP 1: Extract text ──────────────────────────────────────
    logger.info("[Step 1/6] Extracting text from file …")
    raw_text = extract_text(file_path)

    if not raw_text:
        raise ValueError("Text extraction returned empty output. Check the input file.")

    # ── STEP 2: Clean text ────────────────────────────────────────
    logger.info("[Step 2/6] Cleaning text …")
    cleaned = clean_text(raw_text)

    # ── STEP 3: Validate OCR quality ─────────────────────────────
    logger.info("[Step 3/6] Validating text quality …")
    is_valid, reason = validate_text(cleaned)
    if not is_valid:
        raise ValueError(f"Text quality validation failed: {reason}")

    # ── STEP 4: Extract main claim ────────────────────────────────
    logger.info("[Step 4/6] Extracting main claim …")
    claim = extract_main_text(cleaned)

    # ── STEP 5: Run all tasks in parallel ─────────────────────────
    logger.info("[Step 5/6] Running RoBERTa + APIs in parallel …")
    raw_labels = _run_apis_parallel(claim)

    # Map internal keys to output-friendly names
    api_results_output = {
        "roberta":           raw_labels.get("roberta",     "Unknown"),
        "similarity":        raw_labels.get("similarity",  "Uncertain"),
        "google_fact_check": raw_labels.get("google",      "Unknown"),
        "news_api":          raw_labels.get("news",        "Unknown"),
        "guardian":          raw_labels.get("guardian",    "Unknown"),
    }

    # Keys for decision engine must match API_WEIGHTS keys in config.py
    decision_input = {
        "roberta":    raw_labels.get("roberta",    "Unknown"),
        "similarity": raw_labels.get("similarity", "Uncertain"),
        "google":     raw_labels.get("google",     "Unknown"),
        "news":       raw_labels.get("news",       "Unknown"),
        "guardian":   raw_labels.get("guardian",   "Unknown"),
    }

    # ── STEP 6: Score + Decision ──────────────────────────────────
    logger.info("[Step 6/6] Computing score and final decision …")
    score = compute_score(decision_input)
    decision, confidence = final_decision(score)

    elapsed = time.perf_counter() - pipeline_start
    logger.info(
        "PIPELINE COMPLETE in %.2fs | decision='%s' | confidence='%s' | score=%.4f",
        elapsed, decision, confidence, score,
    )
    logger.info("=" * 60)

    return {
        "extracted_text": raw_text[:2000],   # Truncate for readability
        "claim":          claim,
        "api_results":    api_results_output,
        "score":          score,
        "final_decision": decision,
        "confidence":     confidence,
    }
