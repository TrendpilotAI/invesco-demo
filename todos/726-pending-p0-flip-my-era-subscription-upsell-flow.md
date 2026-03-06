# TODO-726: Implement Subscription Upsell Flow

**Repo:** flip-my-era  
**Priority:** P0  
**Effort:** Medium (4-6 hours)  
**Status:** pending

## Description
The pricing strategy (Free → Swiftie Starter $12.99 → Swiftie Deluxe $25 → Opus VIP $49.99) is fully documented in `DOCS/PRICING_PLANS.md` but there is no in-app upgrade path. When free users run out of credits they hit a dead end with no conversion flow.

## Coding Prompt
```
In /data/workspace/projects/flip-my-era/:

1. Create a CreditExhaustionModal component (src/modules/credits/components/CreditExhaustionModal.tsx)
   - Trigger: when credit balance === 0 and user tries to generate
   - Show: current plan, next plan benefits, price, "Upgrade Now" CTA
   - Wire to: /pricing route

2. Update src/modules/credits/hooks/useCredits.ts
   - Add isExhausted boolean
   - Fire modal open event when credits hit 0 during generation attempt

3. Update /pricing page (src/app/pages/PricingPage.tsx or equivalent)
   - Each plan card should have a "Subscribe" button
   - Wire "Subscribe" to Stripe checkout session creation
   - Use existing Stripe integration (check scripts/setup-stripe-products.js for product IDs)
   - Create Supabase edge function: create-checkout-session (if not exists)
     - Accepts: priceId, userId
     - Returns: Stripe checkout URL
     - Redirect user to Stripe hosted checkout

4. Post-payment webhook handler (supabase/functions/stripe-webhook/)
   - On checkout.session.completed: update user's plan in DB, add credits
   - Test with: node test-webhook-retry.js

5. Add success/cancel return URLs to checkout session
   - Success: /dashboard?upgrade=success
   - Cancel: /pricing?cancelled=true
   - Show toast on dashboard for upgrade success
```

## Acceptance Criteria
- [ ] Free user hitting generate with 0 credits sees upsell modal
- [ ] Modal links to pricing page with plan comparison
- [ ] Pricing page has working "Subscribe" buttons for each paid tier
- [ ] Stripe checkout completes and webhook upgrades user plan
- [ ] User credits are replenished after successful subscription
- [ ] E2E test covers: exhaust credits → upsell modal → pricing → checkout redirect

## Dependencies
- TODO-015 (wire-subscription-tiers-stripe) — may overlap, check status first
