'''check_api_status.py — Diagnostic utility to test Fake News Detection APIs.
This script tests connections and credentials for:
- Gemini API (Google Generative AI)
- Google Fact Check API
- NewsAPI
- The Guardian Content API
''' 

import sys
import os
import logging
from pathlib import Path

# Ensure project root is importable
sys.path.insert(0, str(Path(__file__).resolve().parent))

# Make sure API keys are loaded from environment variables or .env file before running this utility.

# Import API calls and configs
from fake_news_module.config import (
    GEMINI_API_KEY,
    GOOGLE_API_KEY,
    NEWS_API_KEY,
    GUARDIAN_API_KEY,
)
from fake_news_module.apis.gemini_api import call_gemini_api
from fake_news_module.apis.google_api import call_google_fact_check
from fake_news_module.apis.news_api import call_news_api
from fake_news_module.apis.guardian_api import call_guardian_api

# Disable internal library logging noise
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger("api_check")

# Visual separators
def print_header(title: str):
    print("=" * 60)
    print(f"  TESTING: {title}")
    print("=" * 60)

def print_footer():
    print("-" * 60)
    print()

def main():
    print("\n============================================================")
    print("      FAKE NEWS DETECTION ENGINE -- API DIAGNOSTIC TOOL      ")
    print("============================================================\n")

    test_claim = "Scientists discover water on Mars in recent NASA mission."

    # 1. TEST GEMINI
    print_header("Gemini API (Google Generative AI)")
    print(f"  Gemini URL: {os.getenv('GEMINI_API_URL', 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent')}")
    print(f"  Gemini Key: {GEMINI_API_KEY[:10]}...{GEMINI_API_KEY[-10:] if len(GEMINI_API_KEY) > 20 else ''}\n")
    try:
        gemini_res = call_gemini_api(test_claim)
        print(f"  [ OK ] Gemini API returned: '{gemini_res}'")
    except Exception as e:
        print(f"  [ FAIL ] Gemini API FAILED: {e}")
    print_footer()

    # 2. TEST GOOGLE FACT CHECK
    print_header("Google Fact Check API")
    print(f"  Google API Key: {GOOGLE_API_KEY[:10]}...\n")
    try:
        google_res = call_google_fact_check("Earth is flat")
        print(f"  [ OK ] Google Fact Check returned: '{google_res}'")
    except Exception as e:
        print(f"  [ FAIL ] Google Fact Check FAILED: {e}")
    print_footer()

    # 3. TEST NEWSAPI
    print_header("NewsAPI")
    print(f"  NewsAPI Key: {NEWS_API_KEY[:10]}...\n")
    try:
        articles = call_news_api("Trump election")
        if articles:
            print(f"  [ OK ] NewsAPI returned {len(articles)} articles.")
        else:
            print("  [ OK ] NewsAPI returned no articles but connection succeeded.")
    except Exception as e:
        print(f"  [ FAIL ] NewsAPI FAILED: {e}")
    print_footer()

    # 4. TEST GUARDIAN API
    print_header("Guardian Content API")
    print(f"  Guardian API Key: {GUARDIAN_API_KEY[:10]}...\n")
    try:
        guardian_res = call_guardian_api(test_claim)
        print(f"  [ OK ] Guardian API returned: '{guardian_res}'")
    except Exception as e:
        print(f"  [ FAIL ] Guardian API FAILED: {e}")
    print_footer()

if __name__ == "__main__":
    main()
