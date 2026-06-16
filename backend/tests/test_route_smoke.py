import importlib
import sys
import types


def _load_app(monkeypatch):
    monkeypatch.setenv("FLASK_SECRET", "test-secret")
    monkeypatch.setitem(sys.modules, "pytesseract", types.SimpleNamespace(pytesseract=types.SimpleNamespace()))
    monkeypatch.setitem(sys.modules, "cv2", types.SimpleNamespace())
    monkeypatch.setitem(sys.modules, "pdfplumber", types.SimpleNamespace(open=lambda *_args, **_kwargs: None))
    monkeypatch.setitem(sys.modules, "requests", types.SimpleNamespace())
    if "app" in sys.modules:
        return importlib.reload(sys.modules["app"])
    return importlib.import_module("app")


def test_required_routes_are_available(monkeypatch):
    flask_app = _load_app(monkeypatch)
    client = flask_app.app.test_client()

    assert client.get("/").status_code == 200
    assert client.get("/health").status_code == 200
    assert client.post("/analyze", data={"text": "smoke"}).status_code in {200, 404, 422, 500}
    assert client.get("/download_report").status_code == 400
    assert client.get("/api/analytics").status_code == 200
    assert client.get("/api/analytics/summary").status_code == 200
    assert client.get("/api/analytics/performance").status_code == 200
