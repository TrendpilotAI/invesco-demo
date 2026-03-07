# TODO-824: Wire Webhook Delivery to Signal Run Completion

**Repo**: signal-builder-backend  
**Priority**: HIGH  
**Effort**: Medium (4-6 hours)

## Context
HMAC signing infrastructure exists (`apps/webhooks/webhook_signer.py`). EventManager exists (`apps/events/`). Need to wire signal execution completion → webhook delivery.

## Task
1. After signal run completes in `apps/signals/cases/signal.py`, emit event via EventManager
2. Event handler queries registered webhook endpoints for the organization
3. Dispatch Celery task: `deliver_webhook(endpoint_url, payload, secret)`
4. Task uses `sign_payload()` from `webhook_signer.py` to create signed envelope
5. POST to endpoint, retry with exponential backoff on failure (use `backoff` lib already in deps)
6. Log each delivery attempt in audit log

## Acceptance Criteria
- Signal completion triggers webhook delivery
- HMAC signature verifiable by receiving endpoint
- Failed deliveries retried up to 3 times with backoff
- Tests: `tests/webhooks/test_webhook_delivery.py`
