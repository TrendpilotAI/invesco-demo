# SO-001 — Stripe Payment Integration ✅

**Completed:** 2026-03-13
**Commit:** a4c2c50 (main branch, TrendpilotAI/Second-Opinion)

## What Was Implemented

### Backend: Cloud Functions (`functions/src/stripe/`)

#### `subscription.ts` — Subscription status & usage tracking
- `getSubscription(userId)` — reads from `subscriptions/{userId}` Firestore doc
- `getConsultationUsage(userId)` — reads monthly counter from `users/{userId}/usage/consultations`
- `assertConsultationAllowed(userId)` — throws `FREE_TIER_EXHAUSTED` error if 3 free consultations used
- `incrementConsultationUsage(userId)` — increments monthly counter, auto-resets on new month
- `findUserByStripeCustomer(stripeCustomerId)` — reverse lookup for webhook handler
- `upsertSubscription(userId, data)` — merges subscription record into Firestore

#### `checkout.ts` — Stripe Checkout + Portal Cloud Functions
- `createStripeCheckout` (onCall) — creates Stripe Checkout session for Pro subscription
  - Looks up or creates Stripe customer, stores `stripeCustomerId`
  - Returns `{ url }` for frontend redirect to Stripe-hosted checkout page
- `createStripePortalSession` (onCall) — creates Customer Portal session for subscription management
- `getSubscriptionStatus` (onCall) — returns `{ plan, status, used, limit, isProActive, canConsult }`

#### `webhook.ts` — Stripe Webhook Handler
- `stripeWebhook` (onRequest, POST /stripeWebhook) — handles Stripe events
- Verifies webhook signature using `STRIPE_WEBHOOK_SECRET`
- Events handled:
  - `checkout.session.completed` → activates Pro plan in Firestore
  - `customer.subscription.updated` → syncs status changes
  - `customer.subscription.deleted` → reverts to free plan
  - `invoice.payment_succeeded` → confirms active status + extends period
  - `invoice.payment_failed` → marks subscription as `past_due`

### Analysis Gating
All analysis functions now call `assertConsultationAllowed()` before running:
- `analyzeCase` — gated + increments usage on success
- `runAgenticPipeline` — gated + increments usage on success
- `startOpinionSynthesis` — gated (no usage increment — just starts async task)
- `synthesizeDoctorOpinion` — gated

### Frontend

#### `services/stripeService.ts`
- `getSubscriptionStatus()` — calls `getSubscriptionStatus` Cloud Function
- `redirectToCheckout(successPath, cancelPath)` — creates session + redirects to Stripe
- `redirectToCustomerPortal(returnPath)` — portal redirect
- `isFreeTierExhausted(error)` — detects `FREE_TIER_EXHAUSTED` error code

#### `components/UpgradePrompt.tsx`
- Full-screen modal shown when free tier is exhausted
- Shows plan comparison: Free (3/month) vs Pro ($9.99/mo, unlimited)
- One-click "Upgrade to Pro" button → calls `redirectToCheckout()`
- Shows loading state while redirecting to Stripe
- Features listed: unlimited consultations, FHIR export, priority queue, etc.

#### `hooks/useSubscription.ts`
- `useSubscription()` React hook for subscription state management
- Exposes: `status`, `loading`, `showUpgradePrompt`, `setShowUpgradePrompt`, `handleConsultationError`, `refresh`
- Auto-refreshes after returning from Stripe Checkout (`?upgraded=1` in URL)
- `handleConsultationError(err)` — auto-shows upgrade modal for `FREE_TIER_EXHAUSTED` errors

#### `App.tsx`
- Imports `useSubscription` and `UpgradePrompt`
- Shows upgrade-specific UI (blue, not red) when error message contains "free consultations"
- `UpgradePrompt` modal wired with real subscription status
- Auto-detects upgrade success via `?upgraded=1` query param

### Firestore Schema
```
subscriptions/{userId}
  plan: 'free' | 'pro'
  status: 'active' | 'canceled' | 'past_due' | 'trialing'
  stripeCustomerId: string
  stripeSubscriptionId: string | null
  currentPeriodEnd: Timestamp
  updatedAt: Timestamp

users/{userId}/usage/consultations
  monthKey: 'YYYY-MM'
  count: number
  updatedAt: Timestamp
```

### Firestore Security Rules
- `subscriptions/{userId}` — read by owner, write by Cloud Functions only
- `users/{userId}/usage/{document}` — read by owner, write by Cloud Functions only

## Environment Variables Required
| Variable | Where | Purpose |
|---|---|---|
| `STRIPE_SECRET_KEY` | Firebase Functions secret | Stripe API authentication |
| `STRIPE_WEBHOOK_SECRET` | Firebase Functions secret | Webhook signature verification |
| `STRIPE_PRO_PRICE_ID` | Firebase Functions env | Stripe Price ID for Pro subscription |

## Setup Steps (Post-Deploy)
1. Set secrets in Firebase: `firebase functions:secrets:set STRIPE_SECRET_KEY`
2. Set secrets in Firebase: `firebase functions:secrets:set STRIPE_WEBHOOK_SECRET`
3. Set env var: `firebase functions:config:set stripe.pro_price_id="price_xxx"` (or use secrets)
4. In Stripe Dashboard → Webhooks → Add endpoint: `https://<region>-<project>.cloudfunctions.net/stripeWebhook`
5. Subscribe to events: `checkout.session.completed`, `customer.subscription.*`, `invoice.payment_*`
6. Test with Stripe CLI: `stripe listen --forward-to localhost:5001/...`

## Pricing
- Free tier: 3 consultations/month
- Pro: $9.99/month, unlimited consultations
