import io
import importlib
import sys
import types


def _install_app_import_stubs(monkeypatch):
    monkeypatch.setenv("FLASK_SECRET", "test-secret")
    monkeypatch.setitem(sys.modules, "pytesseract", types.SimpleNamespace(pytesseract=types.SimpleNamespace()))
    monkeypatch.setitem(sys.modules, "cv2", types.SimpleNamespace())
    monkeypatch.setitem(sys.modules, "pdfplumber", types.SimpleNamespace(open=lambda *_args, **_kwargs: None))
    monkeypatch.setitem(sys.modules, "requests", types.SimpleNamespace())


def _load_app(monkeypatch):
    _install_app_import_stubs(monkeypatch)
    if "app" in sys.modules:
        return importlib.reload(sys.modules["app"])
    return importlib.import_module("app")


def _sample_result(claim="Text claim for route test"):
    return {
        "claim": claim,
        "final_decision": "Uncertain",
        "confidence": "Low",
        "score": 0.0,
        "api_results": {"roberta": "Unknown"},
        "explanation": {"reasons": [], "confidence_breakdown": {}, "evidence": {}},
    }


def test_health_route_returns_healthy_payload(monkeypatch):
    flask_app = _load_app(monkeypatch)
    response = flask_app.app.test_client().get("/health")

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["status"] == "healthy"
    assert payload["service"] == "fake-news-detection"
    assert payload["timestamp"]


def test_analyze_accepts_text_and_sets_analysis_header(monkeypatch):
    flask_app = _load_app(monkeypatch)
    monkeypatch.setattr(flask_app, "fake_news_pipeline", lambda claim: _sample_result(claim))

    response = flask_app.app.test_client().post("/analyze", data={"text": "Vaccines cause autism"})

    assert response.status_code == 200
    assert response.get_json()["claim"] == "Vaccines cause autism"
    assert response.headers.get("X-Analysis-Id")


def test_analyze_rejects_invalid_file(monkeypatch):
    flask_app = _load_app(monkeypatch)
    client = flask_app.app.test_client()

    response = client.post(
        "/analyze",
        data={"file": (io.BytesIO(b"bad"), "claim.exe")},
        content_type="multipart/form-data",
    )

    assert response.status_code == 415


def test_download_report_without_payload_returns_bad_request(monkeypatch):
    flask_app = _load_app(monkeypatch)
    response = flask_app.app.test_client().get("/download_report")

    assert response.status_code == 400
