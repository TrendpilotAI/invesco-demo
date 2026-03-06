# TODO-630: Multi-Tenant SaaS Billing Layer (Stripe)

**Repo:** NarrativeReactor  
**Priority:** P0  
**Effort:** 5 days  
**Status:** pending

## Description
Implement a multi-tenant billing layer with Stripe subscriptions. This unlocks direct revenue from NarrativeReactor as a SaaS product.

## Acceptance Criteria
- [ ] Per-tenant API key management with usage quotas enforced
- [ ] Stripe Checkout integration for Starter/Pro/Enterprise plans
- [ ] Usage metering: track token consumption per tenant per billing period
- [ ] Billing dashboard showing tenant usage, cost, plan limits
- [ ] Webhook handler for Stripe events (payment success, cancellation, upgrade)
- [ ] Graceful quota exceeded response (HTTP 429 with upgrade prompt)

## Coding Prompt
```
In /data/workspace/projects/NarrativeReactor:

1. Create src/services/tenants.ts — SQLite-backed tenant management
   - Tables: tenants(id, name, plan, stripe_customer_id, api_key_hash, quota_tokens, used_tokens, reset_at)
   - Methods: createTenant, validateApiKey, incrementUsage, checkQuota

2. Create src/services/billing.ts — Stripe integration
   - createCheckoutSession(tenantId, plan) using Stripe Checkout
   - handleWebhook(payload, sig) for stripe-signature verification
   - Plans: starter (100k tokens/$49), pro (500k/$149), enterprise (custom)

3. Add POST /api/billing/checkout and POST /webhooks/stripe routes in src/index.ts

4. Wrap all Genkit flow calls to track token usage via costTracker.ts → tenant usage

5. Add quota guard middleware: check tenant quota before executing any flow

6. Update React dashboard to show usage metrics

Dependencies: stripe npm package, existing costTracker.ts service
```

## Dependencies
- TODO-599 (structured logging) — billing events should be logged
- TODO-600 (SQLite indexes) — tenant table needs indexes on api_key_hash, stripe_customer_id
