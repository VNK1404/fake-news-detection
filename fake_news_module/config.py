"""
config.py — Central configuration for Fake News Detection Module
AI-Driven Digital Evidence Integrity Monitoring System
"""

import os
import logging

# ──────────────────────────────────────────────
# LOGGING CONFIGURATION
# ──────────────────────────────────────────────
LOG_LEVEL = logging.DEBUG
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

logging.basicConfig(
    level=LOG_LEVEL,
    format=LOG_FORMAT,
    datefmt=LOG_DATE_FORMAT,
)

# ──────────────────────────────────────────────
# API KEYS (override via environment variables for production)
# ──────────────────────────────────────────────
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "")
NEWS_API_KEY = os.environ.get("NEWS_API_KEY", "")
GUARDIAN_API_KEY = os.environ.get("GUARDIAN_API_KEY", "")

# ──────────────────────────────────────────────
# ML MODEL — RoBERTa CLASSIFIER (Phase 1)
# ──────────────────────────────────────────────
import pathlib as _pathlib

# Directory where the fine-tuned RoBERTa weights are saved.
# train.py writes here; roberta_classifier.py reads from here.
ROBERTA_MODEL_DIR: str = str(
    _pathlib.Path(__file__).parent / "ml" / "saved_model"
)

# Set to False to disable RoBERTa and exclude it from the pipeline
# (useful during development before the model is trained).
ROBERTA_ENABLED: bool = True

# ──────────────────────────────────────────────
# SIMILARITY SEARCH — FAISS + Sentence-Transformers (Phase 2)
# ──────────────────────────────────────────────

# Directory containing faiss_index.bin, labels.npy, titles.npy
SIMILARITY_INDEX_DIR: str = str(
    _pathlib.Path(__file__).parent / "similarity" / "index"
)

# Set to False to disable similarity search (e.g. before index is built)
SIMILARITY_ENABLED: bool = True

# Number of nearest neighbours to retrieve from the FAISS index
SIMILARITY_TOP_K: int = 5

# Minimum cosine similarity score (0–1) to count a match as credible.
# Matches below this threshold are ignored in the majority vote.
SIMILARITY_MIN_SCORE: float = 0.60

# ──────────────────────────────────────────────
# API ENDPOINTS
# ──────────────────────────────────────────────
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

GOOGLE_FACT_CHECK_URL = "https://factchecktools.googleapis.com/v1alpha1/claims:search"

NEWS_API_URL = "https://newsapi.org/v2/everything"

GUARDIAN_API_URL = "https://content.guardianapis.com/search"

# ──────────────────────────────────────────────
# DECISION ENGINE WEIGHTS
# ──────────────────────────────────────────────
# Phase 2 weights — Similarity search added as second signal
# Note: these 5 weights must sum to 1.00; source credibility uses SOURCE_WEIGHT separately.
API_WEIGHTS = {
    "roberta":    0.35,   # Local RoBERTa classifier        (Phase 1)
    "similarity": 0.25,   # FAISS similarity search         (Phase 2)
    "google":     0.20,   # Google Fact Check API
    "news":       0.12,   # NewsAPI
    "guardian":   0.08,   # The Guardian Content API
}

# Source credibility signal weight (Phase 4) — kept separate so decision_engine
# can normalise correctly when source data is unavailable.
SOURCE_WEIGHT: float = 0.10

# ──────────────────────────────────────────────
# DECISION THRESHOLDS
# ──────────────────────────────────────────────
REAL_HIGH_THRESHOLD = 0.3       # score > +0.3 → Real, High confidence
FAKE_HIGH_THRESHOLD = -0.3      # score < -0.3 → Fake, High confidence
UNCERTAIN_MED_THRESHOLD = 0.1   # abs(score) > 0.1 → Uncertain, Medium

# ──────────────────────────────────────────────
# TEXT VALIDATION RULES
# ──────────────────────────────────────────────
MIN_TEXT_LENGTH = 30
MAX_NOISE_RATIO = 0.4
CLAIM_MIN_LENGTH = 30
CLAIM_FALLBACK_LENGTH = 200

# ──────────────────────────────────────────────
# NEWS API — TRUSTED SOURCES
# ──────────────────────────────────────────────
TRUSTED_SOURCES = [
    "bbc",
    "reuters",
    "cnn",
    "ndtv",
    "the hindu",
    "associated press",
    "the guardian",
    "al jazeera",
    "abc news",
    "nbc news",
]
TRUSTED_SOURCE_THRESHOLD = 2    # >= 2 trusted sources → Real

# ──────────────────────────────────────────────
# HTTP SETTINGS
# ──────────────────────────────────────────────
REQUEST_TIMEOUT = 15            # seconds
MAX_RETRIES = 2

# ──────────────────────────────────────────────
# SUPPORTED FILE TYPES
# ──────────────────────────────────────────────
SUPPORTED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp"}
SUPPORTED_PDF_EXTENSIONS = {".pdf"}

# ──────────────────────────────────────────────
# TESSERACT PATH (Windows default; override if needed)
# ──────────────────────────────────────────────
TESSERACT_CMD = os.environ.get(
    "TESSERACT_CMD",
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)
