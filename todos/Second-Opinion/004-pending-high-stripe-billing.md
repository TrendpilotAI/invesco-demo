# TODO-004: HIGH — Complete Stripe Billing Integration

**Priority:** HIGH
**Status:** pending
**Category:** business_value

## Problem
Stripe integration exists (checkout.ts, subscription.ts, webhook.ts) but needs completion for production billing. The $0.02/analysis pricing model is documented but payment flow may not be fully wired.

## Tasks
- Verify webhook handler processes all Stripe events correctly
- Test subscription lifecycle (create → upgrade → cancel → expire)
- Implement usage-based billing metering if applicable
- Add billing UI components for plan management

## Files
- `functions/src/stripe/checkout.ts`
- `functions/src/stripe/subscription.ts`
- `functions/src/stripe/webhook.ts`
- `services/stripeService.ts`
