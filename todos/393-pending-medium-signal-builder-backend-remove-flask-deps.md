# TODO-393: Remove Flask Dependencies — Complete sqladmin Migration

**Repo:** signal-builder-backend  
**Priority:** Medium  
**Status:** Pending  
**Created:** 2026-03-02  

## Description

Flask deps (flask-admin, flask-security-too, flask-sqlalchemy) still exist in Pipfile
alongside the FastAPI stack. Admin was migrated to sqladmin, but Flask packages remain.
This increases attack surface, dependency conflicts risk, and Docker image size.

## Execution Prompt

```
You are removing Flask dependencies from signal-builder-backend at /data/workspace/projects/signal-builder-backend/.

Steps:
1. Read Pipfile — identify all Flask-related packages
2. Read apps/admin/ — confirm sqladmin is fully in use, no Flask imports remain
3. Search for any Flask imports across the codebase:
   `grep -r "from flask\|import flask" apps/ --include="*.py"`
4. If any Flask imports found: replace with FastAPI/sqladmin equivalents
5. Remove from Pipfile: flask, flask-admin, flask-security-too, flask-sqlalchemy, 
   and any Flask-specific deps not needed by sqladmin
6. Run: `pipenv install` to rebuild lockfile
7. Run: `pytest` to confirm nothing broke
8. Update Pipfile.lock

Acceptance: `grep -r "flask" Pipfile` returns only sqladmin (which is FastAPI-native).
```

## Effort Estimate
- S (1-2 hours)

## Acceptance Criteria
- [ ] No Flask packages in Pipfile production deps
- [ ] All admin functionality working via sqladmin
- [ ] All 134+ tests still passing
- [ ] Pipfile.lock updated
