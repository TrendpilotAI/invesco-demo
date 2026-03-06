# 810 — Add X-Request-ID Middleware

**Repo:** signal-studio-auth  
**Priority:** P2  
**Effort:** S (1 hour)  
**Dependencies:** none

## Acceptance Criteria

- [ ] Every request gets a UUID request ID (from `X-Request-ID` header or generated)
- [ ] Request ID is attached to all log lines for that request
- [ ] Request ID is echoed back in response headers
- [ ] Works with existing structured logging

## Coding Prompt

```
Create /data/workspace/projects/signal-studio-auth/middleware/request_id.py:

import uuid
import logging
from fastapi import Request

logger = logging.getLogger(__name__)

async def request_id_middleware(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    request.state.request_id = request_id
    
    # Add to log context (use logging extras or contextvars)
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response

Add to main.py:
app.middleware("http")(request_id_middleware)

Update all logger calls to include request_id:
logger.info("...", extra={"request_id": request.state.request_id})
```
