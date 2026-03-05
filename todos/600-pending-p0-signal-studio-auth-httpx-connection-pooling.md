# TODO-600: httpx Connection Pooling via FastAPI Lifespan

**Repo:** signal-studio-auth  
**Priority:** P0 (HIGH)  
**Effort:** 1h  
**Status:** pending

## Problem
Every route handler in `routes/auth_routes.py` creates a new `httpx.AsyncClient` via `async with httpx.AsyncClient() as client:`. This opens a fresh TCP connection to Supabase on every request, adding 10-50ms latency and risking file descriptor exhaustion under load (6 separate `async with` blocks).

## Fix: Module-level AsyncClient with FastAPI Lifespan

```python
# main.py or app factory
from contextlib import asynccontextmanager
import httpx
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.http_client = httpx.AsyncClient(
        timeout=httpx.Timeout(30.0),
        limits=httpx.Limits(max_connections=100, max_keepalive_connections=20),
    )
    yield
    await app.state.http_client.aclose()

app = FastAPI(lifespan=lifespan)
```

Then in `auth_routes.py`, replace every `async with httpx.AsyncClient() as client:` with:
```python
client: httpx.AsyncClient = request.app.state.http_client
response = await client.post(...)
```

## Files to Change
- `routes/auth_routes.py` — remove all 6 `async with httpx.AsyncClient()` blocks
- `main.py` (create if missing) — add lifespan context manager

## Acceptance Criteria
- [ ] Single `AsyncClient` shared across all requests
- [ ] Lifespan properly opens and closes the client
- [ ] All 6 route handlers use `request.app.state.http_client`
- [ ] Test: concurrent requests reuse connections (verify via connection count)
- [ ] No regression in existing test suite

## Dependencies
None
