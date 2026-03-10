# 879 · Add Rate Limiting to Twilio Webhook (Cost Protection)

**Project:** Ultrafone  
**Priority:** P0 (Security/Cost)  
**Status:** pending  
**Effort:** 2h  
**Created:** 2026-03-10

---

## Problem

Each POST to the Twilio webhook triggers:
- Groq LLM API call (~$0.001)
- Deepgram STT streaming (~$0.004/min)
- Fish Audio TTS (~$0.002)

Without rate limiting, a flood attack could cost hundreds of dollars in seconds.

## Task

Add `slowapi` rate limiting to webhook endpoints.

## Implementation

```bash
pip install slowapi
```

```python
# backend/main.py
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# backend/api/routes/calls.py
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@router.post("/incoming")
@limiter.limit("10/minute")
async def handle_incoming_call(request: Request, ...):
    ...
```

Also add per-phone-number limiting:
```python
def get_caller_phone(request: Request) -> str:
    """Extract From phone for per-number rate limiting."""
    return request.form.get("From", get_remote_address(request))

@router.post("/incoming")  
@limiter.limit("5/minute", key_func=get_caller_phone)
async def handle_incoming_call(request: Request, ...):
    ...
```

## Acceptance Criteria
- [ ] Max 10 req/min per IP on webhook endpoints
- [ ] Max 5 req/min per caller phone number
- [ ] 429 response returned with `Retry-After` header
- [ ] Rate limit metrics visible in PostHog/Sentry
- [ ] Test: flood test returns 429 after threshold
- [ ] Twilio's own IPs are NOT blocked (Twilio has multiple IPs — use signature validation as primary defense)
