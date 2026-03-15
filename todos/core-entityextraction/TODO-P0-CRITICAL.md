# core-entityextraction — P0 CRITICAL TODOs
> Updated: 2026-03-15 | Scored by Honey 🍯

## 🐛 [BUG] Fix off-by-one in ExcludeRules.is_start_of_sentence
- **File:** `main.py` line 104
- **Issue:** `range(start_index, 1, -1)` starts at the entity's own first character instead of the character before it. Loop checks entity char (never punctuation), exits via `break`, returns `False` — incorrectly marking entities as NOT at sentence start.
- **Fix:** Change to `range(start_index - 1, 0, -1)`
- **Impact:** Causes incorrect entity extraction results in production. Entities at sentence boundaries are misclassified.
- **Effort:** XS (1-line fix)
- **Status:** ❌ PENDING

## 🧪 [QUALITY] Add Test Suite — ZERO Coverage
- **Issue:** Production NLP service with 0% test coverage. No test files exist (only `tests/__pycache__/`).
- **Priority test cases:**
  - `test_pattern_matching.py` — `_locate_entities`, `_build_entity_patterns`, ExcludeRules edge cases
  - `test_api.py` — pytest + httpx AsyncClient for all FastAPI endpoints
  - `test_persistence.py` — async mock tests for asyncpg persistence layer
  - `test_ml_extraction.py` — mock spaCy model, assert response structure
  - `conftest.py` — shared fixtures (test app, mock entity store, mock DB)
- **Tooling:** pytest, pytest-asyncio, httpx, pytest-mock
- **Effort:** M (1-2 days)
- **Status:** ❌ PENDING

## 🔒 [SECURITY] Add CORS Middleware
- **File:** `main.py`
- **Issue:** No `CORSMiddleware` configured. Browser clients cannot call the API (blocked by CORS policy).
- **Fix:** Add `app.add_middleware(CORSMiddleware, allow_origins=[env-configured origins], allow_methods=["*"], allow_headers=["*"])`
- **Effort:** XS (5 lines)
- **Status:** ❌ PENDING

## 📖 [DOCS] Rewrite README.md — Completely Stale
- **Issue:** README references Flask, SQLite, Python 3.6.5, `flask run`, `db.sqlite`, Swagger via Flasgger. The live service is FastAPI + asyncpg + Railway. Every instruction is wrong.
- **Fix:** Rewrite with: FastAPI overview, `DATABASE_URL` config, Docker Compose, Railway deploy, API endpoint docs, env var reference
- **Effort:** S
- **Status:** ❌ PENDING

## 📖 [DOCS] Replace .env.example with FastAPI-relevant variables
- **Issue:** `.env.example` contains `FLASK_APP=app:create`, `FLASK_ENV`, `SECRET_KEY`, `DATABASE=db.sqlite` — all meaningless to FastAPI.
- **Fix:** Replace with: `DATABASE_URL`, `ENTITY_EXTRACTION_API_KEY`, `ENABLE_SPACY_ENTITY_EXTRACTION`, `SPACY_MODEL`, `DB_POOL_MIN`, `DB_POOL_MAX`, `RATE_LIMIT_REGEX`, `RATE_LIMIT_ML`
- **Effort:** XS
- **Status:** ❌ PENDING
