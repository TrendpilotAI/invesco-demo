# TODO-724: Add CORS + security hardening

**Repo:** core-entityextraction  
**Priority:** P1  
**Effort:** 2h  
**Status:** pending

## Description
No CORS middleware configured. API key is re-read from env on every request (perf + security).
Add CORS, cache API keys at startup, add /admin/reload-keys endpoint.

## Acceptance Criteria
- CORSMiddleware restricts to configured allowed origins
- API keys cached at startup, refreshed only on /admin/reload-keys
- ALLOWED_ORIGINS env var configures CORS
- Pre-commit bandit scan passes

## Coding Prompt
```
In /data/workspace/projects/core-entityextraction/main.py:

1. Add CORSMiddleware:
   from fastapi.middleware.cors import CORSMiddleware
   origins = os.environ.get("ALLOWED_ORIGINS", "*").split(",")
   app.add_middleware(CORSMiddleware, allow_origins=origins, allow_methods=["*"], allow_headers=["*"])

2. Cache API keys at startup:
   _valid_keys: Set[str] = set()
   In startup_event: _valid_keys.update(_load_valid_api_keys())
   In middleware: use _valid_keys directly (don't call _load_valid_api_keys() per-request)

3. Add admin reload endpoint (protected by same API key):
   @app.post("/admin/reload-keys")
   def reload_keys(): _valid_keys.clear(); _valid_keys.update(_load_valid_api_keys()); return {"reloaded": len(_valid_keys)}

4. Add ALLOWED_ORIGINS to .env.example with default "http://localhost:3000"
```

## Dependencies
None
