# TODO 008 — Add /health Endpoint with DB + Redis Probes

**Status:** pending  
**Priority:** high  
**Repo:** signal-builder-backend  
**Effort:** S (2-3 hours)

## Problem

The Railway deployment (`railway.json`, `Dockerfile.railway`) has no health check configured. Railway needs a `/health` endpoint to:
- Verify the service is live (liveness probe)
- Verify dependencies (DB, Redis) are reachable (readiness probe)
- Enable zero-downtime deploys

Without this, Railway can't distinguish a healthy pod from a crashed one.

## Files Affected

- `api.py` (add health router)
- `core/internals/get_application.py` (register health router)
- `railway.json` (add healthcheckPath)
- New file: `core/health.py`

## Coding Prompt

```
You are adding a health check endpoint to signal-builder-backend deployed on Railway.

1. Create /data/workspace/projects/signal-builder-backend/core/health.py:
   - FastAPI router with GET /health endpoint (no auth required)
   - Check DB: run "SELECT 1" against the async PostgreSQL connection
   - Check Redis: ping the Redis connection from settings
   - Return JSON: {"status": "healthy", "db": "ok", "redis": "ok", "version": APP_VERSION}
   - If any check fails, return 503 with {"status": "unhealthy", "db": "error", "redis": "ok", "detail": "..."}
   - Use asyncpg or SQLAlchemy async session for DB check
   - Use redis-py async client for Redis check
   - Keep the endpoint fast (< 500ms timeout on each probe)

2. Register the health router in core/internals/get_application.py — add it before auth middleware so it doesn't require authentication.

3. Update railway.json to add:
   {
     "deploy": {
       "healthcheckPath": "/health",
       "healthcheckTimeout": 10
     }
   }

4. Write a test in tests/ for the health endpoint that mocks DB and Redis connections.

Use the existing settings (DB_HOST, DB_PORT, etc.) and dependency injector patterns from the codebase.
```

## Acceptance Criteria

- [ ] GET /health returns 200 with JSON payload when DB + Redis are reachable
- [ ] GET /health returns 503 when DB is unreachable
- [ ] Endpoint does NOT require authentication (public)
- [ ] railway.json updated with healthcheckPath
- [ ] Test coverage for healthy and unhealthy states

## Dependencies

- TODO 007 (pin deps) recommended first, but not blocking
