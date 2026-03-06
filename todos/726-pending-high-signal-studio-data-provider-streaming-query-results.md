# TODO 726: Streaming Query Results via Async Generators

**Repo:** signal-studio-data-provider  
**Priority:** HIGH  
**Effort:** M (2-3 days)  
**Dependencies:** None

## Description
`execute_query` returns `QueryResult` with all rows in memory. For enterprise Snowflake queries returning millions of rows, this causes OOM crashes. Add a `stream_query()` method to the `DataProvider` protocol that returns `AsyncGenerator[dict[str, Any], None]`.

## Acceptance Criteria
- [ ] `DataProvider` protocol gains `stream_query(sql, params, batch_size=1000)` method
- [ ] All three providers implement streaming (Snowflake cursor.fetchmany, asyncpg server-side cursor, Oracle cursor.fetchmany)
- [ ] `execute_signal` uses streaming internally for large result sets
- [ ] Memory usage stays <100MB for 10M-row queries
- [ ] Tests verify async generator behavior

## Coding Prompt
```python
# In providers/base.py, add to DataProvider protocol:
async def stream_query(
    self, sql: str, 
    params: dict[str, Any] | None = None,
    batch_size: int = 1000
) -> AsyncGenerator[dict[str, Any], None]:
    """Stream query results in batches to avoid loading all rows into memory."""
    ...

# In providers/snowflake_provider.py:
async def stream_query(self, sql, params=None, batch_size=1000):
    async with self._get_cursor() as cursor:
        await cursor.execute(sql, params or {})
        while True:
            rows = cursor.fetchmany(batch_size)
            if not rows:
                break
            for row in rows:
                yield dict(zip([col[0] for col in cursor.description], row))

# In providers/supabase_provider.py (asyncpg server-side cursor):
async def stream_query(self, sql, params=None, batch_size=1000):
    async with self._pool.acquire() as conn:
        async with conn.transaction():
            async for row in conn.cursor(sql, *list(params.values() if params else [])):
                yield dict(row)
```
