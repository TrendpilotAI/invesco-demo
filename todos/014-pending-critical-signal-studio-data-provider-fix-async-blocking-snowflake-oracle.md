---
status: pending
priority: p1
issue_id: "014"
tags: [python, async, snowflake, oracle, performance, signal-studio-data-provider]
dependencies: []
---

# Fix Async Blocking: Snowflake and Oracle Providers Block the Event Loop

## Problem Statement

`SnowflakeProvider` and `OracleProvider` declare all methods as `async def` but internally call synchronous blocking functions (`snowflake.connector.connect()`, `cursor.execute()`, `pool.acquire()`, etc.) directly on the event loop. Under any real async load (FastAPI, aiohttp, Signal Studio backend), a single slow Snowflake query will freeze the entire event loop, making all concurrent requests unresponsive. This is a production-blocking correctness bug.

## Findings

**SnowflakeProvider:**
- `_get_connection()` calls `snowflake.connector.connect()` — blocking I/O (TLS handshake, auth)
- `_cursor()` returns a sync cursor
- `execute_query()` calls `cur.execute()` and `cur.fetchall()` — blocking, can take seconds
- `test_connection()`, `get_tables()`, `get_columns()`, `cortex_complete()`, `cortex_embed()` all block

**OracleProvider:**
- `_get_pool()` calls `oracledb.create_pool()` — blocking
- `execute_query()` uses `with pool.acquire() as conn:` — sync context manager in async def
- `cur.execute()` and `cur.fetchall()` are blocking
- `write_back()` blocks on `conn.commit()`

**Root cause:** Both connectors have synchronous APIs. The async def wrapper gives a false async interface that doesn't yield to the event loop.

## Proposed Solutions

### Option A: Wrap in `asyncio.run_in_executor` (Recommended — Immediate Fix)
Use `loop.run_in_executor(None, sync_fn, *args)` to offload blocking calls to a thread pool. This is safe, non-breaking, and can be done incrementally.

```python
import asyncio

async def execute_query(self, sql, params=None):
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(None, self._sync_execute, sql, params)
    return result

def _sync_execute(self, sql, params):
    cur = self._cursor()
    try:
        cur.execute(sql, params or {})
        columns = [desc[0] for desc in cur.description] if cur.description else []
        rows = [dict(zip(columns, row)) for row in cur.fetchall()]
        return columns, rows
    finally:
        cur.close()
```

- **Pros:** Minimal changes, safe, immediate fix, works with existing connector
- **Cons:** Thread pool overhead (~1ms per call), not true async

### Option B: Migrate to Native Async Connectors (Long-term)
- Snowflake: Use `snowflake-snowpark-python` async API or async adapter
- Oracle: `oracledb` v2+ has async support via `oracledb.connect_async()`
- **Pros:** True async, better performance under load
- **Cons:** Larger migration, potential API differences, more testing needed

### Recommended: Option A now, Option B later

## Recommended Action

Implement Option A (run_in_executor) for both providers:

1. Extract all blocking I/O into private sync methods (`_sync_execute`, `_sync_connect`, etc.)
2. Wrap each in `asyncio.get_running_loop().run_in_executor(None, ...)` in the async methods
3. Add `asyncio.Semaphore` to cap concurrent DB threads (e.g., max 10)
4. Add a test that verifies no event loop blocking: run query with `asyncio.wait_for(..., timeout=0.5)` and verify concurrent tasks still progress

## Acceptance Criteria

- [ ] `SnowflakeProvider.execute_query()` does not block the event loop (verified by concurrent async task test)
- [ ] `OracleProvider.execute_query()` does not block the event loop
- [ ] All async methods in both providers delegate blocking I/O to thread executor
- [ ] `SnowflakeProvider._get_connection()` is called in executor, not directly
- [ ] `OracleProvider._get_pool()` is called in executor on first use
- [ ] Tests run with `pytest-asyncio` and include a concurrency test
- [ ] No performance regression on single-query benchmarks (within 10%)
- [ ] `asyncio.Semaphore` limits concurrent thread pool usage

## Coding Prompt

```
TASK: Fix async blocking in SnowflakeProvider and OracleProvider in the signal-studio-data-provider repo.

REPO: /data/workspace/projects/signal-studio-data-provider/

FILES TO MODIFY:
  - providers/snowflake_provider.py
  - providers/oracle_provider.py
  - tests/test_providers.py

APPROACH:
1. In SnowflakeProvider:
   a. Create `_sync_execute(self, sql, params)` that does the cursor create/execute/fetchall/close
   b. Create `_sync_connect(self)` that calls snowflake.connector.connect()
   c. In `execute_query()`, use `await asyncio.get_running_loop().run_in_executor(None, self._sync_execute, sql, params)`
   d. In `test_connection()`, `cortex_complete()`, `cortex_embed()`, wrap sync calls similarly
   e. Add `self._executor_semaphore = asyncio.BoundedSemaphore(10)` in __init__

2. In OracleProvider:
   a. Create `_sync_execute(self, sql, params)` extracting the pool.acquire/cursor.execute/fetchall logic
   b. In `execute_query()`, await run_in_executor
   c. In `write_back()`, wrap the sync DB calls
   d. In `test_connection()`, wrap the sync check

3. Add tests:
   a. `test_snowflake_execute_is_non_blocking`: create two coroutines, run concurrently, verify both complete
   b. `test_oracle_execute_is_non_blocking`: same pattern
   Use `asyncio.gather()` with mocked connectors that have a `time.sleep(0.1)` to simulate I/O

IMPORTANT: Do NOT change the public async API signatures. Only internal implementation changes.
```

## Dependencies

None — this is a standalone fix.

## Estimated Effort

M (1-2 days)

## Work Log

### 2026-02-26 — Initial triage

**By:** Planning Agent

**Actions:**
- Identified sync-in-async pattern in SnowflakeProvider and OracleProvider
- Confirmed Snowflake connector has no native async API
- Confirmed oracledb v2+ has async support but migration is higher risk
- Recommended run_in_executor as immediate fix

**Learnings:**
- Both providers are architecturally identical in their sync-blocking pattern
- The issue is invisible in tests because tests mock the connector
- Will only manifest under production load
