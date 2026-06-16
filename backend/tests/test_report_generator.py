from __future__ import annotations

import io
import sys
import types
from pathlib import Path

from pypdf import PdfReader


def _install_pipeline_import_stubs(monkeypatch):
    monkeypatch.setenv("FLASK_SECRET", "test-secret")
    monkeypatch.setitem(sys.modules, "pytesseract", types.SimpleNamespace(pytesseract=types.SimpleNamespace()))
    monkeypatch.setitem(sys.modules, "cv2", types.SimpleNamespace())
    monkeypatch.setitem(sys.modules, "pdfplumber", types.SimpleNamespace(open=lambda *_args, **_kwargs: None))
    monkeypatch.setitem(sys.modules, "requests", types.SimpleNamespace())


def _sample_result():
    return {
        "claim": "Vaccines cause autism",
        "final_decision": "Fake",
        "confidence": "High",
        "score": -0.91,
        "api_results": {
            "roberta": "Fake",
            "similarity": "Fake",
            "google_fact_check": "False",
            "news_api": "Uncertain",
            "guardian": "Unknown",
            "source": "Fake",
        },
        "explanation": {
            "verdict": "Fake",
            "confidence": "High",
            "confidence_pct": 91,
            "reasons": [
                "The weighted analysis of 4 verification signals produced a strong consensus verdict of FAKE.",
                "RoBERTa classified the claim as Fake.",
                "Semantic similarity search found matching false claims.",
            ],
            "confidence_breakdown": {
                "roberta": {"weight_pct": 35, "label": "Fake", "contributed": True, "direction": "FAKE"},
                "similarity": {"weight_pct": 25, "label": "Fake", "contributed": True, "direction": "FAKE"},
                "google": {"weight_pct": 20, "label": "False", "contributed": True, "direction": "FAKE"},
                "news": {"weight_pct": 12, "label": "Uncertain", "contributed": False, "direction": "NEUTRAL"},
                "guardian": {"weight_pct": 8, "label": "Unknown", "contributed": False, "direction": "NEUTRAL"},
                "source": {"weight_pct": 10, "label": "Low", "contributed": True, "direction": "FAKE"},
            },
            "evidence": {
                "similarity_evidence": {
                    "top_matches": [
                        {"title": "No evidence vaccines cause autism", "score": 0.94, "label": "Real"},
                        {"title": "Debunking vaccine myths", "score": 0.89, "label": "Real"},
                    ],
                    "description": "FAISS semantic similarity search",
                },
                "factcheck_evidence": {
                    "label": "False",
                    "source": "Google Fact Check Tools API",
                    "description": "Fact check records indicate the claim is false.",
                },
                "source_evidence": {
                    "source_score": 0.12,
                    "sources_found": [{"domain": "example.com", "score": 0.12}],
                    "description": "Average credibility of cited domains.",
                },
                "roberta_evidence": {
                    "label": "Fake",
                    "description": "Local transformer-based classifier.",
                },
                "newsapi_evidence": {
                    "label": "Uncertain",
                    "description": "Recent news coverage was inconclusive.",
                },
            },
        },
    }


def _extract_pdf_text(pdf_bytes: bytes) -> str:
    reader = PdfReader(io.BytesIO(pdf_bytes))
    return "\n".join((page.extract_text() or "") for page in reader.pages)


def test_report_generator_creates_populated_pdf(tmp_path):
    from fake_news_module.reporting.report_generator import build_report_payload, generate_pdf_report

    payload = build_report_payload(_sample_result(), analysis_id="analysis-123")
    output = tmp_path / "report.pdf"
    generate_pdf_report(payload, output)

    assert output.exists()
    assert output.stat().st_size > 0

    text = _extract_pdf_text(output.read_bytes())
    assert "Fake News Detector" in text
    assert "Vaccines cause autism" in text
    assert "Fake" in text
    assert "91%" in text
    assert "No evidence vaccines cause autism" in text
    assert "RoBERTa classified the claim as Fake." in text


def test_download_report_endpoint_returns_pdf(monkeypatch, tmp_path):
    _install_pipeline_import_stubs(monkeypatch)
    import app as flask_app

    flask_app.REPORTS_FOLDER = Path(tmp_path / "reports")
    flask_app.REPORTS_FOLDER.mkdir(exist_ok=True)

    client = flask_app.app.test_client()
    response = client.post("/download_report", json={"result": _sample_result()})

    assert response.status_code == 200
    assert response.mimetype == "application/pdf"
    assert len(response.data) > 0

    text = _extract_pdf_text(response.data)
    assert "Vaccines cause autism" in text
    assert "Fake" in text
    assert "91%" in text
    assert "No evidence vaccines cause autism" in text
    assert "RoBERTa classified the claim as Fake." in text
