# TODO 729: Snowflake Query Cost Pre-Estimation

**Repo:** signal-studio-data-provider  
**Priority:** MEDIUM  
**Effort:** S (half day)  
**Dependencies:** None (config field max_query_cost already exists)

## Description
`OrgConfig.max_query_cost` exists but is unused. Wire it up: before executing any Snowflake query, run `EXPLAIN` to get estimated byte scan, convert to credit estimate, and block if it exceeds the limit.

## Acceptance Criteria
- [ ] `SnowflakeProvider.execute_query` runs `EXPLAIN` before execution
- [ ] Converts `partitions_scanned` + `bytes_scanned` estimate to credit cost
- [ ] Raises `QueryCostExceededError` if estimated cost > `max_query_cost`
- [ ] EXPLAIN step can be disabled per-query via `skip_cost_check=True` param
- [ ] Warning logged (not blocked) if cost is within 80-100% of limit
- [ ] Tests mock EXPLAIN responses

## Coding Prompt
```python
# In providers/snowflake_provider.py:
BYTES_PER_CREDIT = 1_000_000_000  # rough estimate: 1 credit ≈ 1GB scanned

async def _estimate_cost(self, cursor, sql: str) -> float:
    """Run EXPLAIN and return estimated Snowflake credit cost."""
    cursor.execute(f"EXPLAIN {sql}")
    row = cursor.fetchone()
    if row and "bytes_scanned" in str(row):
        # Parse from EXPLAIN output
        bytes_scanned = self._parse_explain_bytes(row)
        return bytes_scanned / BYTES_PER_CREDIT
    return 0.0

async def execute_query(self, sql, params=None, skip_cost_check=False):
    async with self._get_cursor() as cursor:
        if not skip_cost_check and self._config.snowflake.max_query_cost > 0:
            estimated = await self._estimate_cost(cursor, sql)
            limit = self._config.max_query_cost
            if estimated > limit:
                raise QueryCostExceededError(
                    f"Query estimated at {estimated:.4f} credits, limit is {limit}"
                )
        cursor.execute(sql, params or {})
        rows = cursor.fetchall()
        ...
```
