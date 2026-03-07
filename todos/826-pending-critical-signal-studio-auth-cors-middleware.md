# TODO-826: Add CORS Middleware to signal-studio-auth

**Repo:** signal-studio-auth  
**Priority:** P0 (Critical)  
**Effort:** 30 minutes  
**Status:** pending

## Problem
No `CORSMiddleware` is configured. Without it, browser requests from Signal Studio frontend will be blocked by CORS policy. Additionally, without an explicit allowlist, any CORS implementation might be overly permissive.

## Task
Add `CORSMiddleware` to `main.py` with:
- `CORS_ALLOWED_ORIGINS` env var (comma-separated list of allowed origins)
- Default: empty string (deny all cross-origin in production)
- Test: verify preflight OPTIONS requests return correct headers

## Coding Prompt
```python
# In main.py, after imports:
from fastapi.middleware.cors import CORSMiddleware
import os

CORS_ORIGINS = [o.strip() for o in os.environ.get("CORS_ALLOWED_ORIGINS", "").split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "X-Request-ID"],
)
```

## Acceptance Criteria
- [ ] OPTIONS preflight to /auth/login returns 200 with CORS headers when origin is in allowlist
- [ ] Cross-origin request from unlisted origin returns 403
- [ ] `CORS_ALLOWED_ORIGINS` env var is documented in `.env.example`
- [ ] Test in `test_security.py` covers CORS behavior
