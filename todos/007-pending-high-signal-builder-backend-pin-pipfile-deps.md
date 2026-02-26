# TODO 007 — Pin All Wildcard Pipfile Dependencies

**Status:** pending  
**Priority:** high  
**Repo:** signal-builder-backend  
**Effort:** S (1-2 hours)

## Problem

Multiple production dependencies in `Pipfile` use wildcard versions (`'*'`), creating risks:
- Unpredictable builds across environments
- Silent introduction of breaking changes on new deploys
- Security vulnerabilities from auto-upgrading to vulnerable versions

Unpinned packages: `fastapi-jwt-auth`, `loguru`, `passlib`, `uvicorn`, `gunicorn`, `pydantic`, `dependency-injector`, `python-dotenv`, `flask-admin`, `flask-security-too`, `flask-sqlalchemy`, `httpx`, `aiohttp`, `backoff`, `celery`, `redis`, `pandas`, `jsonpickle`, `openpyxl`

Also: `fastapi==0.92.0` is severely outdated (current is 0.115+). This version has known security issues.

## Files Affected

- `Pipfile`
- `Pipfile.lock` (regenerate)

## Coding Prompt

```
You are hardening the dependency management for signal-builder-backend.

1. In /data/workspace/projects/signal-builder-backend/Pipfile:
   - Replace all wildcard (*) versions with pinned versions
   - Use the currently installed versions from Pipfile.lock as the pinned baseline
   - For fastapi==0.92.0, evaluate upgrading to latest stable (0.115.x) — note any breaking changes
   - Keep versions consistent (e.g., if pydantic is v1, don't upgrade to v2 without full migration)

2. Run: cd /data/workspace/projects/signal-builder-backend && pipenv lock --clear

3. Add a comment block at the top of Pipfile explaining the pinning policy:
   # All production dependencies must be pinned to exact versions.
   # To upgrade: pipenv update <package>, test, then commit Pipfile.lock.

4. Check if fastapi-jwt-auth is still maintained (it may be abandoned).
   If so, note this in a comment and add to the security backlog.

5. Verify: pipenv check (runs safety check for known CVEs)
```

## Acceptance Criteria

- [ ] No `'*'` versions remain in `[packages]` section of Pipfile
- [ ] `pipenv lock` succeeds with no conflicts
- [ ] App starts successfully with pinned versions
- [ ] `pipenv check` shows no critical CVEs (or documents accepted exceptions)

## Dependencies

None.
