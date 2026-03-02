# TODO-400: NarrativeReactor — Stripe Billing Integration

**Priority:** high
**Repo:** NarrativeReactor
**Effort:** L (4-5 days)

## Description
Monetize NarrativeReactor with usage-based Stripe billing. Charge per content generation, video, TTS call.

## Coding Prompt
```
Add Stripe billing to NarrativeReactor at /data/workspace/projects/NarrativeReactor/

1. Add stripe to dependencies
2. Create src/services/billing.ts:
   - createCustomer(tenantId, email)
   - createSubscription(customerId, tier: 'starter'|'pro'|'agency')
   - recordUsage(customerId, quantity, unit: 'content'|'video'|'tts')
   - getUsageSummary(customerId)

3. Wire into costTracker.ts — after each AI call, record to Stripe meter
4. Add billing endpoints:
   - POST /api/billing/subscribe
   - GET /api/billing/usage
   - GET /api/billing/invoices
   - POST /webhooks/stripe (handle payment_failed, subscription_updated)

5. Pricing tiers:
   - Starter: $49/mo, 100 content pieces, 10 videos, 50 TTS
   - Pro: $199/mo, 500 content, 50 videos, unlimited TTS
   - Agency: $499/mo, unlimited all

6. Add STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET to env
```

## Acceptance Criteria
- [ ] Tenant can subscribe to a plan
- [ ] Usage is tracked per API call
- [ ] Stripe webhook handles payment failures
- [ ] Usage dashboard shows current period consumption

## Dependencies
- TODO-397 (multi-tenancy) — billing requires tenant concept
