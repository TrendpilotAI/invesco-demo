# 882 · Zapier/Make.com Webhook Bridge for Distribution

**Project:** Ultrafone  
**Priority:** P1 (Revenue Enabler)  
**Status:** pending  
**Effort:** 1 day  
**Created:** 2026-03-10

---

## Problem

Currently Ultrafone can't connect to the 5,000+ apps in Zapier/Make ecosystems. Adding outbound webhooks unlocks HubSpot, Salesforce, Slack, Gmail, Notion, and more without custom integrations — a huge distribution multiplier for a SaaS product.

## Task

Add a configurable outbound webhook system that fires on key Ultrafone events.

## Events to Emit

| Event | Payload | Use Cases |
|-------|---------|-----------|
| `call.classified` | type, from_number, caller_name | Routing, early alerts |
| `call.completed` | transcript, disposition, security_score, duration | CRM entry, Slack summary |
| `lead.created` | company, role, product_interest, contact | HubSpot, Salesforce |
| `appointment.captured` | office, date, appointment_type | Calendar, reminder systems |
| `spam.blocked` | from_number, score, flags | Blocklist sync |

## Implementation

### 1. Webhook Config Model

```python
# backend/models/webhook_config.py
class WebhookConfig(Base):
    __tablename__ = "webhook_configs"
    
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("user_profiles.id"))
    url = Column(String, nullable=False)
    events = Column(JSON, default=["call.completed"])  # subscribe to specific events
    secret = Column(String)  # HMAC signing secret
    active = Column(Boolean, default=True)
```

### 2. Webhook Service

```python
# backend/services/webhook_service.py
import hmac, hashlib, httpx

class WebhookService:
    async def fire(self, user_id: str, event: str, payload: dict):
        configs = await self.db.query(WebhookConfig).filter_by(
            user_id=user_id, active=True
        ).all()
        
        for config in configs:
            if event not in config.events:
                continue
            
            # Sign payload
            body = json.dumps({"event": event, "data": payload})
            sig = hmac.new(config.secret.encode(), body.encode(), hashlib.sha256).hexdigest()
            
            async with httpx.AsyncClient() as client:
                await client.post(
                    config.url,
                    content=body,
                    headers={
                        "Content-Type": "application/json",
                        "X-Ultrafone-Signature": sig,
                        "X-Ultrafone-Event": event,
                    },
                    timeout=5.0
                )
```

### 3. Settings API

```
POST /settings/webhooks — create webhook config
GET  /settings/webhooks — list active webhooks
DELETE /settings/webhooks/{id} — remove webhook
POST /settings/webhooks/{id}/test — send test payload
```

## Acceptance Criteria
- [ ] `WebhookConfig` model and migration
- [ ] `WebhookService.fire()` sends signed POST to registered URLs
- [ ] All 5 event types implemented
- [ ] HMAC signature verification documented in README
- [ ] API endpoints for CRUD on webhook configs
- [ ] Async fire (non-blocking — don't delay call processing)
- [ ] Retry with exponential backoff on 5xx responses
- [ ] Test endpoint to verify webhook is receiving correctly

## Revenue Impact
Zapier has 5,000+ app integrations. This makes Ultrafone plug into any CRM/calendar/notification tool without us building it — **10x distribution** for $1-2 days of work.
