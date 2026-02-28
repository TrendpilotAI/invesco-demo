# Add Signal Webhooks / Event System

**Repo:** signal-builder-backend  
**Priority:** medium  
**Effort:** M (3-5 days)  
**Phase:** 4

## Problem
No way for external systems to subscribe to signal events. Clients/integrations must poll for results.

## Task
1. Create `WebhookSubscription` model (signal_id, url, events, secret)
2. Add webhook CRUD endpoints under `/signals/{id}/webhooks/`
3. Create Celery task to deliver webhook payload with HMAC signature
4. Emit events: `signal.created`, `signal.updated`, `signal.executed`, `signal.failed`
5. Add retry logic with exponential backoff for failed deliveries
6. Add webhook delivery log for debugging

## Acceptance Criteria
- Users can subscribe webhooks to specific signal events
- Webhook delivery includes HMAC-SHA256 signature for verification
- Failed deliveries retry up to 5 times with backoff
- Delivery history queryable via API
- Docs updated with webhook integration guide
