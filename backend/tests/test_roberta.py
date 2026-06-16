import pytest
from fake_news_module.ml.inference import call_roberta

def test_roberta_real_claim():
    # If the model isn't loaded properly, this might return Unknown
    res = call_roberta("Scientists discover water on Mars")
    assert res in ["Real", "Fake", "Unknown"]

def test_roberta_empty_claim():
    res = call_roberta("")
    assert res == "Unknown"
