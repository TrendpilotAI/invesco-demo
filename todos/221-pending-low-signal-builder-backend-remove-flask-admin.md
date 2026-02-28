# TODO: Replace Flask Admin with FastAPI-native Admin (signal-builder-backend)

**Priority:** Low  
**Repo:** signal-builder-backend  
**Effort:** 8 hours  
**Status:** pending

## Description
Flask-admin, flask-security-too, flask-sqlalchemy are in a FastAPI project. Two separate frameworks doubles complexity and security surface. Admin runs as separate Gunicorn process.

## Coding Prompt
```
In /data/workspace/projects/signal-builder-backend:

1. Evaluate admin needs — what models/views does the Flask admin expose?
   Run: cat admin.py (or admin/__init__.py)

2. Replace with one of:
   Option A: fastapi-admin (async, FastAPI-native, Tortoise ORM or SQLAlchemy)
   Option B: starlette-admin (SQLAlchemy async compatible)
   Recommended: starlette-admin (best SQLAlchemy 2.0 support)

3. Install: pipenv install starlette-admin
   
4. Mount admin on main FastAPI app at /admin with authentication

5. Migrate all Flask admin views to starlette-admin ModelViews

6. Remove from Pipfile: flask-admin, flask-security-too, flask-sqlalchemy

7. Update docker-compose.yml to remove separate admin service
   Update Railway to remove admin Gunicorn process

8. Update Pipfile scripts: remove `admin` script
```

## Dependencies
- 219-pending-high-signal-builder-backend-upgrade-deps.md

## Acceptance Criteria
- Admin UI accessible at /admin with authentication
- All previous Flask admin models/views replicated
- Flask dependencies removed from Pipfile
- One fewer Railway service to manage
