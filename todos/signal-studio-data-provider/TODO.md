# TODO — signal-studio-data-provider

**Updated:** 2026-03-14  
**Composite Score:** 7.2/10  
**Category:** CORE

---

## 🔴 CRITICAL — Fix Immediately

### 1. SecretStr `.get_secret_value()` Missing in Providers
**Severity:** CRITICAL — Runtime crash  
**Files:**
- `providers/snowflake_provider.py:71` — `password=self._sf.password` (SecretStr, not str)
- `providers/oracle_provider.py:49` — `password=self._ora.password`
- `providers/supabase_provider.py:43` — `self._sb.database_url` (SecretStr)
**Problem:** Config fields were changed to `SecretStr` but providers still access them as plain strings. All provider connections will fail at runtime.
**Fix:** Change to `self._sf.password.get_secret_value()` etc. everywhere a SecretStr field is passed to a connector.

### 2. Fix Test Runner — numpy/pandas Binary Incompatibility
**Severity:** CRITICAL — Zero tests running  
**Problem:** `ValueError: numpy.dtype size changed` kills pytest before any test runs.
**Fix:** `pip install --upgrade numpy pandas` in `.venv` OR pin compatible versions in `pyproject.toml`.

### 3. No Integration Tests for Data Abstraction Layer
**Severity:** HIGH — Mock-only tests for a DB abstraction = false confidence  
**Fix:** Add `tests/integration/` with testcontainers (PostgreSQL, Oracle XE).

---

## 🟡 HIGH — Fix This Sprint

### 4. Remove Unused `lru_cache` Import
**File:** `providers/snowflake_provider.py:8`  
**Fix:** Delete `from functools import lru_cache`. Zero risk, 1 minute.

### 5. Replace `run_in_executor` with `asyncio.to_thread()`
**File:** `providers/snowflake_provider.py:107,127,190`  
**Current:** `loop = asyncio.get_running_loop(); await loop.run_in_executor(None, ...)`  
**Fix:** `await asyncio.to_thread(...)` — matches Oracle provider pattern. More idiomatic, simpler.

### 6. DRY — Extract `_validate_identifier` to `providers/_utils.py`
**Files:** All 3 providers define identical `_SAFE_IDENTIFIER_RE` + `_validate_identifier()`.
**Fix:** Create `providers/_utils.py`, import from all three.

### 7. DRY — Extract `build_schema_info` helper
All 3 providers have identical `get_schema()` → `get_tables()` → `SchemaInfo(...)` pattern.
**Fix:** Add to `providers/_utils.py`.

### 8. Factory Cache Race Condition
**File:** `factory.py` — `_provider_cache` dict has no async locking.
**Fix:** Add `asyncio.Lock()` with double-check pattern.

### 9. Schema Registry — Sequential Column Fetch
**File:** `schema/registry.py:37-41` — fetches columns per table in a loop.
**Fix:** Use `asyncio.gather()` for parallel column fetching. Major perf win for large schemas.

---

## 🟢 MEDIUM — Next Sprint

### 10. Deterministic Cache Keys for Snowflake
**File:** `providers/snowflake_provider.py:104`  
`cache_key = f"{sql}|{params}"` — list vs tuple produces different keys for same query.
**Fix:** Use `hashlib.sha256(json.dumps(...)).hexdigest()`.

### 11. Shared Cache Backend (Redis)
Only Snowflake has TTL cache (in-memory, lost on restart). Supabase/Oracle have none.
**Fix:** Create `cache.py` with `CacheBackend` protocol + `InMemoryCache` + `RedisCache`.

### 12. Security Fuzzing Tests
Add `tests/test_security.py` with `hypothesis` property-based tests for `_validate_identifier`.

### 13. DataProvider Contract Tests
Parameterized test suite verifying all 3 providers implement `DataProvider` protocol consistently.

### 14. Async Context Manager Support
Add `__aenter__`/`__aexit__` to all providers for `async with` usage.

### 15. Shared Retry Decorator
Create `providers/_retry.py` with exponential backoff. Currently no retry logic in any provider.

---

## ⚪ LOW — Backlog

### 16. Query Audit Log
Append `execute_query()` calls to structured audit log (compliance for financial clients).

### 17. OpenTelemetry Instrumentation
Wrap provider methods with OTel spans for observability.

### 18. Streaming Query Results
Add `execute_query_stream()` yielding `AsyncIterator[list[dict]]` for large result sets.

### 19. Query Cost Pre-Estimation
Run `EXPLAIN` before execution; block queries exceeding `max_query_cost`.

### 20. Bulk Upsert for `write_back()`
Current INSERT-only. Add ON CONFLICT DO UPDATE / MERGE support.

### 21. Supabase Realtime Subscriptions
`subscribe()` currently raises `NotImplementedError`.

### 22. DuckDB Provider
Local/edge analytics provider for on-premise Signal Studio deployments.

### 23. PyPI Publication
Package already structured. Publish to PyPI for client engineer integration.

---

## Score Breakdown

| Dimension | Score | Notes |
|-----------|-------|-------|
| Architecture | 9/10 | Excellent Protocol-based design, factory routing, clean separation |
| Documentation | 9/10 | Thorough README, BRAINSTORM, PLAN, AUDIT docs |
| Business Value | 8/10 | Critical infrastructure for Signal Studio multi-DB support |
| Code Quality | 7/10 | Good overall, but DRY violations and dead imports |
| Security | 7/10 | Cortex injection fixed, SecretStr added but not wired properly |
| Test Coverage | 4/10 | Test runner broken, mock-only, no integration tests |
