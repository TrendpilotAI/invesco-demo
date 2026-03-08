# SSA-001 + SSA-002 + SSA-003 — Auth Service Quick Wins

**Completed:** 2026-03-08  
**Commit:** f022411 → pushed to TrendpilotAI/signal-studio-auth master  
**Tests:** 98 passed, 0 failed

---

## SSA-001 — Remove dead `_build_rate_limiter()` ✅

Removed the ~70-LOC `_build_rate_limiter()` function from `routes/auth_routes.py`.  
It was superseded by `_redis_or_memory_check()` but never deleted.

**Side effect:** 5 tests in `test_rate_limit_and_tokens.py` imported `_build_rate_limiter` directly.  
Updated those tests to use `_make_shim_check` (in-memory fallback tests) and  
`_redis_or_memory_check` (Redis path tests) — the actual live implementations.

---

## SSA-002 — Security headers middleware ✅

Added `@app.middleware("http")` to `main.py` setting:

| Header | Value |
|--------|-------|
| `Strict-Transport-Security` | `max-age=31536000; includeSubDomains` |
| `X-Frame-Options` | `DENY` |
| `X-Content-Type-Options` | `nosniff` |
| `Referrer-Policy` | `strict-origin-when-cross-origin` |
| `Content-Security-Policy` | `default-src 'self'` |
| `X-XSS-Protection` | `0` |

---

## SSA-003 — Pin dependency versions ✅

Pinned all `>=` ranges in `requirements.txt` to exact versions from the running environment.  
Added `# pinned 2026-03-08` comment at top.

| Package | Was | Now |
|---------|-----|-----|
| PyJWT | `>=2.8.0` | `==2.11.0` |
| email-validator | `>=2.0.0` | `==2.3.0` |
| fastapi | `>=0.100.0` | `==0.135.1` |
| httpx | `>=0.25.0` | `==0.28.1` |
| limits | `>=3.0.0` | `==5.8.0` |
| pydantic[email] | `>=2.0.0` | `==2.12.5` |
| pytest | `>=7.0.0` | `==9.0.2` |
| redis | `>=4.6.0` | `==7.2.1` |
| uvicorn | `>=0.20.0` | `==0.41.0` |

Also added `pytest-asyncio==1.3.0` and `pytest-cov==7.0.0` (were in env but missing from requirements).

`pip-audit` was not available in the environment — CVE scan skipped.
