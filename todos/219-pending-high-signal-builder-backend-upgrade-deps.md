# TODO: Upgrade Core Dependencies (signal-builder-backend)

**Priority:** High  
**Repo:** signal-builder-backend  
**Effort:** 4 hours  
**Status:** pending

## Description
FastAPI is pinned to 0.92.0 (2+ years old). SQLAlchemy, alembic, asyncpg also outdated. Security vulnerabilities and missing features.

## Coding Prompt
```
In /data/workspace/projects/signal-builder-backend:

1. Update Pipfile dependencies:
   - fastapi: 0.92.0 → latest stable (>=0.115)
   - SQLAlchemy: 2.0.4 → latest 2.x
   - alembic: 1.9.4 → latest
   - asyncpg: 0.27.0 → latest
   - psycopg2: 2.9.5 → latest

2. Run: pipenv update
3. Run tests: python -m pytest tests/ -x -q
4. Fix any breaking changes:
   - FastAPI 0.9x→0.115: Check for deprecated response_model_exclude_unset usage
   - SQLAlchemy 2.0 changes are mostly compatible but check session.execute() returns
5. Update Pipfile.lock
6. Run: pipenv run python api.py (verify startup)
```

## Dependencies
- None (foundational)

## Acceptance Criteria
- All tests pass with upgraded deps
- App starts without errors
- No deprecation warnings in startup logs
