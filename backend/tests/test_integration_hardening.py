from pathlib import Path

from fake_news_module.core.decision_engine import compute_score, final_decision
from fake_news_module.source_scoring.source_scorer import (
    _extract_domain,
    get_source_score,
    score_source_evidence,
)


def _install_pipeline_import_stubs(monkeypatch):
    import sys
    import types

    monkeypatch.setitem(sys.modules, "pytesseract", types.SimpleNamespace(pytesseract=types.SimpleNamespace()))
    monkeypatch.setitem(sys.modules, "cv2", types.SimpleNamespace())
    monkeypatch.setitem(sys.modules, "pdfplumber", types.SimpleNamespace(open=lambda *_args, **_kwargs: None))
    monkeypatch.setitem(sys.modules, "requests", types.SimpleNamespace())


def test_source_scoring_is_safe_for_plain_claim_text():
    assert _extract_domain("Plain claim text without a URL") == ""
    assert get_source_score("Plain claim text without a URL") == 0.5
    assert score_source_evidence(["Plain claim text without a URL"]) == {
        "source_score": 0.5,
        "sources_found": [],
    }


def test_source_scoring_collects_evidence_domains():
    evidence = score_source_evidence([
        "Claim cites https://www.reuters.com/world/example",
        {"url": "https://infowars.com/story"},
    ])

    assert evidence["source_score"] == 0.5
    assert evidence["sources_found"] == [
        {"domain": "reuters.com", "score": 0.97},
        {"domain": "infowars.com", "score": 0.03},
    ]


def test_source_score_affects_decision_weighting():
    without_source = compute_score({"roberta": "Real"})
    with_source = compute_score({"roberta": "Real", "source": "Fake"})

    assert without_source == 1.0
    assert with_source < without_source
    assert with_source == 0.5556


def test_source_only_can_drive_a_verdict():
    score = compute_score({"source": "Fake"})
    decision, confidence = final_decision(score)

    assert score == -1.0
    assert decision == "Fake"
    assert confidence == "High"


def test_pipeline_final_json_schema(monkeypatch, tmp_path):
    _install_pipeline_import_stubs(monkeypatch)
    from fake_news_module.core import pipeline

    sample = tmp_path / "sample.txt"
    sample.write_text("placeholder", encoding="utf-8")

    monkeypatch.setattr(
        pipeline,
        "extract_text",
        lambda path: (
            "Reuters reports that NASA confirmed water on Mars in a new briefing. "
            "See https://www.reuters.com/science/mars-water for the original coverage."
        ),
    )
    monkeypatch.setattr(pipeline, "clean_text", lambda text: text)
    monkeypatch.setattr(pipeline, "validate_text", lambda text: (True, "ok"))
    monkeypatch.setattr(pipeline, "extract_main_text", lambda text: text)
    monkeypatch.setattr(
        pipeline,
        "_run_apis_parallel",
        lambda claim: {
            "roberta": "Real",
            "similarity": (
                "Real",
                [{"title": "NASA confirms water on Mars", "label": "Real", "score": 0.91}],
            ),
            "google": "Real",
            "news": (
                "Real",
                [{"title": "Mars water confirmed", "url": "https://www.reuters.com/science/mars-water"}],
            ),
            "guardian": "Real",
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
    assert set(result["api_results"]) >= {
        "roberta",
        "similarity",
        "google_fact_check",
        "news_api",
        "guardian",
        "source",
    }
    assert result["api_results"]["similarity"] == "Real"
    assert result["api_results"]["source"] == "Real"
    assert result["source_score"] == 0.97
    assert result["final_decision"] == "Real"

    evidence = result["explanation"]["evidence"]
    assert evidence["similarity_evidence"]["top_matches"][0]["title"]
    assert evidence["similarity_evidence"]["top_matches"][0]["score"] == 0.91
    assert evidence["source_evidence"]["sources_found"][0] == {
        "domain": "reuters.com",
        "score": 0.97,
    }
    assert result["explanation"]["reasons"]
    assert result["explanation"]["confidence_breakdown"]["source"]["contributed"] is True


def test_frontend_renders_backend_schema_keys():
    html = Path("templates/index.html").read_text(encoding="utf-8")

    assert "m.score" in html
    assert "m.title" in html
    assert "source_evidence" in html
    assert "explanation-reasons" in html
    assert "breakdown-list" in html
    assert "similar-claims-list" in html
    assert "source-evidence-list" in html
    assert ("Gr" + "ok") not in html
    assert ("Rapid" + "API") not in html
