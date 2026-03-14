# TODO: Integrate Stripe Billing + Pricing Tiers

- **Project:** Second-Opinion
- **Priority:** HIGH
- **Status:** pending
- **Category:** Revenue / Monetization
- **Effort:** M (3-5 days)
- **Created:** 2026-03-14

## Description
No monetization in place. Need Stripe for subscription billing with 3 tiers:
- Patient: $29/mo
- Clinic: $299/mo
- Enterprise: $2K+/mo

## Action Items
1. Add `stripe` package
2. Create Products/Prices in Stripe Dashboard
3. Build subscription webhook Cloud Function
4. Add `/pricing` route with tier comparison
5. Add Stripe Customer Portal for self-service management
6. Add usage metering for API access tier
7. Implement waitlist email capture on landing page
