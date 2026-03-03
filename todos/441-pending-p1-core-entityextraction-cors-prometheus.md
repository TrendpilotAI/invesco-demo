# TODO-441: Add CORS middleware + Prometheus metrics endpoint

**Repo:** core-entityextraction  
**Priority:** P1  
**Effort:** S (2-3h)  
**Status:** pending

## Problem
1. No CORS headers — API unusable from browser clients
2. No metrics endpoint — zero production observability

## Task
Add both CORSMiddleware and Prometheus metrics in one shot (small changes).

## Coding Prompt
```
In /data/workspace/projects/core-entityextraction/main.py:

### CORS
1. Add: from fastapi.middleware.cors import CORSMiddleware
2. Add env var: ALLOWED_ORIGINS (comma-separated, default "*" for dev)
3. Add middleware:
   app.add_middleware(
       CORSMiddleware,
       allow_origins=os.environ.get("ALLOWED_ORIGINS", "*").split(","),
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )

### Prometheus  
1. Add to requirements.txt: prometheus-fastapi-instrumentator>=6.1.0
2. Add to main.py:
   from prometheus_fastapi_instrumentator import Instrumentator
   Instrumentator().instrument(app).expose(app)
3. This auto-exposes /metrics endpoint with:
   - http_requests_total (by endpoint, method, status)
   - http_request_duration_seconds (p50/p95/p99)
4. Add custom metric: entity_store_size gauge
   from prometheus_client import Gauge
   ENTITY_STORE_SIZE = Gauge("entity_store_size", "Total entities in store")
   # Update in startup and after entity mutations
```

## Acceptance Criteria
- [ ] CORS headers present on all responses (test with curl -H "Origin: http://test.com")
- [ ] /metrics returns Prometheus text format
- [ ] entity_store_size gauge shows correct count
- [ ] No performance regression on extraction endpoints
