# 336 — Fix analytical/ Raw psycopg2 Connections

**Priority:** CRITICAL
**Repo:** forwardlane-backend
**Effort:** M (2-3 hours)
**Category:** Performance / Architecture

## Description
`analytical/views.py` creates a fresh `psycopg2.connect(ANALYTICAL_DB_URL)` on every request
across all 5 analytical endpoints. This bypasses Django's connection pooling (`CONN_MAX_AGE=60`)
and creates new TCP connections to PostgreSQL on every HTTP request.

## Impact
- 5 new DB connections per concurrent request
- 50-200ms connection overhead per request
- PostgreSQL connection limit exhausted under load
- Cannot benefit from CONN_MAX_AGE pooling

## Fix
Port the `_analytical_cursor()` pattern already used in `easy_button/views.py`:

```python
# In analytical/views.py — REPLACE:
import psycopg2
import psycopg2.extras

def _get_analytical_conn():
    conn = psycopg2.connect(ANALYTICAL_DB_URL)
    return conn

# WITH:
from django.db import connections

def _analytical_cursor():
    return connections['analytical'].cursor()
```

Then replace all usages:
```python
# Before:
with _get_analytical_conn() as conn:
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(sql)
        rows = cur.fetchall()

# After:
with _analytical_cursor() as cur:
    cur.execute(sql)
    columns = [col[0] for col in cur.description]
    rows = [dict(zip(columns, row)) for row in cur.fetchall()]
```

## Files to Change
- `analytical/views.py` — remove psycopg2 imports, replace `_get_analytical_conn()`, update all 5 view functions

## Acceptance Criteria
- [ ] No `psycopg2.connect()` calls in `analytical/views.py`
- [ ] All 5 analytical endpoints still return correct data
- [ ] `import psycopg2` removed from `analytical/views.py`
- [ ] Verified with load test: repeated requests reuse connection (check pg_stat_activity)
