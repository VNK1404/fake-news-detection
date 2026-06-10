import asyncio
import sys
import time
import types

import aiohttp

from fake_news_module.apis import async_client


def _install_pipeline_import_stubs(monkeypatch):
    monkeypatch.setitem(sys.modules, "pytesseract", types.SimpleNamespace(pytesseract=types.SimpleNamespace()))
    monkeypatch.setitem(sys.modules, "cv2", types.SimpleNamespace())
    monkeypatch.setitem(sys.modules, "pdfplumber", types.SimpleNamespace(open=lambda *_args, **_kwargs: None))
    monkeypatch.setitem(sys.modules, "requests", types.SimpleNamespace())


def test_external_apis_execute_concurrently(monkeypatch):
    async def slow_google(_session, _claim):
        await asyncio.sleep(0.05)
        return "Real"

    async def slow_news(_session, _claim):
        await asyncio.sleep(0.05)
        return ("Real", [{"url": "https://reuters.com/story"}])

    async def slow_guardian(_session, _claim):
        await asyncio.sleep(0.05)
        return "True"

    monkeypatch.setattr(async_client, "async_google_factcheck", slow_google)
    monkeypatch.setattr(async_client, "async_newsapi", slow_news)
    monkeypatch.setattr(async_client, "async_guardian", slow_guardian)

    start = time.perf_counter()
    result = asyncio.run(async_client.run_external_apis_async("claim"))
    elapsed = time.perf_counter() - start

    assert elapsed < 0.12
    assert result == {
        "google": "Real",
        "news": ("Real", [{"url": "https://reuters.com/story"}]),
        "guardian": "True",
    }


def test_external_api_failure_returns_neutral_result(monkeypatch):
    async def ok_google(_session, _claim):
        return "Real"

    async def ok_news(_session, _claim):
        return ("Uncertain", [])

    async def failing_guardian(_session, _claim):
        raise RuntimeError("guardian unavailable")

    monkeypatch.setattr(async_client, "async_google_factcheck", ok_google)
    monkeypatch.setattr(async_client, "async_newsapi", ok_news)
    monkeypatch.setattr(async_client, "async_guardian", failing_guardian)

    result = asyncio.run(async_client.run_external_apis_async("claim"))

    assert result["google"] == "Real"
    assert result["news"] == ("Uncertain", [])
    assert result["guardian"] == "Unknown"


def test_fetch_json_retries_with_exponential_backoff(monkeypatch):
    calls = {"count": 0}
    sleeps = []

    async def fake_sleep(delay):
        sleeps.append(delay)

    class ResponseContext:
        async def __aenter__(self):
            calls["count"] += 1
            if calls["count"] < 3:
                raise aiohttp.ClientError("temporary")
            return self

        async def __aexit__(self, *_args):
            return False

        def raise_for_status(self):
            return None

        async def json(self):
            return {"ok": True}

    class Session:
        def get(self, *_args, **_kwargs):
            return ResponseContext()

    monkeypatch.setattr(async_client.asyncio, "sleep", fake_sleep)
    monkeypatch.setattr(async_client, "MAX_RETRIES", 3)

    result = asyncio.run(async_client._fetch_json(Session(), "UnitTest", "https://example.test", {}))

    assert result == {"ok": True}
    assert calls["count"] == 3
    assert sleeps == [1, 2]


def test_fetch_json_timeout_returns_none(monkeypatch):
    sleeps = []

    async def fake_sleep(delay):
        sleeps.append(delay)

    class TimeoutContext:
        async def __aenter__(self):
            raise asyncio.TimeoutError()

        async def __aexit__(self, *_args):
            return False

    class Session:
        def get(self, *_args, **_kwargs):
            return TimeoutContext()

    monkeypatch.setattr(async_client.asyncio, "sleep", fake_sleep)
    monkeypatch.setattr(async_client, "MAX_RETRIES", 2)

    result = asyncio.run(async_client._fetch_json(Session(), "TimeoutTest", "https://example.test", {}))

    assert result is None
    assert sleeps == [1]


def test_pipeline_async_integration_preserves_json_schema(monkeypatch, tmp_path):
    _install_pipeline_import_stubs(monkeypatch)
    from fake_news_module.core import pipeline

    sample = tmp_path / "sample.txt"
    sample.write_text("placeholder", encoding="utf-8")

    async def fake_external(_claim):
        await asyncio.sleep(0)
        return {
            "google": "Real",
            "news": ("Real", [{"title": "Trusted story", "url": "https://reuters.com/story"}]),
            "guardian": "True",
        }

    monkeypatch.setattr(pipeline, "extract_text", lambda _path: "Reuters confirms claim at https://reuters.com/story")
    monkeypatch.setattr(pipeline, "clean_text", lambda text: text)
    monkeypatch.setattr(pipeline, "validate_text", lambda text: (True, "ok"))
    monkeypatch.setattr(pipeline, "extract_main_text", lambda text: text)
    monkeypatch.setattr(pipeline, "_call_roberta", lambda _claim: "Real")
    monkeypatch.setattr(
        pipeline,
        "_call_similarity",
        lambda _claim: ("Real", [{"title": "Similar trusted claim", "label": "Real", "score": 0.93}]),
    )
    monkeypatch.setattr(pipeline, "run_external_apis_async", fake_external)
    monkeypatch.setattr(
        pipeline,
        "_API_TASKS",
        {
            "roberta": pipeline._call_roberta,
            "similarity": pipeline._call_similarity,
            "external_apis": pipeline._call_external_apis,
        },
    )

    result = pipeline.fake_news_pipeline(str(sample))

    assert set(result) >= {
        "extracted_text",
        "claim",
        "api_results",
        "explanation",
        "source_score",
        "score",
        "final_decision",
        "confidence",
    }
    assert result["api_results"] == {
        "roberta": "Real",
        "similarity": "Real",
        "google_fact_check": "Real",
        "news_api": "Real",
        "guardian": "True",
        "source": "Real",
    }
    assert result["explanation"]["evidence"]["similarity_evidence"]["top_matches"][0]["score"] == 0.93
    assert result["explanation"]["evidence"]["source_evidence"]["sources_found"][0]["domain"] == "reuters.com"


def test_frontend_async_release_contract_is_unchanged():
    html = open("templates/index.html", encoding="utf-8").read()

    assert "lbl-roberta" in html
    assert "lbl-similarity" in html
    assert "lbl-google" in html
    assert "lbl-news" in html
    assert "lbl-guardian" in html
    assert "lbl-source" in html
    assert "similar-claims-list" in html
    assert "source-evidence-list" in html
    assert "explanation-reasons" in html
    assert "breakdown-list" in html
