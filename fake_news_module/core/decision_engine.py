"""
core/decision_engine.py — Weighted score computation + final decision logic
AI-Driven Digital Evidence Integrity Monitoring System

Phase 1: RoBERTa (0.35) as primary signal replacing Gemini.
Phase 2: FAISS similarity search (0.25) added as second signal.
Google Fact-Check (0.20), NewsAPI (0.12), Guardian (0.08) adjusted.
"""

import logging
from typing import Dict, Tuple

from fake_news_module.config import (
    API_WEIGHTS,
    REAL_HIGH_THRESHOLD,
    FAKE_HIGH_THRESHOLD,
    UNCERTAIN_MED_THRESHOLD,
)
from fake_news_module.core.normalization import normalize_result

logger = logging.getLogger(__name__)


def compute_score(results: Dict[str, str]) -> float:
    """
    Compute a weighted aggregate score from RoBERTa + all API results.

    The score is normalized by the **sum of weights of tasks that returned
    a non-Unknown result** so that missing or failed signals don't skew the
    decision unfairly.

    Phase 1 weight breakdown:
        roberta:  0.40  — local RoBERTa binary classifier
        google:   0.25  — Google Fact Check API
        news:     0.20  — NewsAPI
        guardian: 0.15  — The Guardian Content API

    Args:
        results: Dict mapping signal name to raw label string.
                 Expected keys: 'roberta', 'google', 'news', 'guardian'

    Returns:
        Weighted average score in range [-1.0, +1.0].
        Returns 0.0 if no usable results are available.
    """
    # Pull weights from config (with safe defaults)
    weight_map = {
        "roberta":    API_WEIGHTS.get("roberta",    0.35),
        "similarity": API_WEIGHTS.get("similarity", 0.25),
        "google":     API_WEIGHTS.get("google",     0.20),
        "news":       API_WEIGHTS.get("news",       0.12),
        "guardian":   API_WEIGHTS.get("guardian",   0.08),
    }

    weighted_sum = 0.0
    active_weight = 0.0

    for signal_name, label in results.items():
        score = normalize_result(label)
        weight = weight_map.get(signal_name, 0.0)

        weighted_sum += score * weight
        active_weight += weight

        logger.debug(
            "compute_score: signal='%s' label='%s' score=%.2f weight=%.2f",
            signal_name, label, score, weight,
        )

    if active_weight == 0.0:
        logger.warning("compute_score: no active weights, returning 0.0")
        return 0.0

    final_score = weighted_sum / active_weight
    logger.info(
        "compute_score: weighted_sum=%.3f active_weight=%.2f final=%.4f",
        weighted_sum, active_weight, final_score,
    )
    return round(final_score, 4)


def final_decision(score: float) -> Tuple[str, str]:
    """
    Apply threshold rules to the weighted score and return decision + confidence.

    Decision Rules:
        score > +REAL_HIGH_THRESHOLD       → Real,      High confidence
        score < -FAKE_HIGH_THRESHOLD       → Fake,      High confidence
        |score| > UNCERTAIN_MED_THRESHOLD  → Real/Fake, Medium confidence
        else                               → Uncertain, Low confidence

    Args:
        score: Weighted aggregate score from compute_score().

    Returns:
        Tuple of (decision: str, confidence: str)
        decision   ∈ {'Real', 'Fake', 'Uncertain'}
        confidence ∈ {'High', 'Medium', 'Low'}
    """
    if score > REAL_HIGH_THRESHOLD:
        decision, confidence = "Real", "High"
    elif score < FAKE_HIGH_THRESHOLD:
        decision, confidence = "Fake", "High"
    elif abs(score) > UNCERTAIN_MED_THRESHOLD:
        decision = "Real" if score > 0 else ("Fake" if score < 0 else "Uncertain")
        confidence = "Medium"
    else:
        decision, confidence = "Uncertain", "Low"

    logger.info(
        "final_decision: score=%.4f → decision='%s' confidence='%s'",
        score, decision, confidence,
    )
    return decision, confidence
