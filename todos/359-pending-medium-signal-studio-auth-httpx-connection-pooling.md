# TODO 359 — Fix httpx AsyncClient Connection Pooling
**Repo:** signal-studio-auth
**Priority:** MEDIUM
**Effort:** 1 hour
**Status:** pending

## Description
Every auth route creates a new `httpx.AsyncClient()` per request, destroying/recreating
connection pools on every call. Under load this causes latency spikes and connection exhaustion.

## Coding Prompt
In `/data/workspace/projects/signal-studio-auth/routes/auth_routes.py`:

1. Replace per-request clients with a module-level lifespan-managed client:

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
import httpx

# Module-level client (set during lifespan)
_http_client: httpx.AsyncClient | None = None

def get_http_client() -> httpx.AsyncClient:
    if _http_client is None:
        raise RuntimeError("HTTP client not initialized. Use lifespan.")
    return _http_client

@asynccontextmanager
async def lifespan(app: FastAPI):
    global _http_client
    _http_client = httpx.AsyncClient(
        timeout=httpx.Timeout(10.0, connect=5.0),
        limits=httpx.Limits(max_connections=100, max_keepalive_connections=20),
    )
    yield
    await _http_client.aclose()
    _http_client = None
```

2. Update all route handlers to use `get_http_client()`:
```python
@router.post("/login")
async def login(body: LoginRequest):
    client = get_http_client()
    resp = await client.post(
        f"{SUPABASE_URL}/auth/v1/token?grant_type=password",
        headers=_supabase_headers(),
        json={"email": body.email, "password": body.password},
    )
    ...
```

3. Remove all `async with httpx.AsyncClient() as client:` blocks from route handlers.

## Acceptance Criteria
- [ ] Single shared AsyncClient with connection pooling
- [ ] Client initialized during FastAPI lifespan startup
- [ ] Client gracefully closed on shutdown
- [ ] All routes use shared client
- [ ] Existing tests updated to mock the shared client
