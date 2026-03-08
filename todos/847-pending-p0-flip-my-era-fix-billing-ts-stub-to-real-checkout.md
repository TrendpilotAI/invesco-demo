# TODO-847: Fix billing.ts In-Memory Stub → Real Supabase create-checkout Edge Function

**Priority:** P0 — Blocking Revenue
**Repo:** flip-my-era
**Effort:** M (2 days)
**Created:** 2026-03-08 by Judge Agent v2

## Problem

`src/modules/subscriptions/billing.ts` uses in-memory stores (`const usageStore: UsageRecord[] = []`, `const subscriptionStore = new Map()`) — data is lost on every page refresh. The `create-checkout` Supabase edge function exists but may not be called from the checkout flow.

This means: users cannot successfully purchase subscriptions. **Zero subscription revenue is possible in current state.**

## Task

1. Audit `billing.ts` — identify all functions that write to in-memory stores
2. Replace `usageStore` writes with Supabase `credit_transactions` table inserts
3. Replace `subscriptionStore` reads with `check-subscription` edge function calls
4. Verify `createCheckoutSession()` calls `supabase.functions.invoke('create-checkout', { body: { priceId, successUrl, cancelUrl } })`
5. Verify `CreditExhaustionModal` checkout button triggers real Stripe checkout session
6. Test with Stripe test mode: complete checkout, verify credit grant in DB

## Acceptance Criteria
- [ ] Stripe test checkout completes and redirects to success URL
- [ ] Credits appear in `credit_transactions` table after checkout
- [ ] `subscriptionStore` Map is removed from billing.ts
- [ ] `usageStore` array is removed from billing.ts
- [ ] Vitest tests for billing module pass with mocked edge functions
