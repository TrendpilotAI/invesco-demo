# TODO 312 — Fix Snowflake Sync Connector Blocking Async Event Loop

**Priority:** P0 🔴  
**Repo:** signal-studio-data-provider  
**File:** providers/snowflake_provider.py  
**Effort:** M (2-4 hours)  
**Status:** pending

---

## Description

`SnowflakeProvider` declares all methods as `async def` but calls the fully synchronous `snowflake.connector` API internally (`cur.execute()`, `cur.fetchall()`, `conn.commit()`, `executemany()`). These calls block the entire asyncio event loop for the query duration — potentially several seconds — starving all other coroutines.

Affected lines:
- `execute_query`: `cur.execute(sql, params or {})`  + `cur.fetchall()`
- `test_connection`: `cur.execute("SELECT 1")`
- `write_back`: `cur.executemany(...)` + `conn.commit()`
- `get_tables`, `get_columns`: any cursor execute calls

---

## Coding Prompt

```
Fix SnowflakeProvider in /data/workspace/projects/signal-studio-data-provider/providers/snowflake_provider.py
to not block the asyncio event loop.

For each async method that calls the sync snowflake.connector API:

1. Extract the synchronous work into an inner `def _run()` function
2. Wrap with `await asyncio.to_thread(_run)` (Python 3.9+)

Example pattern for execute_query:

import asyncio

async def execute_query(self, sql: str, params: dict[str, Any] | None = None) -> QueryResult:
    cache_key = f"{sql}|{params}"
    cached = self._cache.get(cache_key)
    if cached is not None:
        return cached

    def _run() -> tuple[list[str], list[tuple], float]:
        cur = self._cursor()
        t0 = time.time()
        try:
            cur.execute(sql, list(params.values()) if params else [])
            cols = [d[0] for d in cur.description] if cur.description else []
            rows = cur.fetchall()
            return cols, rows, (time.time() - t0) * 1000
        finally:
            cur.close()

    columns, raw_rows, elapsed = await asyncio.to_thread(_run)
    rows = [dict(zip(columns, row)) for row in raw_rows]
    cost = elapsed / 60_000
    self._total_credits += cost
    result = QueryResult(rows=rows, columns=columns, row_count=len(rows), execution_time_ms=elapsed, cost=cost)
    self._cache.set(cache_key, result)
    return result

Apply the same pattern to: test_connection, write_back, get_tables, get_columns, execute_signal.

Also fix parameter binding: Snowflake connector uses positional %s, not dict kwargs.
Change: cur.execute(sql, params or {})
To:     cur.execute(sql, list(params.values()) if params else [])
```

---

## Dependencies

None — standalone fix.

## Acceptance Criteria

- [ ] No synchronous connector calls outside `asyncio.to_thread()`
- [ ] `pytest -x tests/` still passes
- [ ] Parameter binding works correctly with a list of values
- [ ] Manual test: concurrent execute_query calls don't block each other
