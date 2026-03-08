# TODO #841 — Second-Opinion: Stripe Monetization Integration

**Priority:** P0  
**Effort:** L (1 week)  
**Repo:** /data/workspace/projects/Second-Opinion/  
**Created:** 2026-03-08 by Judge Agent v2

## Task Description

Add Stripe payment integration to unlock revenue from Second-Opinion's existing user base. No monetization currently exists despite a deployed production app with users.

## Implementation

### Setup
```bash
# Install Firebase Stripe Extension
firebase ext:install stripe/firestore-stripe-payments

# Add Stripe deps to functions
cd functions && npm install stripe
```

### Pricing Tiers
- **Free:** 2 analyses/month, basic report
- **Pro ($19/month):** Unlimited analyses, PDF export, full history, priority AI models
- **Clinic ($199/month):** White-label, multi-user, API access, FHIR export

### Code Changes
1. Add `/pricing` route in App.tsx with new PricingPage component
2. Create `services/stripeService.ts` — checkout session creation, subscription status
3. Update `functions/src/` — usage gate middleware per tier limits
4. Add subscription status to user profile in Firestore
5. Gate analysis count in `useAnalysisPipeline.ts` based on tier

### Acceptance Criteria
- [ ] Pricing page live at /pricing with all 3 tiers shown
- [ ] Stripe checkout flow works end-to-end (test mode)
- [ ] Free tier limits enforced (2 analyses/month counter in Firestore)
- [ ] Pro users bypass limit
- [ ] Subscription management portal linked (Stripe Customer Portal)
- [ ] Webhook handler for subscription.created/cancelled events

## Dependencies
- None (can start immediately)

## Risk
- HIPAA: Stripe is HIPAA-eligible with BAA — must sign BAA before processing any PHI in payment context
