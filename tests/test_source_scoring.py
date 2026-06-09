import pytest
from fake_news_module.source_scoring.source_scorer import get_source_score, _extract_domain

def test_extract_domain():
    assert _extract_domain("https://www.nytimes.com/article/123") == "nytimes.com"
    assert _extract_domain("http://bbc.co.uk") == "bbc.co.uk"
    assert _extract_domain("not-a-url") == ""

def test_get_source_score():
    score1 = get_source_score("According to a new report from https://nytimes.com")
    assert score1 > 0.5

    score2 = get_source_score("I read it on https://infowars.com")
    assert score2 < 0.5

    score3 = get_source_score("Just a random claim without source")
    assert score3 == 0.5
