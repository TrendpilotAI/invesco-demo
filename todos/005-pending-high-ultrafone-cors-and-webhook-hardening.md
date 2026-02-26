# TODO 005 — Ultrafone: CORS Hardening & Webhook Security

**Status:** pending  
**Priority:** high  
**Project:** Ultrafone  
**Created:** 2026-02-26

---

## Overview

The current backend has `allow_origins=["*"]` in CORS middleware (security risk for production) and no Twilio webhook signature validation (allows fake call injection). This task hardens both before any public deployment.

---

## Coding Prompt

```
You are a security agent for the Ultrafone project at /data/workspace/projects/Ultrafone/

Your task is to harden the API security:

1. Fix CORS configuration in /data/workspace/projects/Ultrafone/backend/main.py:
   - Replace allow_origins=["*"] with environment-based allowed origins
   - Add ALLOWED_ORIGINS env var support (comma-separated list)
   - Default to ["https://ultrafone.up.railway.app", "http://localhost:5173"] if not set
   - Keep allow_credentials=True only for specific origins, not wildcards

2. Add Twilio webhook signature validation:
   - Create /data/workspace/projects/Ultrafone/backend/middleware/twilio_auth.py
   - Use twilio.request_validator.RequestValidator to validate X-Twilio-Signature header
   - Apply to /twilio/voice, /twilio/voice/status, /twilio/recording endpoints
   - Return 403 if signature invalid (or if TWILIO_AUTH_TOKEN not set in dev mode)
   - Add TWILIO_WEBHOOK_VALIDATION_ENABLED=true/false env var for easy dev bypass

3. Add rate limiting to Twilio webhook endpoints:
   - Use slowapi or starlette-ratelimit
   - Limit /twilio/voice to 100 requests/minute per IP
   - Add rate limit headers to responses

4. Harden JWT configuration:
   - Ensure JWT_SECRET is required (not optional) and has minimum 32-char length validation
   - Add JWT expiry validation if not already present

5. Update tests in /data/workspace/projects/Ultrafone/backend/tests/unit/test_auth.py 
   to cover the new validation logic.

6. Document all security changes in /data/workspace/projects/Ultrafone/SECURITY.md
```

---

## Dependencies

- None (can be done in parallel with TODO 004)

---

## Effort

**Estimate:** 4-6 hours  
**Type:** Security / Backend

---

## Acceptance Criteria

- [ ] CORS no longer uses wildcard origin
- [ ] Twilio webhook signature validation implemented and tested
- [ ] Rate limiting applied to webhook endpoints
- [ ] JWT_SECRET length validation added
- [ ] `SECURITY.md` documents all hardening measures
- [ ] All existing tests still pass
