# core-entityextraction — P1 IMPORTANT TODOs
> Updated: 2026-03-15 | Scored by Honey 🍯

## 🧹 [CLEANUP] Delete Remaining Dead Code
- **`utils/logger.py`** — Flask `current_app.logger` wrapper, raises RuntimeError in FastAPI. Not imported by main.py.
- **`services/ml_entity_extraction_service/`** — MLEntityExtractionService class with broken imports (references nonexistent `spacy_entity_extraction_service`). ML logic is inlined in main.py.
- **`seeds/`** — Seeds use Flask app context and SQLite `get_db()`. Incompatible with current Postgres stack.
- **Effort:** XS
- **Status:** ❌ PENDING

## 🏗️ [ARCHITECTURE] Deduplicate Entity Constants
- **Issue:** 17 `ENTITY_*` constants defined both in `main.py` (lines 40-56) and `constants/entities.py`. Two sources of truth.
- **Fix:** In `main.py`, replace inline definitions with `from constants.entities import *` and delete the duplicate block.
- **Add startup assertion:** `assert set(entity_store.keys()) == set(ENTITY_OPTIONS.keys())`
- **Effort:** XS
- **Status:** ❌ PENDING

## ⚡ [PERFORMANCE] Cache Compiled Regex Patterns
- **File:** `main.py`, `match_patterns()` / `_build_entity_patterns()`
- **Issue:** Every call rebuilds all regex patterns from scratch — O(n) per request with thousands of entities.
- **Fix:** Cache compiled `re.Pattern` objects at module level. Invalidate on `/fixed_lists` write. Estimated 10-50x speedup.
- **Effort:** S (2 hours)
- **Status:** ❌ PENDING

## 🛠️ [DEVOPS] Add Pre-commit Hooks
- **Fix:** Add `.pre-commit-config.yaml` with: `ruff` (lint), `mypy` (types), `bandit` (security scan)
- **Effort:** S
- **Status:** ❌ PENDING

## 🛠️ [DEVOPS] Fix CI Pipeline (bitbucket-pipelines.yml)
- **Issue:** CI only triggers external deploy pipeline. Missing: lint, test, type check, security scan, Docker build verification. Spurious `redis` service declared but unused.
- **Fix:** Add lint → test → security scan steps. Remove redis service. Add coverage gate (≥60%).
- **Effort:** S
- **Status:** ❌ PENDING

## 🚀 [FEATURE] Batch Extraction Endpoints
- **Issue:** Callers must make N API calls for N texts. Bottleneck for document-heavy workflows.
- **Fix:** Add `POST /batch_regex_entity_extraction` and `POST /batch_ml_entity_extraction` accepting `{"texts": [...]}`. Process with `asyncio.gather`.
- **Effort:** S
- **Status:** ❌ PENDING

## 🚀 [FEATURE] Entity Confidence Scores
- **Issue:** ML/spaCy predictions return no confidence score. Callers can't threshold or rank.
- **Fix:** Return `confidence` field from spaCy NER scores. For regex matches return `confidence: 1.0`.
- **Effort:** M
- **Status:** ❌ PENDING

## 🏗️ [ARCHITECTURE] DRY: Refactor Duplicate Error Response Pattern
- **Issue:** Every endpoint repeats identical `try/except → JSONResponse({"response": str(exc), "status": 400})` blocks.
- **Fix:** Create FastAPI `@app.exception_handler(Exception)` or shared decorator.
- **Effort:** XS
- **Status:** ❌ PENDING

## ⚡ [PERFORMANCE] Async Model Loading at Startup
- **File:** `main.py`, `startup_event()`
- **Issue:** `spacy.load()` reads multi-MB binary files synchronously in the async event loop, blocking health checks for 2-10 seconds.
- **Fix:** Wrap with `await asyncio.to_thread(_load_ml_model)`. Add warm-up call after load.
- **Effort:** XS
- **Status:** ❌ PENDING

## 🔒 [SECURITY] API Key Rotation Support
- **Issue:** Single `ENTITY_EXTRACTION_API_KEY` env var. Rotating requires downtime.
- **Fix:** Support comma-separated keys: `VALID_KEYS = set(os.environ.get("ENTITY_EXTRACTION_API_KEY", "").split(","))`
- **Effort:** XS
- **Status:** ❌ PENDING

## 🏷️ [QUALITY] Add Type Annotations
- **Files:** `main.py`, remaining utils
- **Issue:** `match_patterns()` returns `List[Dict]` — should be `List[EntityMatch]` with Pydantic model. Several functions missing return types.
- **Effort:** S
- **Status:** ❌ PENDING
