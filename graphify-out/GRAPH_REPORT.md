# Graph Report - D:\fake-news-detection  (2026-06-13)

## Corpus Check
- 88 files · ~87,669 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 424 nodes · 663 edges · 51 communities detected
- Extraction: 74% EXTRACTED · 26% INFERRED · 0% AMBIGUOUS · INFERRED: 175 edges (avg confidence: 0.78)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 23|Community 23]]
- [[_COMMUNITY_Community 24|Community 24]]
- [[_COMMUNITY_Community 25|Community 25]]
- [[_COMMUNITY_Community 26|Community 26]]
- [[_COMMUNITY_Community 27|Community 27]]
- [[_COMMUNITY_Community 28|Community 28]]
- [[_COMMUNITY_Community 29|Community 29]]
- [[_COMMUNITY_Community 30|Community 30]]
- [[_COMMUNITY_Community 31|Community 31]]
- [[_COMMUNITY_Community 32|Community 32]]
- [[_COMMUNITY_Community 33|Community 33]]
- [[_COMMUNITY_Community 34|Community 34]]
- [[_COMMUNITY_Community 35|Community 35]]
- [[_COMMUNITY_Community 36|Community 36]]
- [[_COMMUNITY_Community 37|Community 37]]
- [[_COMMUNITY_Community 38|Community 38]]
- [[_COMMUNITY_Community 39|Community 39]]
- [[_COMMUNITY_Community 40|Community 40]]
- [[_COMMUNITY_Community 41|Community 41]]
- [[_COMMUNITY_Community 42|Community 42]]
- [[_COMMUNITY_Community 43|Community 43]]
- [[_COMMUNITY_Community 44|Community 44]]
- [[_COMMUNITY_Community 45|Community 45]]
- [[_COMMUNITY_Community 46|Community 46]]
- [[_COMMUNITY_Community 47|Community 47]]
- [[_COMMUNITY_Community 48|Community 48]]
- [[_COMMUNITY_Community 49|Community 49]]
- [[_COMMUNITY_Community 50|Community 50]]

## God Nodes (most connected - your core abstractions)
1. `CacheManager` - 24 edges
2. `fake_news_pipeline()` - 23 edges
3. `RedisCache` - 16 edges
4. `MetricsStore` - 15 edges
5. `run_external_apis_async()` - 15 edges
6. `search()` - 15 edges
7. `generate_pdf_report()` - 13 edges
8. `AnalyticsService` - 10 edges
9. `fake_news_module/source_scoring/__init__.py ====================================` - 10 edges
10. `build_report_payload()` - 9 edges

## Surprising Connections (you probably didn't know these)
- `fake_news_pipeline()` --calls--> `get_analytics_service()`  [INFERRED]
  D:\fake-news-detection\backend\fake_news_module\core\pipeline.py → D:\fake-news-detection\backend\fake_news_module\analytics\analytics_service.py
- `Analytics orchestration helpers for pipeline and dashboard code.` --uses--> `MetricsStore`  [INFERRED]
  D:\fake-news-detection\backend\fake_news_module\analytics\analytics_service.py → D:\fake-news-detection\backend\fake_news_module\analytics\metrics_store.py
- `_record_cache_event()` --calls--> `get_metrics_store()`  [INFERRED]
  D:\fake-news-detection\backend\fake_news_module\cache\cache_manager.py → D:\fake-news-detection\backend\fake_news_module\analytics\metrics_store.py
- `fake_news_module/source_scoring/__init__.py ====================================` --uses--> `CacheManager`  [INFERRED]
  D:\fake-news-detection\backend\fake_news_module\source_scoring\__init__.py → D:\fake-news-detection\backend\fake_news_module\cache\cache_manager.py
- `test_fetch_json_retries_with_exponential_backoff()` --calls--> `_fetch_json()`  [INFERRED]
  D:\fake-news-detection\backend\tests\test_async_execution.py → D:\fake-news-detection\backend\fake_news_module\apis\async_client.py

## Communities

### Community 0 - "Community 0"
Cohesion: 0.09
Nodes (18): AnalyticsService, _api_success_failure_counts(), _confidence_value(), get_analytics_service(), Analytics orchestration helpers for pipeline and dashboard code., _topics(), analytics_performance(), analytics_root() (+10 more)

### Community 1 - "Community 1"
Cohesion: 0.12
Nodes (16): CacheManager, get_cache_manager(), Stable cache-key generation and typed cache operations., High-level Redis cache facade for pipeline, API, and similarity results., _record_cache_event(), stable_hash(), client(), Small fail-open Redis adapter used by the cache manager. (+8 more)

### Community 2 - "Community 2"
Cohesion: 0.08
Nodes (29): compute_score(), final_decision(), core/decision_engine.py — Weighted score computation + final decision logic AI-D, Compute a weighted aggregate score from RoBERTa + all API results.      The scor, Apply threshold rules to the weighted score and return decision + confidence., normalize_result(), core/normalization.py — Convert API labels to numeric scores AI-Driven Digital E, Convert a string label from any API to a numeric score.      Args:         resul (+21 more)

### Community 3 - "Community 3"
Cohesion: 0.15
Nodes (25): download_report(), _resolve_report_source(), _as_float(), _build_evidence_summary(), build_report_payload(), _build_styles(), _bullet_list(), cleanup_old_reports() (+17 more)

### Community 4 - "Community 4"
Cohesion: 0.12
Nodes (25): _analyze_news_results(), async_google_factcheck(), async_guardian(), async_newsapi(), _coerce_label(), _coerce_news_result(), _extract_keywords(), _fetch_json() (+17 more)

### Community 5 - "Community 5"
Cohesion: 0.09
Nodes (22): main(), print_footer(), print_header(), check_api_status.py — Diagnostic utility to test Fake News Detection APIs. This, call_gemini_api(), Send a claim to Gemini model and return a short verification label.      The Gem, call_google_fact_check(), _majority_label() (+14 more)

### Community 6 - "Community 6"
Cohesion: 0.1
Nodes (22): build_parser(), main(), pick_file_with_dialog(), print_result(), main.py — Entry point for Fake News Detection Module AI-Driven Digital Evidence, Open a native Windows file-picker dialog and return the chosen path.     Falls b, _call_external_apis(), _call_roberta() (+14 more)

### Community 7 - "Community 7"
Cohesion: 0.1
Nodes (23): build_confidence_breakdown(), _label_direction(), fake_news_module/explainability/confidence_breakdown.py ========================, Map a raw API label to a directional tag: REAL, FAKE, or NEUTRAL., Convert a numeric source credibility score to a human-readable label., Treat high source credibility as evidence towards REAL., Build a human-readable confidence breakdown for each verification signal.      E, _source_direction() (+15 more)

### Community 8 - "Community 8"
Cohesion: 0.12
Nodes (20): extract_text(), ocr/extractor.py — Unified file-type aware text extractor AI-Driven Digital Evid, Unified entry point: detect file type and delegate to the correct extractor., extract_text_from_image(), _preprocess_image(), ocr/image_ocr.py — Image OCR using pytesseract + OpenCV AI-Driven Digital Eviden, Apply preprocessing pipeline to improve OCR accuracy:     1. Convert to grayscal, Upscale small images — Tesseract performs poorly on images < 300 DPI. (+12 more)

### Community 9 - "Community 9"
Cohesion: 0.13
Nodes (16): call_roberta(), call_similarity(), fake_news_module/similarity/inference.py =======================================, Run FAISS similarity search on a claim and return a standardized label.      Thi, Run RoBERTa inference on a claim and return a standardized label string.      Th, _import_torch(), _import_transformers(), load_model() (+8 more)

### Community 10 - "Community 10"
Cohesion: 0.13
Nodes (16): extract_main_text(), _is_noise_line(), processing/claim_extractor.py — Extract main claim/headline from cleaned text AI, Return True if the sentence looks like a noisy header or social media artifact., Score a sentence for how likely it is to be the main claim.     Higher = better, Extract the most likely main claim or headline from text.      Strategy:     1., _score_sentence(), _call_similarity() (+8 more)

### Community 11 - "Community 11"
Cohesion: 0.23
Nodes (11): clean_text(), _collapse_whitespace(), _normalize_unicode(), processing/text_cleaner.py — Text normalization and cleaning AI-Driven Digital E, Normalize unicode characters to ASCII-compatible form., Remove non-alphanumeric characters except sentence punctuation.     Keeps: lette, Collapse multiple whitespace into a single space., Remove common OCR artifacts:     - Lone single characters (except 'a', 'i') (+3 more)

### Community 12 - "Community 12"
Cohesion: 0.2
Nodes (10): embed(), _load_model(), fake_news_module/similarity/embedder.py ========================================, Lazily import and initialize the SentenceTransformer model.      Returns:, Encode a list of text strings into L2-normalized float32 embeddings.      Args:, build_index(), _load_corpus(), fake_news_module/similarity/index_builder.py =================================== (+2 more)

### Community 13 - "Community 13"
Cohesion: 0.27
Nodes (6): allowed_file(), analyze(), fake_news_pipeline(), app.py — Flask Web Interface for Fake News Detection Module AI-Driven Digital Ev, Accepts a text claim or multipart file upload, runs the detection pipeline,, _store_reportable_result()

### Community 14 - "Community 14"
Cohesion: 0.42
Nodes (7): _install_app_import_stubs(), _load_app(), _sample_result(), test_analyze_accepts_text_and_sets_analysis_header(), test_analyze_rejects_invalid_file(), test_download_report_without_payload_returns_bad_request(), test_health_route_returns_healthy_payload()

### Community 15 - "Community 15"
Cohesion: 0.29
Nodes (7): _compute_metrics(), _load_dataset(), fake_news_module/ml/train.py ============================ Fine-tuning pipeline f, Fine-tune `roberta-base` on the provided CSV dataset.      Args:         dataset, Compute accuracy, precision, recall and F1 from Trainer eval output.      Called, Load a CSV file (columns: `text`, `label`) and return a HuggingFace Dataset., train()

### Community 16 - "Community 16"
Cohesion: 0.48
Nodes (5): analyzeNews(), getAnalytics(), getAnalyticsPerformance(), getAnalyticsSummary(), request()

### Community 17 - "Community 17"
Cohesion: 0.67
Nodes (1): prepare_dataset.py =================== Combines True.csv and Fake.csv from the d

### Community 18 - "Community 18"
Cohesion: 1.0
Nodes (1): config.py — Central configuration for Fake News Detection Module AI-Driven Digit

### Community 19 - "Community 19"
Cohesion: 1.0
Nodes (0): 

### Community 20 - "Community 20"
Cohesion: 1.0
Nodes (0): 

### Community 21 - "Community 21"
Cohesion: 1.0
Nodes (0): 

### Community 22 - "Community 22"
Cohesion: 1.0
Nodes (0): 

### Community 23 - "Community 23"
Cohesion: 1.0
Nodes (0): 

### Community 24 - "Community 24"
Cohesion: 1.0
Nodes (0): 

### Community 25 - "Community 25"
Cohesion: 1.0
Nodes (0): 

### Community 26 - "Community 26"
Cohesion: 1.0
Nodes (0): 

### Community 27 - "Community 27"
Cohesion: 1.0
Nodes (0): 

### Community 28 - "Community 28"
Cohesion: 1.0
Nodes (0): 

### Community 29 - "Community 29"
Cohesion: 1.0
Nodes (0): 

### Community 30 - "Community 30"
Cohesion: 1.0
Nodes (0): 

### Community 31 - "Community 31"
Cohesion: 1.0
Nodes (0): 

### Community 32 - "Community 32"
Cohesion: 1.0
Nodes (0): 

### Community 33 - "Community 33"
Cohesion: 1.0
Nodes (0): 

### Community 34 - "Community 34"
Cohesion: 1.0
Nodes (0): 

### Community 35 - "Community 35"
Cohesion: 1.0
Nodes (0): 

### Community 36 - "Community 36"
Cohesion: 1.0
Nodes (0): 

### Community 37 - "Community 37"
Cohesion: 1.0
Nodes (0): 

### Community 38 - "Community 38"
Cohesion: 1.0
Nodes (0): 

### Community 39 - "Community 39"
Cohesion: 1.0
Nodes (0): 

### Community 40 - "Community 40"
Cohesion: 1.0
Nodes (0): 

### Community 41 - "Community 41"
Cohesion: 1.0
Nodes (0): 

### Community 42 - "Community 42"
Cohesion: 1.0
Nodes (0): 

### Community 43 - "Community 43"
Cohesion: 1.0
Nodes (0): 

### Community 44 - "Community 44"
Cohesion: 1.0
Nodes (0): 

### Community 45 - "Community 45"
Cohesion: 1.0
Nodes (0): 

### Community 46 - "Community 46"
Cohesion: 1.0
Nodes (0): 

### Community 47 - "Community 47"
Cohesion: 1.0
Nodes (0): 

### Community 48 - "Community 48"
Cohesion: 1.0
Nodes (0): 

### Community 49 - "Community 49"
Cohesion: 1.0
Nodes (0): 

### Community 50 - "Community 50"
Cohesion: 1.0
Nodes (0): 

## Knowledge Gaps
- **104 isolated node(s):** `app.py — Flask Web Interface for Fake News Detection Module AI-Driven Digital Ev`, `Accepts a text claim or multipart file upload, runs the detection pipeline,`, `check_api_status.py — Diagnostic utility to test Fake News Detection APIs. This`, `main.py — Entry point for Fake News Detection Module AI-Driven Digital Evidence`, `Open a native Windows file-picker dialog and return the chosen path.     Falls b` (+99 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 18`** (2 nodes): `config.py — Central configuration for Fake News Detection Module AI-Driven Digit`, `config.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 19`** (2 nodes): `layout.tsx`, `RootLayout()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 20`** (2 nodes): `page.tsx`, `LandingPage()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 21`** (2 nodes): `page.tsx`, `AnalyzePage()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 22`** (2 nodes): `page.tsx`, `ReportsPage()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 23`** (2 nodes): `page.tsx`, `ResultsPage()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 24`** (2 nodes): `AppShell()`, `AppShell.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 25`** (2 nodes): `ConfidenceGauge()`, `ConfidenceGauge.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 26`** (2 nodes): `HealthIndicator.tsx`, `HealthIndicator()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 27`** (2 nodes): `Providers.tsx`, `Providers()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 28`** (2 nodes): `ReportTable.tsx`, `ReportTable()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 29`** (2 nodes): `SideNavBar.tsx`, `SideNavBar()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 30`** (2 nodes): `SimilarityCard.tsx`, `SimilarityCard()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 31`** (2 nodes): `UploadZone.tsx`, `UploadZone()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 32`** (2 nodes): `VerdictCard.tsx`, `VerdictCard()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 33`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 34`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 35`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 36`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 37`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 38`** (1 nodes): `eslint.config.mjs`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 39`** (1 nodes): `next-env.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 40`** (1 nodes): `next.config.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 41`** (1 nodes): `postcss.config.mjs`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 42`** (1 nodes): `page.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 43`** (1 nodes): `page.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 44`** (1 nodes): `AnalyticsChart.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 45`** (1 nodes): `HeroSection.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 46`** (1 nodes): `LoadingPipeline.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 47`** (1 nodes): `TopNavBar.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 48`** (1 nodes): `TrustMeter.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 49`** (1 nodes): `data.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 50`** (1 nodes): `useAppStore.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `fake_news_pipeline()` connect `Community 6` to `Community 0`, `Community 1`, `Community 2`, `Community 3`, `Community 4`, `Community 7`, `Community 8`, `Community 10`, `Community 11`?**
  _High betweenness centrality (0.251) - this node is a cross-community bridge._
- **Why does `search()` connect `Community 10` to `Community 1`, `Community 3`, `Community 9`, `Community 11`, `Community 12`?**
  _High betweenness centrality (0.096) - this node is a cross-community bridge._
- **Why does `extract_text()` connect `Community 8` to `Community 6`?**
  _High betweenness centrality (0.073) - this node is a cross-community bridge._
- **Are the 8 inferred relationships involving `CacheManager` (e.g. with `RedisCache` and `fake_news_module/source_scoring/__init__.py ====================================`) actually correct?**
  _`CacheManager` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 20 inferred relationships involving `fake_news_pipeline()` (e.g. with `main()` and `extract_text()`) actually correct?**
  _`fake_news_pipeline()` has 20 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `RedisCache` (e.g. with `CacheManager` and `Stable cache-key generation and typed cache operations.`) actually correct?**
  _`RedisCache` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `MetricsStore` (e.g. with `AnalyticsService` and `Analytics orchestration helpers for pipeline and dashboard code.`) actually correct?**
  _`MetricsStore` has 5 INFERRED edges - model-reasoned connections that need verification._