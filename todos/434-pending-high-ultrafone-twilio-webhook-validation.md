# 434 — Add Twilio Webhook Signature Validation

**Priority:** HIGH  
**Repo:** Ultrafone  
**Effort:** S (2-4 hours)  

## Description

Twilio webhook endpoints in Ultrafone's FastAPI backend do not validate the `X-Twilio-Signature` header. Without this, any attacker can POST fake call events to the webhook URL and trigger AI receptionist flows, incurring costs and potentially exposing data.

## Coding Prompt

```python
# In backend/main.py or a middleware, add Twilio request validation

from twilio.request_validator import RequestValidator
from fastapi import Request, HTTPException

validator = RequestValidator(settings.TWILIO_AUTH_TOKEN)

async def validate_twilio_request(request: Request):
    signature = request.headers.get("X-Twilio-Signature", "")
    url = str(request.url)
    form = await request.form()
    params = dict(form)
    
    if not validator.validate(url, params, signature):
        raise HTTPException(status_code=403, detail="Invalid Twilio signature")

# Apply as dependency to all Twilio routes:
@app.post("/twilio/voice", dependencies=[Depends(validate_twilio_request)])
async def twilio_voice_webhook(request: Request): ...
```

## Files to Modify
- `backend/main.py` — add validator dependency to all `/twilio/*` routes
- `backend/config/settings.py` — ensure `TWILIO_AUTH_TOKEN` is in settings

## Acceptance Criteria
- [ ] All Twilio webhook routes validate `X-Twilio-Signature`
- [ ] Invalid signatures return 403
- [ ] Unit test verifies validation rejects tampered requests
- [ ] `TWILIO_AUTH_TOKEN` is read from env, never hardcoded
