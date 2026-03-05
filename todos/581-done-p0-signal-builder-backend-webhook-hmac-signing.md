# TODO-581: Webhook HMAC-SHA256 Payload Signing

**Priority:** P0 (Critical Security)
**Repo:** signal-builder-backend
**Effort:** S (2-4 hours)
**Status:** Pending

## Problem
Webhook payloads are delivered without cryptographic signatures. Enterprise clients cannot verify that webhooks originate from signal-builder-backend (replay attacks, spoofing possible).

## Task
1. When a webhook is registered, generate and store a webhook secret (UUID or random 32 bytes)
2. On delivery, compute HMAC-SHA256 of the payload using the secret
3. Include signature in `X-Webhook-Signature: sha256=<hex>` header
4. Document the verification process in API docs
5. Add tests for signature generation and delivery

## Coding Prompt
```
In /data/workspace/projects/signal-builder-backend/:

1. Check apps/webhooks/models/webhook.py — add `secret` field (auto-generated UUID on creation)
2. Create Alembic migration to add secret column to webhooks table
3. In apps/webhooks/cases/webhook.py (delivery logic), before HTTP delivery:
   import hmac, hashlib
   payload_bytes = json.dumps(payload).encode()
   sig = hmac.new(secret.encode(), payload_bytes, hashlib.sha256).hexdigest()
   headers["X-Webhook-Signature"] = f"sha256={sig}"
4. Expose webhook secret in the webhook creation response (show once, like API keys)
5. Add unit test in tests/webhooks/ for signature computation
6. Add to OpenAPI docs: webhook verification instructions
```

## Acceptance Criteria
- [ ] All webhook deliveries include `X-Webhook-Signature` header
- [ ] Signature is HMAC-SHA256 of JSON payload using per-webhook secret
- [ ] Secret is returned once on webhook creation
- [ ] Unit tests for signature computation pass
- [ ] API docs explain verification steps
