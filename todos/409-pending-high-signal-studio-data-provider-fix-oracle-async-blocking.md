# TODO 409 — Fix Oracle Provider Sync-in-Async Blocking

**Repo:** signal-studio-data-provider  
**Priority:** High  
**Effort:** Small (0.5 days)  
**Status:** pending

## Description
`OracleProvider.execute_query()` and other methods call synchronous `oracledb` API inside `async def`, blocking the event loop. Same issue as Snowflake (C-2 in AUDIT.md) but not yet fixed for Oracle.

**File:** `providers/oracle_provider.py`

## Task
Wrap all synchronous oracledb calls in `asyncio.to_thread()`:

```python
import asyncio

async def execute_query(self, sql: str, params=None) -> QueryResult:
    pool = self._get_pool()
    t0 = time.time()
    def _run():
        with pool.acquire() as conn:
            cur = conn.cursor()
            cur.execute(sql, params or {})
            cols = [d[0] for d in cur.description] if cur.description else []
            rows = [dict(zip(cols, r)) for r in cur.fetchall()]
            cur.close()
            return cols, rows
    cols, rows = await asyncio.to_thread(_run)
    elapsed = (time.time() - t0) * 1000
    return QueryResult(rows=rows, columns=cols, row_count=len(rows), execution_time_ms=elapsed)
```

Apply same pattern to: `get_schema`, `get_tables`, `get_columns`, `test_connection`, `write_back`.

Also fix `_get_pool()` to be called from async context (lazy init is fine but pool creation should be thread-safe).

## Acceptance Criteria
- [ ] No synchronous oracledb calls directly in async methods
- [ ] All blocking ops wrapped in asyncio.to_thread()
- [ ] Tests updated (existing mocks should still work)
- [ ] Event loop not blocked during Oracle queries

## Dependencies
None (parallel to P0-002 Snowflake async fix)
