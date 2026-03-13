# TODO: Implement Twilio Webhook Signature Validation and Rate Limiting

## Priority: P0
## Repo: Ultrafone

### Problem
Twilio webhook endpoints accept any POST request without validating the X-Twilio-Signature header. This allows attackers to spoof calls, inject fake call data, and potentially amplify costs.

### Action Items
- Implement `twilio.validateRequest()` or use `twilio` SDK's validateExpressRequest middleware on all webhook routes
- Require `TWILIO_AUTH_TOKEN` env var and fail startup if not set
- Add express-rate-limit to `/webhooks/*` routes (max 30 req/min per IP)
- Add test for signature validation rejection
- Document webhook security in README/DEPLOYMENT.md

### Impact
- Closes spoofing attack vector
- Prevents fake call injection
- Prevents cost amplification via webhook flooding
- Required before any public deployment

### References
- AUDIT.md security section
- TODO-434, TODO-878, TODO-879
- Twilio security docs: https://www.twilio.com/docs/usage/webhooks/webhooks-security
