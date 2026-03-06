# 801 — Add CORS Middleware

**Repo:** signal-studio-auth  
**Priority:** P0 (security)  
**Effort:** S (30 mins)  
**Dependencies:** none

## Problem

FastAPI app in `main.py` has no CORS configuration. Any origin can call auth endpoints from a browser. Critical security gap before any production deployment.

## Acceptance Criteria

- [ ] `CORSMiddleware` added to FastAPI app
- [ ] `ALLOWED_ORIGINS` env var controls allowed origins
- [ ] Defaults to `localhost:3000,localhost:5173` for local dev
- [ ] `credentials=True` to allow cookies if needed
- [ ] A test verifies CORS headers present on OPTIONS preflight

## Coding Prompt

```
In /data/workspace/projects/signal-studio-auth/main.py:

1. Add CORSMiddleware:

   import os
   from fastapi.middleware.cors import CORSMiddleware
   
   ALLOWED_ORIGINS = os.environ.get(
       "ALLOWED_ORIGINS", 
       "http://localhost:3000,http://localhost:5173"
   ).split(",")
   
   app.add_middleware(
       CORSMiddleware,
       allow_origins=ALLOWED_ORIGINS,
       allow_credentials=True,
       allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
       allow_headers=["Authorization", "Content-Type", "X-Request-ID"],
   )

2. Add ALLOWED_ORIGINS to .env.example (or create one if it doesn't exist).

3. Add a test in tests/test_security.py that sends an OPTIONS preflight request 
   to /auth/login and verifies Access-Control-Allow-Origin header is present.
```
