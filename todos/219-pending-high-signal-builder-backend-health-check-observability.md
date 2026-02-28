# TODO: Add Health Check + Sentry Observability (signal-builder-backend)

**Priority:** High  
**Repo:** signal-builder-backend  
**Effort:** 3 hours  
**Status:** pending

## Description
No health check endpoint (Railway can't probe the service). No error tracking. Blind to production errors.

## Coding Prompt
```
In /data/workspace/projects/signal-builder-backend:

1. Add health check router in core/internals/get_application.py:
   @app.get("/health")
   async def health_check():
       return {"status": "ok", "version": settings.VERSION}
   
   @app.get("/health/db")
   async def db_health(db: AsyncSession = Depends(get_db)):
       await db.execute(text("SELECT 1"))
       return {"status": "ok", "db": "connected"}

2. Add Sentry integration:
   - Add `sentry-sdk[fastapi]` to Pipfile
   - In core/internals/get_application.py:
     import sentry_sdk
     sentry_sdk.init(dsn=settings.SENTRY_DSN, traces_sample_rate=0.1)
   - Add SENTRY_DSN to settings/common.py (optional, skip if not set)

3. Add to railway.json healthcheckPath: "/health"

4. Add VERSION = os.environ.get("VERSION", "unknown") to settings/common.py
```

## Dependencies
- None

## Acceptance Criteria
- GET /health returns 200 with JSON
- GET /health/db returns 200 when DB connected
- Railway health checks pass
- Sentry captures unhandled exceptions (if SENTRY_DSN configured)
