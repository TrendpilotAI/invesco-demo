# NR-002 Done — Stripe Metered Billing Reporting

**Completed:** 2026-03-13  
**Priority:** P1/M  
**Commit:** `22fe94d` on `main` (TrendpilotAI/NarrativeReactor)

## What Was Implemented

### New Service: `src/services/meteredBilling.ts`
- **`reportTenantUsageToStripe(tenant, subscriptionItemId, syncType)`**  
  Reports current `used_tokens` to Stripe via `stripe.subscriptionItems.createUsageRecord()` with `action: 'set'` (idempotent re-runs).
  
- **`handleInvoiceUpcoming(invoice)`**  
  Called when Stripe fires `invoice.upcoming`. Looks up the tenant by subscription ID, tallies tokens from `tenant_usage_log` for the invoice period (using `period_start`/`period_end` from the event), and submits a final usage record before Stripe invoices.

- **`syncAllTenantUsageToStripe()`**  
  Batch sync: queries all active paid tenants with a Stripe subscription, gets the metered subscription item ID for each, and reports current usage. Returns `{ synced, skipped, errors, results }`.

- **`initMeteredBillingSchema()`**  
  Creates `metered_billing_sync` table — audit log of every usage report (tenant, subscription item, tokens, Stripe record ID, sync type, period, errors).

### `src/services/billing.ts` changes
- Added `'invoice.upcoming'` to `HANDLED_EVENTS` array.
- Added `invoice.upcoming` case in `handleWebhook()` — calls `handleInvoiceUpcoming()`.

### `src/routes/billing.ts` changes
- Added `POST /api/billing/sync-usage` (admin API key required) — daily cron trigger endpoint.

### `.env.example`
- Added Stripe env var documentation: `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`, `STRIPE_PRICE_STARTER`, `STRIPE_PRICE_PRO`.

### Tests: `src/__tests__/services/meteredBilling.test.ts`
- 10 tests covering:
  - Schema creation
  - `invoice.upcoming` event handling in `handleWebhook()`
  - `reportTenantUsageToStripe()` with real/zero usage
  - `syncAllTenantUsageToStripe()` — filters free tenants, syncs paid
  - `handleInvoiceUpcoming()` — known/unknown/no-subscription cases
- All tests pass ✅

## Stripe API Used
- `stripe.subscriptionItems.createUsageRecord(itemId, { quantity, timestamp, action: 'set' })`
- `stripe.subscriptions.retrieve(subId, { expand: ['items.data.price'] })` — to find metered item ID
