# TODO 416: Stripe Billing Integration

**Repo:** Ultrafone  
**Priority:** High  
**Effort:** L (3-5 days)  
**Dependencies:** 415 (secrets management)

## Description
Add Stripe billing to enable SaaS monetization. Three tiers: Personal ($9/mo, 1 number), Pro ($29/mo, 3 numbers + voice cloning), Business ($99/mo, multi-user).

## Coding Prompt
```
1. Install stripe Python SDK and React Stripe.js
2. Create Supabase table: subscriptions (user_id, stripe_customer_id, plan, status, period_end)
3. Backend: /api/billing/checkout - create Stripe checkout session
4. Backend: /api/billing/portal - customer portal session
5. Backend: /api/webhooks/stripe - handle subscription.created/updated/deleted events
6. Apply Supabase RLS so users only see their data based on active subscription
7. Gate features: voice cloning gated to Pro+, multi-user to Business+
8. Frontend: Settings > Billing tab with current plan, upgrade/downgrade, invoice history
9. Add STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET to env vars
```

## Acceptance Criteria
- User can subscribe, upgrade, downgrade via Stripe checkout
- Webhook updates subscription status in DB
- Features properly gated by plan
- Billing portal accessible from Settings
