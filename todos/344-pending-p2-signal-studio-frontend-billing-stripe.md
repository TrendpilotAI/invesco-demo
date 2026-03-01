# TODO-344: Billing / Stripe Integration

**Repo:** signal-studio-frontend  
**Priority:** P2  
**Effort:** M (4-8 hours)  
**Dependencies:** TODO-337, TODO-338

## Description
No billing UI exists. Add plan display, upgrade CTA, and Stripe Customer Portal redirect for plan management.

## Coding Prompt
```
In /data/workspace/projects/signal-studio-frontend/:

1. Create src/app/(app)/settings/billing/page.tsx:
   - Current plan display (free/pro/enterprise from Organization.plan)
   - Feature comparison table
   - Upgrade button → calls POST /billing/portal-session → redirect to Stripe portal
   - For enterprise: "Contact Sales" CTA

2. Create src/lib/api/billing.ts:
   - createPortalSession() → apiClient<{url: string}>('/billing/portal-session', {method:'POST'})
   - getSubscription() → apiClient<{plan, status, renewal_date}>('/billing/subscription')

3. Add billing hooks to hooks.ts:
   - useBillingPortal() mutation
   - useSubscription() query

4. Update settings/page.tsx to include billing tab link

5. Add plan badge to topbar (shows current plan)

6. Gate features by plan:
   - Create src/lib/billing/gates.ts with isPro(), isEnterprise() helpers
   - Show upgrade prompts when free users hit limits
```

## Acceptance Criteria
- [ ] Settings shows current plan
- [ ] Upgrade button redirects to Stripe portal
- [ ] Feature gates prevent free users accessing pro features
- [ ] Plan displayed in topbar
