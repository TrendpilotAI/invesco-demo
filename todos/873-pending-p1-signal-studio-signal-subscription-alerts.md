# 873 — Signal Subscription & Alert System

**Repo:** signal-studio  
**Priority:** P1 — Revenue Feature  
**Effort:** 3 weeks  
**Status:** pending

## Problem
Users have no way to get notified when a signal fires or conditions change. This limits the value proposition to "check manually" which reduces engagement and revenue potential.

## Opportunity
- Unlock SaaS subscription model: users pay to subscribe to signal feeds
- Drive daily active usage: push notifications vs passive queries
- Salesforce integration: alerts appear as SFDC tasks/activities

## Architecture

```
Signal Trigger Events
  → lib/services/signal-trigger-service.ts
  → Checks signal conditions against CRM data
  → If triggered: emit to notification queue

Notification Service
  → lib/services/notification-service.ts
  → Email (SendGrid/Resend)
  → Webhook (user-configured URL)
  → Salesforce Task creation

API Routes
  → app/api/signals/subscribe/route.ts (CRUD subscriptions)
  → app/api/signals/[id]/alerts/route.ts (alert history)

UI
  → components/signal-alert-config.tsx (alert setup)
  → app/signals/[id]/page.tsx (signal detail + alerts)
```

## Task
1. Design subscription data model (PostgreSQL)
2. Build alert configuration UI
3. Implement trigger evaluation service
4. Integrate with email (Resend/SendGrid)
5. Add Salesforce task creation via API

## Acceptance Criteria
- [ ] Users can subscribe to a signal with email + webhook options
- [ ] Subscriptions stored in PostgreSQL
- [ ] Email alert sent when signal fires
- [ ] Webhook POST sent with signal payload
- [ ] Alert history viewable in UI
- [ ] Salesforce task created when configured

## Revenue Impact
- Direct path to per-signal subscription pricing
- Reduces churn (habitual daily notifications = stickiness)
- Justifies enterprise pricing tier
