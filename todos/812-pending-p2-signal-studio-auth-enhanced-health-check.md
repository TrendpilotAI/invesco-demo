# 812 — Enhanced Health Check (Redis + Supabase Connectivity)

**Repo:** signal-studio-auth  
**Priority:** P2  
**Effort:** S (1 hour)  
**Dependencies:** none

## Acceptance Criteria

- [ ] `GET /health` returns detailed status of Redis and Supabase connectivity
- [ ] Returns 200 if all deps healthy, 503 if any critical dep is down
- [ ] Response includes latency for each dependency check
- [ ] Used by Railway/Fly.io health check probe

## Coding Prompt

```
Update /data/workspace/projects/signal-studio-auth/main.py health endpoint:

import time

@app.get("/health")
async def health(request: Request):
    checks = {}
    overall = "ok"
    
    # Redis check
    t0 = time.monotonic()
    try:
        r = get_redis()
        if r:
            r.ping()
            checks["redis"] = {"status": "ok", "latency_ms": round((time.monotonic() - t0) * 1000, 2)}
        else:
            checks["redis"] = {"status": "unavailable"}
    except Exception as e:
        checks["redis"] = {"status": "error", "error": str(e)}
        overall = "degraded"
    
    # Supabase check (just verify URL is reachable)
    t0 = time.monotonic()
    try:
        async with _http_client(request) as client:
            resp = await client.get(f"{SUPABASE_URL}/auth/v1/health", timeout=2.0)
            checks["supabase"] = {"status": "ok", "latency_ms": round((time.monotonic() - t0) * 1000, 2)}
    except Exception as e:
        checks["supabase"] = {"status": "error", "error": str(e)}
        overall = "degraded"
    
    status_code = 200 if overall == "ok" else 503
    return JSONResponse({"status": overall, "checks": checks}, status_code=status_code)
```
