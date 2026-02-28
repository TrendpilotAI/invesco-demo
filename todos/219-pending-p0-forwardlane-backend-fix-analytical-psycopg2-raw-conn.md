# TODO 219: Fix analytical/ raw psycopg2 connection leak (P0 — critical)

**Repo:** forwardlane-backend  
**Priority:** P0 — Critical (production connection exhaustion risk)  
**Effort:** M (4–8 hours)  
**Status:** pending

## Problem

`analytical/views.py` opens a **new psycopg2 connection on every HTTP request** via:
```python
def get_analytical_conn():
    conn = psycopg2.connect(ANALYTICAL_DB_URL)
    conn.autocommit = True
    return conn
```

These connections are **never closed** in finally blocks — they rely on Python GC. Under load
(Invesco demo with multiple users) this will exhaust Postgres max_connections and cause 503s.

`easy_button/views.py` correctly uses Django's `connections['analytical']` pool — that pattern
should be applied to the `analytical/` app as well.

## Acceptance Criteria
- [ ] `analytical/views.py` uses `from django.db import connections` → `connections['analytical']`
- [ ] All raw `psycopg2.connect()` calls removed from view layer
- [ ] Connection closed/returned to pool in `finally` blocks
- [ ] `get_analytical_conn()` helper function either deleted or moved to a test helper only
- [ ] No regression on existing analytical/ endpoints (GET /api/analytics/*)
- [ ] Unit test added: `analytical/tests/test_views.py` with at least dashboard endpoint mocked

## Coding Prompt

```
Fix /data/workspace/projects/forwardlane-backend/analytical/views.py:

1. Replace all occurrences of:
     conn = get_analytical_conn()
     with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
   with:
     from django.db import connections
     with connections['analytical'].cursor() as cur:

2. Django cursors return lists of tuples by default. Use:
     from django.db.models.sql.compiler import SQLCompiler  # not needed
   Instead, after cursor.execute(), use:
     columns = [col[0] for col in cur.description]
     rows = [dict(zip(columns, row)) for row in cur.fetchall()]
   (This replaces psycopg2.extras.RealDictCursor behavior)

3. Delete the get_analytical_conn() function and remove psycopg2 imports from views.py

4. Add ANALYTICAL_DATABASE_URL to django DATABASES dict in settings (it may already be there
   as 'analytical' — check settings/base.py or settings.py.example)

5. Run: python manage.py check --settings=forwardlane.tests_settings
6. Add tests/test_views.py to analytical/ app with at least 3 endpoint tests using TestCase
   and patch('django.db.connections') to mock DB calls.
```

## Dependencies
- Requires ANALYTICAL_DATABASE_URL in Railway env vars (already set)
- Should be done before 214-pending-p0-forwardlane-backend-pytest-tests-easy-button-analytical.md

## Risk
Medium — easy_button already uses the correct pattern so the DB alias is proven to work.
The main risk is RealDictCursor → manual dict mapping, which needs careful testing.
