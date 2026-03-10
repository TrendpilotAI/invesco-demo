# TODO-831: Remove Duplicate Inline Security Headers Middleware

**Repo:** signal-studio-auth
**Priority:** P1 (High)
**Effort:** 15 minutes
**Status:** pending
**Dependencies:** None (independent)
**Created:** 2026-03-10

## Problem

`main.py` has **two** security header layers that set identical headers on every response:

1. **Line 51:** `app.add_middleware(SecurityHeadersMiddleware)` — the class-based middleware in `middleware/security_headers.py` (SSA-002, commit 790ce14)
2. **Lines 55-64:** `@app.middleware("http") async def security_headers_middleware(...)` — an inline function that sets the same headers with slightly different values

The inline version overwrites the class middleware's values because `@app.middleware("http")` runs **after** `BaseHTTPMiddleware` in FastAPI's ASGI stack. This means:
- CSP is downgraded from `"default-src 'none'; frame-ancestors 'none'; form-action 'self'"` to `"default-src 'self'"` (less restrictive)
- `Permissions-Policy` header set by the class is preserved (inline doesn't touch it)
- `X-XSS-Protection` changes from `"1; mode=block"` to `"0"` (inconsistent)
- HSTS loses `preload` directive

## Files to Change

- `main.py` lines 54-64 — DELETE the entire `@app.middleware("http")` function

## Coding Prompt

```
Open /data/workspace/projects/signal-studio-auth/main.py

Delete the following block (lines 54-64):

@app.middleware("http")
async def security_headers_middleware(request: Request, call_next):
    """SSA-002: Add security headers to every response."""
    response: Response = await call_next(request)
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["X-XSS-Protection"] = "0"
    return response

Also remove the unused imports that become dead after this deletion:
- `Request` from fastapi (KEEP — still used by health endpoint? No, /health doesn't use Request)
- `Response` from fastapi.responses (no longer needed)

Actually: `Request` and `Response` are still imported for the router, so check if they're used elsewhere in main.py. They are NOT used elsewhere in main.py (only in the deleted middleware). Remove them from main.py imports.

Run tests: cd /data/workspace/projects/signal-studio-auth && python -m pytest tests/test_security_headers.py -v
Verify the SecurityHeadersMiddleware class still applies all headers correctly.
```

## Acceptance Criteria

- [ ] Only ONE security headers middleware exists (the class in `middleware/security_headers.py`)
- [ ] `CSP` header is `"default-src 'none'; frame-ancestors 'none'; form-action 'self'"` (the stricter version)
- [ ] `X-XSS-Protection` is `"1; mode=block"` (not `"0"`)
- [ ] HSTS includes `preload` directive
- [ ] `Permissions-Policy` header is present
- [ ] All existing tests pass
- [ ] No unused imports in `main.py`
