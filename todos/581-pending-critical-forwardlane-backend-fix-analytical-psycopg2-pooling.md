# TODO-581: Fix analytical/views.py — Use Django Connection Pool

**Priority:** CRITICAL
**Repo:** forwardlane-backend
**Effort:** S (2h)
**Status:** pending

## Problem
`analytical/views.py` creates a new raw `psycopg2.connect()` on every HTTP request via `get_analytical_conn()`. With 5 views each calling this, a single page load opens 5 fresh TCP connections to Postgres. Under any load this will exhaust Postgres's `max_connections` limit (default 100).

`easy_button/views.py` correctly uses `connections['analytical'].cursor()` which is pooled via Django's `CONN_MAX_AGE=60` setting.

## Fix

Replace the entire `get_analytical_conn()` function and all usages throughout `analytical/views.py`:

```python
# REMOVE this function entirely:
def get_analytical_conn():
    ...psycopg2.connect(ANALYTICAL_DB_URL)...

# REPLACE all usages like:
conn = get_analytical_conn()
with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
    cur.execute(...)
    rows = cur.fetchall()

# WITH Django connections (already configured in settings):
from django.db import connections
with connections['analytical'].cursor() as cur:
    cur.execute(...)
    rows = [dict(zip([col[0] for col in cur.description], row)) for row in cur.fetchall()]
```

Also remove unused imports: `psycopg2`, `psycopg2.extras`, `os` (for ANALYTICAL_DB_URL), `time`.

## Files
- `analytical/views.py` — full refactor

## Acceptance Criteria
- [ ] `get_analytical_conn()` function is deleted
- [ ] All 5 view classes use `connections['analytical'].cursor()`
- [ ] `psycopg2` and `psycopg2.extras` imports removed from `analytical/views.py`
- [ ] Tests pass: `python manage.py test analytical`
- [ ] Load test shows no connection exhaustion under 10 concurrent requests

## Dependencies
- TODO-213 (CONN_MAX_AGE=60 — should already be done)
