# core-entityextraction — P1 IMPORTANT TODOs

> Generated: 2026-03-14 | Source: AUDIT.md + code review

## 🟡 TODO-894: Fix HTTP Status Code Inconsistency
**File:** `main.py`  
**Effort:** S (30 min)  
**Description:** All error paths return `status_code=200` with `{"status": 400}` in body. Breaks monitoring, alerting, and standard HTTP clients.  
**Fix:** Use `HTTPException(status_code=400)` or `JSONResponse(..., status_code=400)`.  
**Affected endpoints:** `/regex_entity_extraction`, `/ml_entity_extraction`, `/spacy_entity_extraction`, `/fixed_lists` DELETE  
**⚠️ Risk:** May break clients that parse body status. Audit API consumers first.

---

## 🟡 TODO-895: Migrate psycopg2 → asyncpg
**File:** `persistence.py`  
**Effort:** M (2-3h)  
**Description:** FastAPI is async-native; sync `psycopg2.ThreadedConnectionPool` blocks the event loop on every DB call. Replace with `asyncpg` + async connection pool for true async I/O.  
**Dependencies:** TODO-893 (fix connection leak first)

---

## 🟡 TODO-896: Dead Code Cleanup + Wire Pydantic Models
**File:** `main.py`  
**Effort:** XS-S (20 min)  
**Tasks:**
1. Remove dead `_locate_entities()` function (non-compiled slow path, never called since TODO-232)
2. Wire `FixedListsUpdateRequest` and `FixedListsDeleteRequest` as endpoint parameters instead of `await request.json()`
3. Extract `special_characters` tuple to module-level constant (DRY)

---

## 🟡 TODO-897: Env-Based Rate Limits + Allowlist Validation
**File:** `main.py`  
**Effort:** XS (20 min)  
**Tasks:**
1. Replace hardcoded `@limiter.limit("100/minute")` with `os.environ.get("RATE_LIMIT_REGEX", "100/minute")`
2. Same for ML endpoint with `RATE_LIMIT_ML`
3. Add `entity_types_list` allowlist validation — unknown types should return HTTP 422, not silently match nothing

---

## 🟡 TODO-898: Persistence Layer Tests
**File:** `tests/`  
**Effort:** S (1h)  
**Description:** Zero tests for `persistence.py`. Need:
- `init_db()` returns False without DATABASE_URL
- `save_entities` called on fixed_lists update
- `delete_entities` called on fixed_lists delete
- Connection pool retry on transient failures

---

## 🟡 TODO-899: CORS Middleware
**File:** `main.py`  
**Effort:** XS (10 min)  
**Description:** Add `CORSMiddleware` for browser-based clients. Use `CORS_ORIGINS` env var.

---

## 🟡 TODO-900: Prometheus Metrics
**File:** `main.py`, `requirements.txt`  
**Effort:** S (1h)  
**Description:** Add `prometheus-fastapi-instrumentator` for request rate/latency, ML prediction latency, entity store size gauge.

---

## 🟡 TODO-901: Pre-commit Hooks + CI Linting
**Files:** `.pre-commit-config.yaml`, `bitbucket-pipelines.yml`  
**Effort:** S (30 min)  
**Description:** Add ruff + mypy pre-commit hooks. Add linting step to CI pipeline. Add coverage reporting.
