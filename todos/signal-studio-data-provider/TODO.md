# TODO — signal-studio-data-provider

**Updated:** 2026-03-15  
**Composite Score:** 6.3/10  
**Category:** Infrastructure / Data Layer  
**Location:** `/data/workspace/projects/signal-studio-data-provider`

---

## Dimension Scores

| Dimension | Score | Notes |
|-----------|-------|-------|
| **Documentation** | 9/10 | Excellent BRAINSTORM.md, PLAN.md, AUDIT.md with detailed architecture |
| **Architecture** | 8/10 | Protocol-based design, factory pattern, clean provider separation |
| **Business Value** | 7/10 | Critical multi-DB data layer for Signal Studio (Snowflake/Supabase/Oracle) |
| **Code Quality** | 6/10 | SecretStr adoption incomplete, DRY violations, deprecated asyncio usage |
| **Security** | 5/10 | Cortex injection pattern still risky, SecretStr not wired through providers |
| **Test Coverage** | 4/10 | 570 lines of tests but runner broken; mock-only; no integration tests |

---

## 🔴 CRITICAL — Fix Immediately (see CRITICAL.md)

1. **SecretStr `.get_secret_value()` missing** — all providers crash at runtime
2. **Test runner broken** — numpy/pandas incompatibility, zero tests executing
3. **Cortex SQL injection pattern** — f-string interpolation despite allowlist
4. **Deprecated `asyncio.get_event_loop()`** — 3 occurrences in Snowflake provider

---

## 🟡 HIGH — Fix This Sprint

### 5. Factory Cache Race Condition
**File:** `factory.py`  
**Problem:** `_provider_cache` dict accessed without async lock. Concurrent requests can race to create duplicate providers.  
**Fix:** Add `asyncio.Lock()` with double-check pattern.  
**Effort:** 30 minutes

### 6. DRY: Extract `_validate_identifier` to shared module
**Files:** All 3 providers define identical `_SAFE_IDENTIFIER_RE` + `_validate_identifier()`  
**Fix:** Create `providers/_utils.py`, import from all 3.  
**Effort:** 1 hour

### 7. DRY: Extract `build_schema_info` helper
**Problem:** All 3 providers implement identical `get_schema()` pattern.  
**Fix:** Extract to `providers/_utils.py` as shared coroutine.  
**Effort:** 1 hour

### 8. Remove unused `lru_cache` import
**File:** `providers/snowflake_provider.py` line 8  
**Fix:** Delete `from functools import lru_cache`  
**Effort:** 1 minute

---

## 🟢 MEDIUM — Next Sprint

### 9. Integration Tests via Testcontainers
**Problem:** All tests are mock-only. Critical data layer needs real DB verification.  
**Fix:** Add `tests/integration/` with PostgreSQL container (Supabase), Oracle XE container.  
**Effort:** 1 sprint

### 10. Security Fuzzing Tests
**Problem:** No property-based tests for SQL identifier validation.  
**Fix:** Add `tests/test_security.py` using `hypothesis` library.  
**Effort:** 4 hours

### 11. DataProvider Contract Tests
**Problem:** No shared test suite verifying all 3 providers implement the same contract.  
**Fix:** Parameterized test suite across all providers.  
**Effort:** 4 hours

### 12. Schema Registry Parallel Column Fetch
**File:** `schema/registry.py`  
**Problem:** Sequential column fetch per table — O(n) network round trips.  
**Fix:** `asyncio.gather()` for concurrent column fetch.  
**Effort:** 2 hours

### 13. Deterministic Snowflake Cache Key
**File:** `providers/snowflake_provider.py`  
**Problem:** `cache_key = f"{sql}|{params}"` — list vs tuple produces different keys.  
**Fix:** Use `hashlib.sha256(json.dumps(...)).hexdigest()`.  
**Effort:** 1 hour

### 14. Shared Retry Decorator
**Problem:** No retry/backoff logic in any provider. Transient DB errors cause immediate failure.  
**Fix:** Create `providers/_retry.py` with exponential backoff decorator.  
**Effort:** 4 hours

---

## ⚪ LOW — Backlog

### 15. Async Context Manager (`__aenter__`/`__aexit__`)
Enable `async with get_provider(config) as provider:` usage pattern.

### 16. Redis Cache Backend
Shared `CacheBackend` protocol with `InMemoryCache` + `RedisCache`. Currently only Snowflake has caching (in-memory TTL).

### 17. Streaming Query Results
`execute_query_stream()` yielding `AsyncIterator[list[dict]]` for large result sets.

### 18. Query Audit Log
Structured logging of every query: timestamp, org_id, sql, row_count, execution_time_ms.

### 19. OpenTelemetry Instrumentation
Wrap providers with OTel spans for observability.

### 20. Query Cost Pre-Estimation
`EXPLAIN`-based cost estimation before execution. Block queries exceeding `max_query_cost`.

### 21. DuckDB Provider
Local/edge analytics provider for on-premise deployments.

### 22. PyPI Publication
Package already structured with `pyproject.toml`. Publish for client engineer integration.

### 23. Supabase Realtime Subscriptions
`subscribe()` currently raises `NotImplementedError`.

### 24. Bulk Upsert for `write_back()`
Currently INSERT-only. Add MERGE/ON CONFLICT DO UPDATE support.

---

## Stats

- **Source lines:** ~988 (providers, schema, factory, config, adapters)
- **Test lines:** ~570 (all mock-based, currently broken)
- **Providers:** 3 (Snowflake, Supabase, Oracle)
- **Last audit:** 2026-03-10 (AUDIT.md v3)
