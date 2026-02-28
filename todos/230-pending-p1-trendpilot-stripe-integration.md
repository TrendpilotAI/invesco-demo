# TODO: Trendpilot — Stripe Payment Integration

**Priority:** P1 — Revenue unlock  
**Repo:** /data/workspace/projects/Trendpilot/  
**Effort:** 3-4 days  
**Dependencies:** Supabase migration done, Stripe account with products created

## Description
Trendpilot has pricing tier logic in code (src/services/pricing/index.ts) but zero payment processing. Without Stripe, there's no way to monetize. Add Stripe Checkout + webhooks + subscription management.

## Coding Prompt (Autonomous Execution)
```
In /data/workspace/projects/Trendpilot/:

1. Install: npm install stripe

2. Create Stripe products/prices (document in STRIPE_SETUP.md):
   - Starter: $29/mo — 1 newsletter, 500 subscribers
   - Growth: $79/mo — 5 newsletters, 5000 subscribers  
   - Pro: $199/mo — unlimited, white-label

3. Create src/services/billing/stripe.ts:
   - createCheckoutSession(tenantId, priceId) → Stripe Checkout URL
   - createPortalSession(tenantId) → Stripe Customer Portal URL
   - handleWebhook(payload, signature) → process events

4. Add webhook handler in src/api/index.ts:
   - POST /api/billing/webhook (raw body parser for Stripe)
   - Events to handle: checkout.session.completed, customer.subscription.updated, customer.subscription.deleted

5. Add routes:
   - POST /api/billing/checkout — create checkout session
   - POST /api/billing/portal — create portal session
   - GET /api/billing/subscription — get current subscription status

6. Update Supabase tenants table with: stripe_customer_id, stripe_subscription_id, plan_tier, plan_status

7. Enforce plan limits in API:
   - Check subscriber count against plan limit before adding
   - Check newsletter count against plan limit before creating
   - Return 402 Payment Required with upgrade URL if over limit

8. Add STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET to .env.example

Tests in tests/billing/:
- stripe.test.ts (mock Stripe SDK)
- webhooks.test.ts
```

## Acceptance Criteria
- [ ] Can complete checkout flow end-to-end (test mode)
- [ ] Subscription status reflected in DB within 5s of webhook
- [ ] Plan limits enforced at API level
- [ ] Customer portal accessible for subscription management
- [ ] Cancellation handled gracefully (downgrade to free tier)
