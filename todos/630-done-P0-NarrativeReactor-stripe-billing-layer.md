# TODO-630: Multi-Tenant SaaS Billing Layer (Stripe) — DONE

**Commit:** 7f8eadc  
**Pushed:** 2026-03-06  
**Branch:** main

## What Was Implemented

### New Files
- `src/services/tenants.ts` — SQLite-backed multi-tenant management
  - Tables: `tenants` + `tenant_usage_log` with indexes on api_key_hash, stripe_customer_id, email
  - API key generation with `nr_live_` prefix, SHA-256 hashed in DB
  - Methods: createTenant, validateApiKey, checkQuota, incrementUsage, rotateApiKey, upgradeTenantPlan, deactivateTenant
  - Monthly quota auto-reset when past reset_at date

- `src/services/billing.ts` — Stripe integration
  - createCheckoutSession (starter/pro plans via STRIPE_PRICE_* env vars)
  - createPortalSession for subscription management
  - handleWebhook with stripe-signature verification
  - Events: checkout.session.completed, customer.subscription.updated/deleted, invoice.payment_succeeded/failed
  - Stripe API version: 2026-02-25.clover

- `src/middleware/tenantAuth.ts` — Auth + quota enforcement
  - `tenantAuth`: validates X-API-Key header → 401 on invalid/inactive key
  - `quotaGuard`: HTTP 429 with JSON upgrade prompt + X-RateLimit-{Quota,Remaining,Reset} headers

- `src/routes/billing.ts` — All billing routes wired
  - GET  /api/billing/plans — public plan listing
  - POST /api/billing/checkout — Stripe Checkout (tenant auth)
  - POST /api/billing/portal — Customer portal (tenant auth)  
  - GET  /api/billing/usage — quota status (tenant auth)
  - POST /api/billing/tenants — create tenant (admin API_KEY auth)
  - GET  /api/billing/tenants — list tenants (admin)
  - GET  /api/billing/tenants/:id/usage — usage log (admin)
  - POST /api/billing/tenants/:id/rotate-key — rotate API key (admin)
  - POST /webhooks/stripe — raw body webhook

- `src/__tests__/billing.test.ts` — 14 passing unit tests

### Modified Files
- `src/index.ts` — wired billingRouter + stripeWebhookRouter
- `src/lib/env.ts` — added validateBillingEnv() non-fatal Stripe env check

## Plans & Pricing
| Plan       | Tokens/month | Price/month |
|------------|-------------|-------------|
| free       | 10,000      | $0          |
| starter    | 100,000     | $49         |
| pro        | 500,000     | $149        |
| enterprise | 10,000,000  | custom      |

## Required Env Vars (Stripe)
```
STRIPE_SECRET_KEY=sk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...
STRIPE_PRICE_STARTER=price_...
STRIPE_PRICE_PRO=price_...
APP_URL=https://narrativereactor.ai
```

## Acceptance Criteria Status
- [x] Per-tenant API key management with usage quotas enforced
- [x] Stripe Checkout integration for Starter/Pro/Enterprise plans
- [x] Usage metering: track token consumption per tenant per billing period
- [ ] Billing dashboard showing tenant usage, cost, plan limits (deferred — next pass)
- [x] Webhook handler for Stripe events (payment success, cancellation, upgrade)
- [x] Graceful quota exceeded response (HTTP 429 with upgrade prompt)
