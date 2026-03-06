# TODO-586: Webhook Delivery Retry System with Exponential Backoff + Dead Letter Queue

**Repo:** signal-builder-backend
**Priority:** P1 (High)
**Effort:** M (Medium, ~4-6h)
**Status:** pending
**Created:** 2026-03-06

## Description

Webhook delivery was added (HMAC signing in TODO-581), but there is no retry mechanism. When a downstream system is unavailable, webhook events are silently lost. Enterprise clients require reliable webhook delivery.

## Acceptance Criteria

- [ ] Failed webhook deliveries retry with exponential backoff (1s, 2s, 4s, 8s, 16s, max 5 attempts)
- [ ] After max retries, event moves to a dead-letter queue (Redis key or DB table)
- [ ] Dead-letter entries are queryable via admin or API
- [ ] Retry logic is idempotent — uses the existing Celery dedup guard (TODO-397)
- [ ] Tests cover: success on retry 2, exhaust retries → DLQ, DLQ queryable

## Coding Prompt

```
In /data/workspace/projects/signal-builder-backend/:

1. In apps/webhooks/tasks.py (create if not exists), add a Celery task:
   @celery_app.task(bind=True, max_retries=5)
   def deliver_webhook(self, webhook_id: int, payload: dict):
       try:
           # fetch webhook endpoint from DB
           # POST with HMAC-SHA256 header (use existing webhook_signer)
           # on 2xx: mark delivery as success
           # on 4xx: do NOT retry (bad endpoint config)
           # on 5xx/timeout: raise self.retry(countdown=2**self.request.retries)
       except MaxRetriesExceededError:
           # write to dead letter queue: Redis key "webhook:dlq" or DB table webhook_dlq
           pass

2. Add webhook_dlq table to db/orm.py:
   class WebhookDeadLetter(Base):
       id, webhook_id, payload (JSON), failed_at, reason, attempt_count

3. Add Alembic migration for webhook_dlq table

4. Add GET /v1/webhooks/{id}/dead-letters endpoint to apps/webhooks/routers_v1.py

5. Write tests in tests/test_webhook_retry.py:
   - Mock HTTP 500 → verify retry scheduling
   - Mock 5 consecutive failures → verify DLQ entry created
   - Mock success on attempt 3 → verify no DLQ entry
```

## Dependencies
- TODO-397 (Celery dedup) should be done first for idempotency
- TODO-581 (HMAC signing) — DONE ✅

## Risk
- Medium: Celery retry + DB writes can create duplicate DLQ entries without idempotency guard
