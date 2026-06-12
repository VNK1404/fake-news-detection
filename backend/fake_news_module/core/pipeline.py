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
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Dict

from fake_news_module.ocr.extractor import extract_text
from fake_news_module.processing.text_cleaner import clean_text
from fake_news_module.processing.validator import validate_text
from fake_news_module.processing.claim_extractor import extract_main_text
from fake_news_module.apis.async_client import run_external_apis_async
from fake_news_module.source_scoring.source_scorer import score_source_evidence
from fake_news_module.explainability.explanation_engine import generate_explanation
from fake_news_module.core.decision_engine import compute_score, final_decision
from fake_news_module.analytics import get_analytics_service
from fake_news_module.cache import get_cache_manager
from fake_news_module.reporting.report_generator import build_report_payload
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


def _call_similarity(claim: str) -> tuple:
    """Call the FAISS similarity searcher. Returns tuple (label, top_matches)."""
    if not SIMILARITY_ENABLED or not _SIMILARITY_AVAILABLE:
        logger.info("Similarity search disabled or unavailable — returning Uncertain.")
        return ("Uncertain", [])
    try:
        from fake_news_module.similarity.searcher import search
        res = search(claim)
        return (res.get("label", "Uncertain"), res.get("top_matches", []))
    except Exception as exc:                          # noqa: BLE001
        logger.error("Similarity search exception: %s", exc)
        return ("Uncertain", [])


def _call_external_apis(claim: str) -> Dict[str, Any]:
    """Run external APIs concurrently through the aiohttp async client."""
    try:
        return asyncio.run(run_external_apis_async(claim))
    except Exception as exc:                          # noqa: BLE001
        logger.error("Async external API execution exception: %s", exc)
        return {
            "google": "Unknown",
            "news": ("Unknown", []),
            "guardian": "Unknown",
        }


# Task registry: name → callable
# RoBERTa and Similarity run in the same thread pool as the API calls.
_API_TASKS: Dict[str, Any] = {
    "roberta":       _call_roberta,
    "similarity":    _call_similarity,
    "external_apis": _call_external_apis,
}


def _run_apis_parallel(claim: str) -> tuple[Dict[str, Any], Dict[str, float]]:
    """
    Fire all API calls AND RoBERTa inference concurrently using a thread pool.

    Returns:
        Dict of {task_name: result}
    """
    results: Dict[str, Any] = {}
    timings: Dict[str, float] = {}

    def _timed_call(name: str, fn: Any) -> Any:
        start = time.perf_counter()
        try:
            return fn(claim)
        finally:
            timings[name] = time.perf_counter() - start

    with ThreadPoolExecutor(max_workers=5, thread_name_prefix="api_worker") as pool:
        futures = {
            pool.submit(_timed_call, name, fn): name
            for name, fn in _API_TASKS.items()
        }
        for future in as_completed(futures):
            name = futures[future]
            try:
                result = future.result()
                if name == "external_apis" and isinstance(result, dict):
                    results.update(result)
                else:
                    results[name] = result
            except Exception as exc:              # noqa: BLE001
                logger.error("Task '%s' raised exception: %s", name, exc)
                results[name] = "Unknown"

    return results, timings


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

    cache = get_cache_manager()
    cached_result = cache.get_pipeline_result(claim)
    if isinstance(cached_result, dict):
        elapsed = time.perf_counter() - pipeline_start
        logger.info("PIPELINE CACHE HIT in %.2fs | claim_hash=%s", elapsed, cache.claim_hash(claim))
        get_analytics_service().record_analysis(
            cached_result,
            pipeline_duration=elapsed,
            stage_timings={},
            cache_hit=True,
        )
        return cached_result

    # ── STEP 5: Run all tasks in parallel ─────────────────────────
    logger.info("[Step 5/6] Running RoBERTa + APIs in parallel …")
    parallel_result = _run_apis_parallel(claim)
    if isinstance(parallel_result, tuple) and len(parallel_result) == 2:
        raw_labels, stage_timings = parallel_result
    else:
        raw_labels = parallel_result
        stage_timings = {}

    # Unpack rich results for similarity and news
    similarity_label = "Uncertain"
    similarity_matches = []
    if isinstance(raw_labels.get("similarity"), tuple):
        similarity_label, similarity_matches = raw_labels["similarity"]
        raw_labels["similarity"] = similarity_label
    else:
        similarity_label = raw_labels.get("similarity", "Uncertain")

    news_label = "Unknown"
    news_articles = []
    if isinstance(raw_labels.get("news"), tuple):
        news_label, news_articles = raw_labels["news"]
        raw_labels["news"] = news_label
    else:
        news_label = raw_labels.get("news", "Unknown")

    # Compute source credibility from claim text and API evidence URLs.
    source_credibility = score_source_evidence([claim, *news_articles])
    source_score_numeric = source_credibility["source_score"]
    if source_score_numeric >= 0.6:
        source_label = "Real"
    elif source_score_numeric <= 0.4:
        source_label = "Fake"
    else:
        source_label = "Uncertain"
    raw_labels["source"] = source_label

    # Map internal keys to output-friendly names
    api_results_output = {
        "roberta":           raw_labels.get("roberta",     "Unknown"),
        "similarity":        similarity_label,
        "google_fact_check": raw_labels.get("google",      "Unknown"),
        "news_api":          news_label,
        "guardian":          raw_labels.get("guardian",    "Unknown"),
        "source":            raw_labels.get("source",     "Unknown"),
    }

    # Keys for decision engine must match API_WEIGHTS keys in config.py
    decision_input = {
        "roberta":    raw_labels.get("roberta",    "Unknown"),
        "similarity": raw_labels.get("similarity", "Uncertain"),
        "google":     raw_labels.get("google",     "Unknown"),
        "news":       raw_labels.get("news",       "Unknown"),
        "guardian":   raw_labels.get("guardian",   "Unknown"),
        "source":     raw_labels.get("source",     "Unknown"),
    }

    # ── STEP 6: Score + Decision ──────────────────────────────────
    logger.info("[Step 6/6] Computing score and final decision …")
    score = compute_score(decision_input)
    decision, confidence = final_decision(score)
    # Generate explanation for UI
    explanation = generate_explanation(
        claim=claim,
        verdict=decision,
        confidence=confidence,
        score=score,
        api_results=decision_input,
        similarity_top_matches=similarity_matches,
        news_articles=news_articles,
        source_credibility=source_credibility,
    )

    elapsed = time.perf_counter() - pipeline_start
    logger.info(
        "PIPELINE COMPLETE in %.2fs | decision='%s' | confidence='%s' | score=%.4f",
        elapsed, decision, confidence, score,
    )
    logger.info("=" * 60)

    result = {
        "extracted_text": raw_text[:2000],   # Truncate for readability
        "claim":          claim,
        "api_results":    api_results_output,
        "explanation":      explanation,
        "source_score":    source_score_numeric,
        "score":          score,
        "final_decision": decision,
        "confidence":     confidence,
    }
    _ = build_report_payload(result)
    cache.set_pipeline_result(claim, result)
    get_analytics_service().record_analysis(
        result,
        pipeline_duration=elapsed,
        stage_timings=stage_timings,
        cache_hit=False,
    )
    return result
