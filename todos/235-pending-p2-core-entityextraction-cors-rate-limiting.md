# 235 — Add CORS Configuration and Rate Limiting

**Repo:** core-entityextraction  
**Priority:** P2 (Security)  
**Effort:** 2 hours  
**Dependencies:** None

## Description
FastAPI app has no CORS config (defaults allow all origins) and no rate limiting on extraction endpoints.

## Coding Prompt
```
In /data/workspace/projects/core-entityextraction/main.py:

1. Add CORS middleware:
   from fastapi.middleware.cors import CORSMiddleware
   
   ALLOWED_ORIGINS = os.environ.get("CORS_ORIGINS", "").split(",")
   if not ALLOWED_ORIGINS or ALLOWED_ORIGINS == [""]:
       ALLOWED_ORIGINS = ["*"]  # Dev mode
   
   app.add_middleware(
       CORSMiddleware,
       allow_origins=ALLOWED_ORIGINS,
       allow_credentials=True,
       allow_methods=["GET", "POST", "DELETE"],
       allow_headers=["X-API-Key", "Content-Type"],
   )

2. Add rate limiting with slowapi:
   pip install slowapi
   Add to requirements.txt: slowapi>=0.1.9
   
   from slowapi import Limiter, _rate_limit_exceeded_handler
   from slowapi.util import get_remote_address
   from slowapi.errors import RateLimitExceeded
   
   limiter = Limiter(key_func=get_remote_address)
   app.state.limiter = limiter
   app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
   
   Apply to extraction endpoints:
   @app.post("/regex_entity_extraction")
   @limiter.limit("60/minute")
   async def regex_entity_extraction(request: Request, req: EntityExtractionRequest):
       ...
   
   (Similar for ml_ and spacy_ endpoints)

3. Add CORS_ORIGINS to .env.example:
   CORS_ORIGINS=https://app.forwardlane.com,https://staging.forwardlane.com
```

## Acceptance Criteria
- [ ] CORS_ORIGINS env var controls allowed origins
- [ ] Extraction endpoints rate-limited to 60 req/min per IP
- [ ] Rate limit exceeded returns 429 with Retry-After header
- [ ] /health endpoint exempt from rate limiting
