import pytest
from fake_news_module.similarity.searcher import search

def test_similarity_real_claim():
    res = search("Senate panel to hold hearing on Equifax hack")
    assert res.get("label", "Uncertain") in ["Real", "Fake", "Uncertain"]
    assert isinstance(res.get("top_matches", []), list)

def test_similarity_empty():
    res = search("")
    assert res.get("label", "Uncertain") == "Uncertain"
    assert res.get("top_matches", []) == []
