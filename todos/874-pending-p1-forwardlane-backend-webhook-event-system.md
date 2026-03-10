# FL-012: Webhook Event System

**Repo:** forwardlane-backend  
**Priority:** P1  
**Effort:** L (5-7 days)  
**Status:** pending

## Task Description
Build a full webhook event system allowing tenants to receive real-time push notifications when rankings update, recommendations are ready, pipeline runs complete, or reports are generated. HMAC-SHA256 signed payloads dispatched via Celery with exponential backoff retry.

## Problem
Invesco and other enterprise clients need to integrate ForwardLane data into their own workflows (dashboards, reporting systems, internal tools). Without webhooks, they must poll our API, which is inefficient and unscalable. This is a standard enterprise integration requirement.

## Coding Prompt
```
Create a new Django app: webhooks/

1. webhooks/models.py:
```python
import secrets
from django.db import models
from core.models import BaseModel

class WebhookEndpoint(BaseModel):
    EVENT_CHOICES = [
        ('ranking.updated', 'Ranking Updated'),
        ('recommendation.ready', 'Recommendation Ready'),
        ('pipeline.completed', 'Pipeline Completed'),
        ('report.ready', 'Report Ready'),
    ]
    tenant = models.ForeignKey('customers.Tenant', on_delete=models.CASCADE)
    url = models.URLField(max_length=500)
    events = models.JSONField(default=list)  # List of event types to subscribe to
    secret = models.CharField(max_length=64, default=secrets.token_hex)
    is_active = models.BooleanField(default=True)
    description = models.CharField(max_length=200, blank=True)
    
    class Meta:
        db_table = 'webhooks_endpoint'

class WebhookDelivery(BaseModel):
    STATUS_CHOICES = [('pending', 'Pending'), ('success', 'Success'), ('failed', 'Failed')]
    endpoint = models.ForeignKey(WebhookEndpoint, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=100)
    payload = models.JSONField()
    status = models.CharField(max_length=20, default='pending')
    response_status_code = models.IntegerField(null=True)
    response_body = models.TextField(blank=True)
    attempt_count = models.IntegerField(default=0)
    delivered_at = models.DateTimeField(null=True)
```

2. webhooks/dispatcher.py:
```python
import hashlib, hmac, json
import requests
from django.utils import timezone

def sign_payload(payload: dict, secret: str) -> str:
    body = json.dumps(payload, sort_keys=True).encode()
    return hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()

def dispatch_webhook(endpoint_id: int, event_type: str, payload: dict):
    """Dispatch webhook — called from Celery task"""
    from webhooks.models import WebhookEndpoint, WebhookDelivery
    endpoint = WebhookEndpoint.objects.get(id=endpoint_id, is_active=True)
    
    if event_type not in endpoint.events:
        return  # Not subscribed to this event
    
    signature = sign_payload(payload, endpoint.secret)
    headers = {
        'Content-Type': 'application/json',
        'X-ForwardLane-Signature': f'sha256={signature}',
        'X-ForwardLane-Event': event_type,
    }
    
    delivery = WebhookDelivery.objects.create(
        endpoint=endpoint, event_type=event_type, payload=payload
    )
    
    try:
        response = requests.post(endpoint.url, json=payload, headers=headers, timeout=10)
        delivery.status = 'success' if response.ok else 'failed'
        delivery.response_status_code = response.status_code
        delivery.response_body = response.text[:1000]
        delivery.delivered_at = timezone.now()
    except requests.RequestException as e:
        delivery.status = 'failed'
        delivery.response_body = str(e)
    finally:
        delivery.attempt_count += 1
        delivery.save()
    
    return delivery.status == 'success'
```

3. webhooks/tasks.py:
```python
from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@shared_task(bind=True, max_retries=5)
def dispatch_webhook_task(self, endpoint_id: int, event_type: str, payload: dict):
    from webhooks.dispatcher import dispatch_webhook
    try:
        success = dispatch_webhook(endpoint_id, event_type, payload)
        if not success:
            raise Exception(f'Webhook delivery failed for endpoint {endpoint_id}')
    except Exception as exc:
        countdown = 2 ** self.request.retries * 60  # 1min, 2min, 4min, 8min, 16min
        raise self.retry(exc=exc, countdown=countdown)

def emit_event(event_type: str, tenant_id: int, payload: dict):
    """Call this from business logic to fire webhook events"""
    from webhooks.models import WebhookEndpoint
    endpoints = WebhookEndpoint.objects.filter(
        tenant_id=tenant_id, is_active=True, events__contains=[event_type]
    )
    for endpoint in endpoints:
        dispatch_webhook_task.delay(endpoint.id, event_type, payload)
```

4. webhooks/views.py — CRUD for webhook config:
- GET/POST /api/v1/webhooks/ — list/create endpoints
- GET/PUT/DELETE /api/v1/webhooks/{id}/ — manage endpoint
- POST /api/v1/webhooks/{id}/test/ — send test event
- GET /api/v1/webhooks/{id}/deliveries/ — delivery history

5. Wire into business logic:
- In client_ranking/tasks.py after ranking update: emit_event('ranking.updated', ...)
- In pipeline_engine after completion: emit_event('pipeline.completed', ...)

6. webhooks/tests/test_dispatcher.py:
- Test HMAC signature generation
- Test delivery creation and status update
- Test retry logic on failed delivery
- Test emit_event fans out to all subscribed endpoints

Files to create:
- webhooks/__init__.py, apps.py, models.py, views.py, serializers.py, urls.py, tasks.py, dispatcher.py, admin.py
- webhooks/tests/ (test files)
- webhooks/migrations/ (initial migration)
- Update forwardlane/urls.py to include webhooks.urls
- Update INSTALLED_APPS in settings
```

## Acceptance Criteria
- [ ] WebhookEndpoint model with tenant scoping
- [ ] HMAC-SHA256 signed payloads
- [ ] Celery task with exponential backoff retry (5 attempts)
- [ ] CRUD API endpoints for webhook management
- [ ] Test endpoint triggers a real delivery
- [ ] Delivery history logged in WebhookDelivery table
- [ ] `ranking.updated` event fired from client_ranking
- [ ] Tests cover dispatcher, signature, retry logic

## Dependencies
- FL-030 (Celery queue routing) — webhook tasks should use `default` queue.
- FL-034 (API audit logging) — webhook API calls will be audit-logged automatically.
