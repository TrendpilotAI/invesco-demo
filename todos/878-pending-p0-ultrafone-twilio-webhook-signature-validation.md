# 878 · CRITICAL: Add Twilio Webhook Signature Validation

**Project:** Ultrafone  
**Priority:** P0 (Critical Security)  
**Status:** completed  
**Effort:** 2h  
**Created:** 2026-03-10

---

## Problem

The Twilio webhook endpoint (`POST /webhook/incoming`) accepts any POST request without validating that it came from Twilio. This means any attacker can:
1. Fake incoming calls (spam your AI receptionist)
2. Trigger Groq/Deepgram/Fish API calls at your expense (cost amplification attack)
3. Inject malicious caller data

## Task

Add Twilio request signature validation to all webhook endpoints in `backend/api/routes/calls.py`.

## Implementation

```python
# backend/api/routes/calls.py
from twilio.request_validator import RequestValidator
from fastapi import Request, HTTPException, Depends
from config.settings import settings

def validate_twilio_signature(request: Request, form_data: dict) -> None:
    """Validates that the request originated from Twilio."""
    validator = RequestValidator(settings.twilio_auth_token)
    signature = request.headers.get("X-Twilio-Signature", "")
    url = str(request.url)
    
    if not validator.validate(url, form_data, signature):
        raise HTTPException(status_code=403, detail="Invalid Twilio signature")

# Add as dependency to webhook routes:
@router.post("/incoming")
async def handle_incoming_call(
    request: Request,
    form_data: FormData = Depends(parse_form),
    _: None = Depends(validate_twilio_signature)
):
    ...
```

Also add to:
- `/webhook/status` (call status callbacks)
- `/webhook/recording` (recording status callbacks)
- Any other Twilio callback endpoints

## Acceptance Criteria
- [ ] `RequestValidator` used on all Twilio webhook endpoints
- [ ] Non-Twilio requests get 403 response
- [ ] Unit test added: `test_twilio_signature_validation()`
- [ ] Works correctly in Railway environment (HTTPS URL matching)
- [ ] Dev environment has bypass flag: `settings.skip_twilio_validation = True` for local testing

## Dependencies
- Depends on: API keys being rotated first (TODO 858)
- Blocks: Nothing (additive hardening)
