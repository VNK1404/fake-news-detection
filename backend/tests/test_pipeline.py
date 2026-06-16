import pytest


def _install_pipeline_import_stubs(monkeypatch):
    import sys
    import types

    monkeypatch.setitem(sys.modules, "pytesseract", types.SimpleNamespace(pytesseract=types.SimpleNamespace()))
    monkeypatch.setitem(sys.modules, "cv2", types.SimpleNamespace())
    monkeypatch.setitem(sys.modules, "pdfplumber", types.SimpleNamespace(open=lambda *_args, **_kwargs: None))
    monkeypatch.setitem(sys.modules, "requests", types.SimpleNamespace())



def test_pipeline_invalid_file(monkeypatch):
    _install_pipeline_import_stubs(monkeypatch)
    from fake_news_module.core.pipeline import fake_news_pipeline

    with pytest.raises(FileNotFoundError):
        fake_news_pipeline("nonexistent_file.jpg")
