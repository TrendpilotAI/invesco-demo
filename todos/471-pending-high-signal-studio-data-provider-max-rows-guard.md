---
id: "471"
status: pending
priority: high
repo: signal-studio-data-provider
title: "Add max_rows guard to execute_query across all providers"
effort: S
dependencies: []
created: "2026-03-04"
---

## Task Description

None of the three providers limit result set sizes. An NL→SQL generated `SELECT * FROM customers` on a 10M-row table will OOM the process. Must add configurable row cap.

## Coding Prompt

1. In `config.py`, add `max_query_rows` to `OrgConfig`:
```python
class OrgConfig(BaseModel):
    ...
    max_query_rows: int = 10_000  # Configurable per org
```

2. Create a utility function in `providers/_utils.py` (new file):
```python
import re

_LIMIT_RE = re.compile(r'\bLIMIT\s+\d+', re.IGNORECASE)

def inject_row_limit(sql: str, max_rows: int) -> str:
    """Wrap SQL in a LIMIT subquery if no LIMIT clause present."""
    if _LIMIT_RE.search(sql):
        return sql  # Already has LIMIT — respect it
    # Wrap to avoid interfering with CTEs, ORDER BY, etc.
    return f"SELECT * FROM ({sql}) __row_capped_q LIMIT {max_rows}"
```

3. Apply in each provider's `execute_query()`:

**supabase_provider.py:**
```python
async def execute_query(self, sql: str, params=None, jwt=None) -> QueryResult:
    sql = inject_row_limit(sql, self._config.max_query_rows)
    ...
```

**snowflake_provider.py** (in `_execute_query_sync`):
```python
def _execute_query_sync(self, sql: str, params=None) -> QueryResult:
    sql = inject_row_limit(sql, self._config.max_query_rows)
    ...
```

**oracle_provider.py** (in `_execute_query_sync`):
```python
def _execute_query_sync(self, sql: str, params=None) -> QueryResult:
    sql = inject_row_limit(sql, self._config.max_query_rows)
    ...
```

4. Add tests:
```python
def test_inject_row_limit_adds_limit():
    sql = "SELECT * FROM orders"
    result = inject_row_limit(sql, 1000)
    assert "LIMIT 1000" in result

def test_inject_row_limit_respects_existing_limit():
    sql = "SELECT * FROM orders LIMIT 50"
    result = inject_row_limit(sql, 1000)
    assert result == sql  # Unchanged

def test_inject_row_limit_handles_cte():
    sql = "WITH cte AS (SELECT 1) SELECT * FROM cte"
    result = inject_row_limit(sql, 500)
    assert "LIMIT 500" in result
```

## Acceptance Criteria
- [ ] `max_query_rows` added to `OrgConfig` (default 10,000)
- [ ] `inject_row_limit()` utility in `providers/_utils.py`
- [ ] All 3 providers apply row limit before execution
- [ ] SQL with existing LIMIT is not double-wrapped
- [ ] Tests for limit injection, passthrough, CTE handling
