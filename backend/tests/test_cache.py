import time

from fake_news_module.cache.cache_manager import CacheManager
from fake_news_module.cache.redis_cache import RedisCache


class FakeRedis:
    def __init__(self):
        self.store = {}
        self.now = time.time()

    def get(self, key):
        item = self.store.get(key)
        if item is None:
            return None
        expires_at, payload = item
        if expires_at <= self.now:
            self.store.pop(key, None)
            return None
        return payload

    def setex(self, key, ttl, payload):
        self.store[key] = (self.now + ttl, payload)
        return True


class BrokenRedis:
    def get(self, _key):
        raise ConnectionError("redis down")

    def setex(self, _key, _ttl, _payload):
        raise ConnectionError("redis down")


def test_cache_hit_and_miss():
    fake = FakeRedis()
    manager = CacheManager(RedisCache(client=fake), ttl_seconds=60, key_prefix="test")

    assert manager.get_pipeline_result("same claim") is None

    result = {"claim": "same claim", "final_decision": "Real", "api_results": {"roberta": "Real"}}
    assert manager.set_pipeline_result("same claim", result) is True
    assert manager.get_pipeline_result("same claim") == result


def test_cache_expiration():
    fake = FakeRedis()
    manager = CacheManager(RedisCache(client=fake), ttl_seconds=1, key_prefix="test")

    manager.set_similarity_result("claim", {"label": "Real", "top_matches": []})
    assert manager.get_similarity_result("claim")["label"] == "Real"

    fake.now += 2
    assert manager.get_similarity_result("claim") is None


def test_redis_unavailable_never_raises():
    manager = CacheManager(RedisCache(client=BrokenRedis()), ttl_seconds=60, key_prefix="test")

    assert manager.get_api_response("external_apis", "claim") is None
    assert manager.set_api_response("external_apis", "claim", {"google": "Unknown"}) is False


def test_cached_pipeline_result_preserves_schema():
    fake = FakeRedis()
    manager = CacheManager(RedisCache(client=fake), ttl_seconds=60, key_prefix="test")
    result = {
        "extracted_text": "text",
        "claim": "claim",
        "api_results": {
            "roberta": "Real",
            "similarity": "Real",
            "google_fact_check": "Unknown",
            "news_api": "Uncertain",
            "guardian": "False",
            "source": "Real",
        },
        "explanation": {},
        "source_score": 0.8,
        "score": 0.5,
        "final_decision": "Real",
        "confidence": "High",
    }

    manager.set_pipeline_result("claim", result)

    assert set(manager.get_pipeline_result("claim")) == set(result)
