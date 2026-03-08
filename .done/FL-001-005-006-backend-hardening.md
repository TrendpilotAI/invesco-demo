# FL-001 + FL-005 + FL-006 — Backend Production Hardening

**Status:** ✅ Complete  
**Branch:** `railway-deploy`  
**Commit:** `30d7a79b`  
**PR:** https://bitbucket.org/forwardlane/forwardlane-backend/pull-requests/2056

---

## FL-001 — check_env Management Command

**File created:** `core/management/commands/check_env.py`

Validates all critical environment variables at startup. Safe to run in Railway release phase — exits with code 1 if any check fails, aborting the deploy.

**Checks performed:**
- `SECRET_KEY` — must be set and not the dev default
- `DATABASE_URL` — must be set
- `REDIS_URL` — must be set
- `ALLOWED_HOSTS` — must be set; warns if `*` in production
- `DJANGO_ENV` — must be set
- `DEBUG` — must not be True when `DJANGO_ENV=production`

**Optional (warned but not fatal):**
- `SENTRY_DSN`
- `CELERY_BROKER_URL`

**Usage in Railway release phase:**
```
python manage.py check_env
```

---

## FL-005 — pip-audit in CI

**File modified:** `bitbucket-pipelines.yml`, `Pipfile`

Added `pip-audit` security scan step to:
- `master` branch pipeline
- `development` branch pipeline  
- All pull request pipelines

The step runs: `pip-audit --ignore-vuln GHSA-3f63-hfp8-52jq` (ecdsa vulnerability — no upstream fix available)

Also added `pip-audit = "*"` to `Pipfile` `[dev-packages]`.

---

## FL-006 — Expand pylint Scope

**File modified:** `tox.ini`

Added `easy_button`, `analytical`, and `adapters` to the pylint module list so they're linted on every CI run.

---

## Notes

- The `python manage.py check` command couldn't be run locally (full dep stack not installed in sandbox), but `check_env.py` syntax was validated with `ast.parse`.
- There was a rebase conflict on `tox.ini` (remote had removed `--cov-report=term-missing`); resolved by keeping remote's pytest flags + our pylint additions.
