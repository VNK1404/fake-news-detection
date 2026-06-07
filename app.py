"""
app.py — Flask Web Interface for Fake News Detection Module
AI-Driven Digital Evidence Integrity Monitoring System
"""

import os
import sys
import json
import uuid
import logging
from pathlib import Path

from flask import Flask, request, jsonify, render_template, send_from_directory
from werkzeug.utils import secure_filename

# Ensure project root is on path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from fake_news_module.core.pipeline import fake_news_pipeline
from fake_news_module.config import SUPPORTED_IMAGE_EXTENSIONS, SUPPORTED_PDF_EXTENSIONS

# ──────────────────────────────────────────────
# App Configuration
# ──────────────────────────────────────────────
UPLOAD_FOLDER = Path(__file__).parent / "uploads"
UPLOAD_FOLDER.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = SUPPORTED_IMAGE_EXTENSIONS | SUPPORTED_PDF_EXTENSIONS
MAX_CONTENT_LENGTH = 20 * 1024 * 1024   # 20 MB

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config["UPLOAD_FOLDER"] = str(UPLOAD_FOLDER)
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH
app.secret_key = os.environ.get("FLASK_SECRET", "fnd-secret-2024-xai")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def allowed_file(filename: str) -> bool:
    suffix = Path(filename).suffix.lower()
    return suffix in ALLOWED_EXTENSIONS


# ──────────────────────────────────────────────
# Routes
# ──────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    """
    Accepts a multipart file upload, runs the detection pipeline,
    and returns a JSON result.
    """
    if "file" not in request.files:
        return jsonify({"error": "No file part in the request."}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No file selected."}), 400

    if not allowed_file(file.filename):
        return jsonify({
            "error": f"Unsupported file type. Allowed: jpg, jpeg, png, bmp, pdf"
        }), 415

    # Save with a unique name to avoid collisions
    original_name = secure_filename(file.filename)
    unique_name = f"{uuid.uuid4().hex}_{original_name}"
    save_path = UPLOAD_FOLDER / unique_name

    try:
        file.save(str(save_path))
        logger.info("File saved: %s", save_path)

        result = fake_news_pipeline(str(save_path))
        result["filename"] = original_name
        return jsonify(result), 200

    except FileNotFoundError as exc:
        logger.error("File not found: %s", exc)
        return jsonify({"error": str(exc)}), 404

    except ValueError as exc:
        logger.warning("Validation error: %s", exc)
        return jsonify({"error": str(exc)}), 422

    except RuntimeError as exc:
        logger.error("Runtime error: %s", exc)
        return jsonify({"error": str(exc)}), 500

    except Exception as exc:                      # noqa: BLE001
        logger.exception("Unexpected error: %s", exc)
        return jsonify({"error": "An unexpected error occurred."}), 500

    finally:
        # Clean up uploaded file after processing
        if save_path.exists():
            save_path.unlink(missing_ok=True)


@app.errorhandler(413)
def file_too_large(e):
    return jsonify({"error": "File too large. Maximum size is 20 MB."}), 413


# ──────────────────────────────────────────────
# Run
# ──────────────────────────────────────────────
if __name__ == "__main__":
    print("\n=== Fake News Detection - Web Interface ===")
    print("=== Open: http://127.0.0.1:5000         ===")
    print("=========================================\n")
    app.run(debug=True, host="127.0.0.1", port=5000)
