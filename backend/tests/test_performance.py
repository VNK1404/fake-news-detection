import asyncio
import time

from fake_news_module.apis import async_client


async def _run_sequential_baseline(claim):
    class DummySession:
        pass

    session = DummySession()
    google = await async_client.async_google_factcheck(session, claim)
    news = await async_client.async_newsapi(session, claim)
    guardian = await async_client.async_guardian(session, claim)
    return {"google": google, "news": news, "guardian": guardian}


def test_async_external_api_latency_improves_over_sequential(monkeypatch):
    async def slow_google(_session, _claim):
        await asyncio.sleep(0.05)
        return "Real"

    async def slow_news(_session, _claim):
        await asyncio.sleep(0.05)
        return ("Real", [])

    async def slow_guardian(_session, _claim):
        await asyncio.sleep(0.05)
        return "True"

    monkeypatch.setattr(async_client, "async_google_factcheck", slow_google)
    monkeypatch.setattr(async_client, "async_newsapi", slow_news)
    monkeypatch.setattr(async_client, "async_guardian", slow_guardian)

    start = time.perf_counter()
    sequential = asyncio.run(_run_sequential_baseline("claim"))
    sequential_elapsed = time.perf_counter() - start

    start = time.perf_counter()
    concurrent = asyncio.run(async_client.run_external_apis_async("claim"))
    async_elapsed = time.perf_counter() - start

    improvement_pct = ((sequential_elapsed - async_elapsed) / sequential_elapsed) * 100
    print(
        "\nPhase 5 benchmark:"
        f"\nBefore: {sequential_elapsed:.4f}s"
        f"\nAfter: {async_elapsed:.4f}s"
        f"\nImprovement: {improvement_pct:.1f}%"
    )

    assert sequential == concurrent
    assert async_elapsed < sequential_elapsed
    assert improvement_pct >= 40.0
