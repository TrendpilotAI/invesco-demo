# 351 — Add slowapi Rate Limiting

**Repo:** core-entityextraction
**Priority:** P0 (Security — Critical)
**Effort:** S (~2 hours)
**Dependencies:** None

## Problem
Any valid API key holder can DDoS the entity extraction service with unlimited requests. Regex pattern matching and spaCy inference are CPU-intensive — a single key can starve all other callers.

## Solution
Add `slowapi` middleware with per-API-key rate limits on all extraction endpoints.

## Coding Prompt
```
In /data/workspace/projects/core-entityextraction/:

1. Add slowapi to requirements.txt:
   slowapi>=0.1.9

2. In main.py, add rate limiter setup after imports:
   from slowapi import Limiter, _rate_limit_exceeded_handler
   from slowapi.util import get_remote_address
   from slowapi.errors import RateLimitExceeded

   def get_api_key(request: Request) -> str:
       """Use API key as rate limit identifier, fall back to IP."""
       return request.headers.get("X-API-Key") or get_remote_address(request)

   limiter = Limiter(key_func=get_api_key)
   app.state.limiter = limiter
   app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

3. Add rate limit decorators to extraction endpoints:
   - POST /regex_entity_extraction → @limiter.limit("100/minute")
   - POST /ml_entity_extraction → @limiter.limit("60/minute")  (heavier)
   - POST /spacy_entity_extraction → @limiter.limit("60/minute")
   - POST /batch_regex_entity_extraction → @limiter.limit("30/minute")
   - POST /batch_ml_entity_extraction → @limiter.limit("20/minute")
   - GET/POST /fixed_lists → @limiter.limit("200/minute")

   Example:
   @app.post("/regex_entity_extraction")
   @limiter.limit("100/minute")
   async def regex_entity_extraction(request: Request, body: EntityExtractionRequest, ...):
       ...

4. Make limits configurable via env vars:
   RATE_LIMIT_REGEX = os.environ.get("RATE_LIMIT_REGEX", "100/minute")
   RATE_LIMIT_ML = os.environ.get("RATE_LIMIT_ML", "60/minute")

5. Exempt /health endpoint from rate limiting.

6. Add test in tests/test_api.py:
   async def test_rate_limit_exceeded():
       # Send 101 requests in a loop, assert 429 on the 101st
       for i in range(101):
           resp = await client.post("/regex_entity_extraction", ...)
       assert resp.status_code == 429

7. Update README.md with rate limit documentation.

8. Commit: "feat: add slowapi per-key rate limiting on extraction endpoints"
```

## Dependencies
- None (can be applied to existing main.py directly)

## Acceptance Criteria
- [ ] `slowapi` added to requirements.txt
- [ ] All extraction endpoints decorated with `@limiter.limit(...)`
- [ ] Rate limit returns HTTP 429 with `Retry-After` header
- [ ] `/health` endpoint NOT rate limited
- [ ] Limits configurable via environment variables
- [ ] Test case verifying 429 response on limit breach
- [ ] Docker build succeeds with new dependency
