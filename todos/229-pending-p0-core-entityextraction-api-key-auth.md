# 229 — Add X-API-Key Authentication Middleware

**Repo:** core-entityextraction  
**Priority:** P0 (Critical — security)  
**Effort:** 2 hours  
**Dependencies:** None

## Description
All endpoints are completely unauthenticated. Anyone with the Railway URL can read/write/delete entity lists. Add X-API-Key header authentication middleware.

## Coding Prompt
```
In /data/workspace/projects/core-entityextraction/main.py:

1. Add to imports: from fastapi import FastAPI, HTTPException, Request, Depends
   from fastapi.security import APIKeyHeader

2. Add API key security:
   API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=False)
   
   def get_api_key(api_key: str = Depends(API_KEY_HEADER)):
       expected = os.environ.get("API_KEY")
       if not expected:
           return  # No API_KEY set = auth disabled (dev mode)
       if api_key != expected:
           raise HTTPException(status_code=401, detail="Invalid or missing API key")

3. Add dependency to all non-health endpoints:
   @app.post("/regex_entity_extraction", dependencies=[Depends(get_api_key)])
   @app.post("/ml_entity_extraction", dependencies=[Depends(get_api_key)])
   @app.post("/spacy_entity_extraction", dependencies=[Depends(get_api_key)])
   @app.post("/fixed_lists", dependencies=[Depends(get_api_key)])
   @app.delete("/fixed_lists", dependencies=[Depends(get_api_key)])
   
   Keep /health and /version unauthenticated (for Railway health checks).

4. Add to .env.example:
   API_KEY=your-secret-key-here

5. Add to Railway service environment variables via railway.json or Railway dashboard.

6. Document in README.md under Configuration section.
```

## Acceptance Criteria
- [ ] Requests without X-API-Key header return 401
- [ ] Requests with wrong API key return 401
- [ ] Requests with correct API key succeed
- [ ] /health and /version remain accessible without auth
- [ ] If API_KEY env var not set, auth is disabled (backward compatible dev mode)
- [ ] API_KEY documented in .env.example and README
