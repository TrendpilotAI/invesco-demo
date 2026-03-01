# TODO-352: Pydantic v2 Migration + FastAPI Upgrade
**Project:** signal-builder-backend  
**Priority:** P0  
**Effort:** M (3-5 days)  
**Status:** pending  
**Created:** 2026-03-01

---

## Description

Migrate signal-builder-backend from Pydantic v1.10.13 (EOL) to Pydantic v2 and FastAPI from 0.92 to latest (0.115+). Pydantic v1 is EOL with known vulnerabilities; v2 is 5–50x faster for validation. FastAPI 0.92 is severely outdated with many security patches and features in newer versions.

---

## Full Autonomous Coding Prompt

```
You are working on the signal-builder-backend FastAPI service located at /data/workspace/projects/signal-builder-backend/.

TASK: Migrate from Pydantic v1.10.13 → v2 and FastAPI 0.92 → latest (0.115+).

STEP 1 — Update Pipfile:
- Change `pydantic = "==1.10.13"` to `pydantic = ">=2.0,<3"`
- Change `fastapi = "==0.92.0"` to `fastapi = ">=0.115,<1"`
- Change `pydantic[email] = "==1.10.13"` to `pydantic[email] = ">=2.0,<3"` if present
- Run: cd /data/workspace/projects/signal-builder-backend && pipenv update pydantic fastapi
- If pydantic-settings is needed: add `pydantic-settings = ">=2.0,<3"` to Pipfile

STEP 2 — Find all API changes. Run these commands:
```
grep -rn "\.dict()" apps/ --include="*.py"
grep -rn "\.schema()" apps/ --include="*.py"
grep -rn "@validator" apps/ --include="*.py"
grep -rn "@root_validator" apps/ --include="*.py"
grep -rn "from pydantic import" apps/ --include="*.py"
grep -rn "class Config:" apps/ --include="*.py"
grep -rn "orm_mode" apps/ --include="*.py"
```

STEP 3 — Apply changes systematically across all files:
- `.dict()` → `.model_dump()`
- `.dict(exclude_unset=True)` → `.model_dump(exclude_unset=True)`
- `.schema()` → `.model_json_schema()`
- `@validator("field")` → `@field_validator("field")` with `@classmethod` decorator
- `@root_validator` → `@model_validator`
- `class Config: orm_mode = True` → `model_config = ConfigDict(from_attributes=True)`
- `from pydantic import validator` → `from pydantic import field_validator`
- `from pydantic import BaseSettings` → `from pydantic_settings import BaseSettings`
- `Optional[X]` style validators: update `values` dict param to `info: FieldValidationInfo`
- `Schema()` → `Field()`

STEP 4 — Update settings files:
- `core/settings.py` and `settings/` directory: migrate BaseSettings imports to pydantic-settings
- Check `settings/common.py`, `settings/development.py`, `settings/production.py`

STEP 5 — Test each app module:
```
cd /data/workspace/projects/signal-builder-backend
pipenv run pytest apps/signals/ -v
pipenv run pytest apps/users/ -v
pipenv run pytest apps/schema_builder/ -v
pipenv run pytest apps/analytical_db/ -v
pipenv run pytest apps/health/ -v
pipenv run pytest -v  # full suite
```

STEP 6 — Fix any import errors revealed by FastAPI upgrade:
- `from fastapi import FastAPI` patterns should still work
- Check response_model usage — Pydantic v2 changes validation behavior
- Update any `response_model_exclude_unset` patterns if broken

STEP 7 — Verify no v1 imports remain:
```
grep -rn "pydantic.v1" apps/ core/ settings/ --include="*.py"
grep -rn "from pydantic import validator" apps/ core/ settings/ --include="*.py"
grep -rn "orm_mode" apps/ core/ settings/ --include="*.py"
```
All should return empty.

STEP 8 — Run the app to verify startup:
```
cd /data/workspace/projects/signal-builder-backend
pipenv run python -c "from apps.main import app; print('OK')"
```
```

---

## Dependencies

- None (this is a P0 foundation task)
- Must complete BEFORE: rate-limiting (TODO-353), schema-builder-tests (TODO-356)

---

## Effort Estimate

**3–5 days** — Schema changes are widespread across all apps/ directories. Validators need careful refactoring to v2 semantics. Testing each module after migration adds time.

---

## Acceptance Criteria

- [ ] `pipenv run pip show pydantic` reports version 2.x
- [ ] `pipenv run pip show fastapi` reports version 0.115+
- [ ] `grep -rn "orm_mode\|@validator\|\.dict()\|from pydantic import validator" apps/ core/ settings/` returns no results
- [ ] All existing tests pass: `pipenv run pytest -v` exits 0
- [ ] App starts without import errors
- [ ] No `pydantic.v1` compatibility shim imports anywhere
- [ ] `pydantic-settings` package used for all BaseSettings classes
