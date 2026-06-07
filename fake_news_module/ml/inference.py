"""
fake_news_module/ml/inference.py
=================================
Thin inference helper that bridges the pipeline with the RoBERTa classifier.

This module is the **only** import the pipeline needs from the ml sub-package.
It wraps `roberta_classifier.predict()` and returns the same simple string
labels ("Real", "Fake", "Unknown") that all other API wrappers return, making
it a drop-in addition to `_API_TASKS` in pipeline.py.

Usage (internal)
----------------
    from fake_news_module.ml.inference import call_roberta

    label = call_roberta("Vaccines cause autism")
    # → "Fake"
"""

import logging
from fake_news_module.ml.roberta_classifier import predict

logger = logging.getLogger(__name__)


def call_roberta(claim: str) -> str:
    """
    Run RoBERTa inference on a claim and return a standardized label string.

    This function is intentionally simple — all complexity lives in
    `roberta_classifier.predict()`. The pipeline calls this exactly like
    any other API wrapper.

    Args:
        claim: The extracted news claim text.

    Returns:
        One of:
            "Real"    — model classified as real news (class 1)
            "Fake"    — model classified as fake news (class 0)
            "Unknown" — model not loaded / inference error
    """
    if not claim or not claim.strip():
        logger.warning("call_roberta: empty claim — returning Unknown.")
        return "Unknown"

    result = predict(claim)
    label = result.get("label", "Unknown")
    confidence = result.get("confidence", 0.0)

    logger.info(
        "call_roberta: label='%s' confidence=%.4f (fake=%.4f real=%.4f)",
        label,
        confidence,
        result.get("fake_prob", 0.0),
        result.get("real_prob", 0.0),
    )
    return label
