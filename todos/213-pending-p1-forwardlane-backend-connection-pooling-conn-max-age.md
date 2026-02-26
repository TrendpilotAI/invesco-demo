# 213 · CONNECTION POOLING — ADD CONN_MAX_AGE TO DATABASES SETTINGS

**Repo:** forwardlane-backend  
**Priority:** P1 (performance — prevents connection exhaustion under demo load)  
**Effort:** S (30 minutes)  
**Status:** pending

---

## Task Description

`analytical/views.py` creates a new `psycopg2.connect()` on every HTTP request (no connection
reuse). Under demo load (10+ req/s), this exhausts Railway Postgres's connection limit.

`easy_button/views.py` correctly uses Django `connections['analytical']`, but without
`CONN_MAX_AGE` configured, Django also creates new connections per request.

**Fix (Part A — Required):** Add `CONN_MAX_AGE: 60` to both `'default'` and `'analytical'`
database entries in `forwardlane/settings/databases.py`. This enables Django's built-in
persistent connection reuse.

**Fix (Part B — Optional but recommended):** Migrate `analytical/views.py` from raw psycopg2
to Django's `connections['analytical']` so it also benefits from pooling and uses one consistent
DB access pattern across both apps.

---

## Coding Prompt (Agent-Executable)

```
You are modifying forwardlane-backend at /data/workspace/projects/forwardlane-backend/.

TASK: Add CONN_MAX_AGE to database settings and optionally migrate analytical/views.py.

STEP 1 — Find the databases settings file:
Run: find /data/workspace/projects/forwardlane-backend/forwardlane/settings -name "*.py" | xargs grep -l "DATABASES"
Open that file (likely databases.py or base.py).

STEP 2 — Add CONN_MAX_AGE to both database entries:
In the DATABASES dict, find the 'default' entry and add 'CONN_MAX_AGE': 60.
Find the 'analytical' entry (may be named differently) and add 'CONN_MAX_AGE': 60.

Example — if the file looks like:
  DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.postgresql',
          'NAME': ...,
          ...
      },
      'analytical': {
          'ENGINE': 'django.db.backends.postgresql',
          ...
      }
  }

Change to:
  DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.postgresql',
          'NAME': ...,
          ...
          'CONN_MAX_AGE': 60,   # Persistent connection reuse (60s idle timeout)
      },
      'analytical': {
          'ENGINE': 'django.db.backends.postgresql',
          ...
          'CONN_MAX_AGE': 60,   # Persistent connection reuse (60s idle timeout)
      }
  }

NOTE: If databases are parsed from DATABASE_URL/ANALYTICAL_DATABASE_URL using dj-database-url,
the CONN_MAX_AGE must be passed to the parse() call:
  import dj_database_url
  DATABASES['default'] = dj_database_url.parse(os.environ['DATABASE_URL'], conn_max_age=60)
  DATABASES['analytical'] = dj_database_url.parse(os.environ['ANALYTICAL_DATABASE_URL'], conn_max_age=60)

STEP 3 — Verify settings load:
Run: cd /data/workspace/projects/forwardlane-backend && python manage.py check --database default
Run: python manage.py check --database analytical (if that database alias exists)

STEP 4 (Optional but recommended) — Fix analytical/views.py to use Django connections:
In analytical/views.py, the get_analytical_conn() function uses raw psycopg2.
Replace it with Django's connection management:

Find:
  import psycopg2
  import psycopg2.extras
  
  ANALYTICAL_DB_URL = os.environ.get("ANALYTICAL_DATABASE_URL", "postgresql://...")
  
  def get_analytical_conn():
      for attempt in range(3):
          try:
              conn = psycopg2.connect(ANALYTICAL_DB_URL)
              conn.autocommit = True
              return conn
          except psycopg2.OperationalError:
              ...

Replace with:
  from django.db import connections
  
  def _analytical_cursor():
      """Returns a Django-managed cursor for the analytical database.
      Uses persistent connections (CONN_MAX_AGE) configured in settings.
      """
      return connections['analytical'].cursor()

Then update each view's DB access pattern:
  - Replace `conn = get_analytical_conn()` → `with _analytical_cursor() as cursor:`
  - Replace `cur = conn.cursor(cursor_factory=RealDictCursor)` → use cursor directly
  - Replace `dict(row)` row conversion → `zip([d[0] for d in cursor.description], row)`
  - Remove all `conn.close()` calls (Django manages connection lifecycle)
  - Remove all psycopg2 imports if no longer needed

STEP 5 — Verify no regressions:
Run: cd /data/workspace/projects/forwardlane-backend && python manage.py check
```

---

## Files to Modify

| File | Change |
|------|--------|
| `forwardlane/settings/databases.py` (or base.py) | Add `CONN_MAX_AGE: 60` to both DB entries |
| `analytical/views.py` | (Optional) Replace psycopg2 with Django `connections['analytical']` |

---

## Acceptance Criteria

- [ ] `CONN_MAX_AGE: 60` present in `DATABASES['default']` settings
- [ ] `CONN_MAX_AGE: 60` present in `DATABASES['analytical']` settings
- [ ] `python manage.py check` passes
- [ ] No new psycopg2 `connect()` calls in `analytical/views.py` (if Step 4 done)
- [ ] All analytical endpoints still return correct data after change

---

## Notes

- `CONN_MAX_AGE=60` means Django holds the connection open for 60s after last use
- At demo scale (10–50 req/s), this reduces new connection overhead by ~80%
- For higher scale: add PgBouncer as Railway service (transaction pooling mode)
- This change is trivially reversible: set `CONN_MAX_AGE=0` to revert to per-request connections
- Railway Postgres default `max_connections=100`; with 2 Django workers + 2 Celery workers
  connecting to 2 databases → max ~16 persistent connections with CONN_MAX_AGE=60
