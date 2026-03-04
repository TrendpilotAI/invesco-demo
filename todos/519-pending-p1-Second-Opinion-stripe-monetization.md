# TODO 519: Add Stripe Monetization to Second-Opinion
**Repo:** Second-Opinion  
**Priority:** P1 — High Impact  
**Effort:** 1 day  
**Status:** pending

## Description
Second-Opinion is production-deployed with real AI functionality but zero monetization. Adding a Stripe freemium subscription layer unlocks revenue immediately.

## Task
Implement freemium subscription gating:
1. Install Firebase Stripe extension (`stripe/firestore-stripe-payments`)
2. Create price tiers: Free (1 case/mo), Pro ($9.99 → 5 cases), Unlimited ($29.99)
3. Add `subscription` field to Firestore user document
4. Gate `runAgenticPipeline` Cloud Function by subscription tier
5. Show paywall modal in `AgenticPipeline.tsx` when user hits limit
6. Add Stripe Customer Portal link in user profile/settings

## Coding Prompt
```
In /data/workspace/projects/Second-Opinion/:

1. Add @stripe/stripe-js to package.json dependencies
2. Create services/stripeService.ts:
   - checkSubscriptionStatus(userId) → { tier, casesUsed, casesLimit }
   - createCheckoutSession(priceId) → redirect URL
   - openCustomerPortal() → portal URL
3. Create components/PaywallModal.tsx - shown when case limit hit
4. Modify functions/src/pipeline.ts: check Firestore user.subscription.tier before processing
5. Add Firebase Stripe extension webhook handler
6. Create /data/workspace/projects/Second-Opinion/STRIPE_SETUP.md with setup instructions
```

## Acceptance Criteria
- [ ] Users can subscribe via Stripe Checkout
- [ ] Free tier: 1 case/month enforced
- [ ] Pro tier: 5 cases/month enforced  
- [ ] Paywall modal appears gracefully at limit
- [ ] Customer portal for subscription management
- [ ] Webhook updates Firestore in real-time

## Dependencies
None — can start immediately
