# TODO-405: Add CORS Middleware + Sentry + Prometheus

**Repo:** signal-studio-auth  
**Priority:** HIGH  
**Effort:** S (2-3 hours)  
**Dependencies:** None

## Problem
- No CORS configuration → frontend requests blocked in production
- No error tracking → silent failures in production
- No metrics → no visibility into auth performance

## Coding Prompt
```
In /data/workspace/projects/signal-studio-auth/:

1. CORS — add to main app file (create main.py if doesn't exist):
   ```python
   from fastapi.middleware.cors import CORSMiddleware
   
   app.add_middleware(
       CORSMiddleware,
       allow_origins=os.environ.get("CORS_ORIGINS", "http://localhost:3000").split(","),
       allow_credentials=True,
       allow_methods=["GET", "POST", "PUT", "DELETE"],
       allow_headers=["Authorization", "Content-Type"],
   )
   ```

2. Sentry — add to requirements.txt: `sentry-sdk[fastapi]>=1.40.0`
   ```python
   import sentry_sdk
   SENTRY_DSN = os.environ.get("SENTRY_DSN")
   if SENTRY_DSN:
       sentry_sdk.init(dsn=SENTRY_DSN, traces_sample_rate=0.1)
   ```

3. Prometheus — add to requirements.txt: `prometheus-fastapi-instrumentator>=6.0.0`
   ```python
   from prometheus_fastapi_instrumentator import Instrumentator
   Instrumentator().instrument(app).expose(app, endpoint="/metrics")
   ```

4. Add env vars to config/supabase_config.py:
   - CORS_ORIGINS
   - SENTRY_DSN

5. Update MIGRATION_GUIDE.md with new env vars
```

## Acceptance Criteria
- [ ] CORS allows Signal Studio frontend domain
- [ ] Sentry captures exceptions in production (no-op if DSN not set)
- [ ] /metrics endpoint returns Prometheus-format metrics
- [ ] All env vars documented
