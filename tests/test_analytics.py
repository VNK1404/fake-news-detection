from flask import Flask

from fake_news_module.analytics.analytics_service import AnalyticsService
from fake_news_module.analytics.dashboard_api import analytics_bp
from fake_news_module.analytics.metrics_store import MetricsStore


def _sample_result(decision="Real"):
    return {
        "claim": "Reuters confirms public health claim",
        "api_results": {
            "roberta": decision,
            "similarity": decision,
            "google_fact_check": "Unknown",
            "news_api": decision,
            "guardian": "True",
            "source": decision,
        },
        "score": 0.6,
        "final_decision": decision,
        "confidence": "High",
    }


def test_metric_recording_and_aggregation(tmp_path):
    store = MetricsStore(str(tmp_path / "analytics.db"))
    service = AnalyticsService(store)

    service.record_analysis(
        _sample_result("Real"),
        pipeline_duration=1.2,
        stage_timings={"external_apis": 0.5, "similarity": 0.2, "roberta": 0.1},
        cache_hit=False,
    )
    service.record_analysis(
        _sample_result("Fake"),
        pipeline_duration=0.3,
        stage_timings={"external_apis": 0.0, "similarity": 0.0, "roberta": 0.0},
        cache_hit=True,
    )
    store.record_cache_event("hit", "pipeline")
    store.record_cache_event("miss", "pipeline")

    summary = service.summary()
    performance = service.performance()

    assert summary["total_analyses"] == 2
    assert summary["real_count"] == 1
    assert summary["fake_count"] == 1
    assert summary["cache_hit_rate"] == 0.5
    assert summary["api_success_rate"] > 0
    assert summary["most_common_topics"]
    assert performance["average_pipeline_duration"] == 0.75
    assert len(performance["latency_trend"]) == 2


def test_analytics_api_endpoints(monkeypatch, tmp_path):
    store = MetricsStore(str(tmp_path / "analytics.db"))
    service = AnalyticsService(store)
    service.record_analysis(
        _sample_result("Uncertain"),
        pipeline_duration=0.4,
        stage_timings={"external_apis": 0.2},
        cache_hit=False,
    )

    from fake_news_module.analytics import dashboard_api

    monkeypatch.setattr(dashboard_api, "get_analytics_service", lambda: service)

    app = Flask(__name__)
    app.register_blueprint(analytics_bp)
    client = app.test_client()

    assert client.get("/api/analytics").status_code == 200
    assert client.get("/api/analytics/summary").get_json()["total_analyses"] == 1
    assert "average_pipeline_duration" in client.get("/api/analytics/performance").get_json()


def test_dashboard_rendering_hooks_exist():
    html = open("templates/index.html", encoding="utf-8").read()

    assert "analytics-dashboard" in html
    assert "metric-total" in html
    assert "verdict-chart" in html
    assert "topics-chart" in html
    assert "latency-chart" in html
    assert "cdn.jsdelivr.net/npm/chart.js" in html
