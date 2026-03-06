# TODO-721 Done: pytest Test Suite for core-entityextraction

## Status: ✅ Complete

## What Was Implemented

### Test Files Created
- `tests/__init__.py` — package marker
- `tests/conftest.py` — shared fixtures:
  - `ENTITY_EXTRACTION_API_KEY` env var set to `test-secret-key-123`
  - `DATABASE_URL` unset (persistence runs in-memory-only mode)
  - `reset_entity_store` autouse fixture clears entity store before/after each test
  - `client` async fixture using `httpx.AsyncClient` + `ASGITransport`
  - `api_headers` fixture returning `{"X-API-Key": "test-secret-key-123"}`
  - `mock_persistence` autouse fixture stubs `save_entities`, `delete_entities`, `init_db`, `load_all`
- `tests/test_health.py` — 4 tests for `/health` and `/version`
- `tests/test_auth.py` — 10 tests covering auth middleware (missing key, wrong key, empty key → 401; valid key passes; `/health` bypasses auth)
- `tests/test_regex_extraction.py` — 24 tests: 20 parametrized financial sentences (Company, Fund, Country, CurrencyPair, EconomicIndicator) + structure/filter tests
- `tests/test_fixed_lists.py` — 6 tests for full CRUD cycle: add entity, extract it, delete it, verify gone

### Support Files
- `requirements-dev.txt` — `pytest>=8.0`, `pytest-asyncio>=0.23`, `httpx>=0.27`
- `pytest.ini` — `asyncio_mode = auto`

### Pipeline
- `bitbucket-pipelines.yml` — added pytest step (before deploy trigger) for both `master` and `development` branches

## Test Results
```
43 passed, 2 warnings in 2.61s
```
All 43 tests pass. The 2 warnings are deprecation notices about FastAPI's `on_event` (not a test issue).
