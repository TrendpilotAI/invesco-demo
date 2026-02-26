---
status: pending
priority: P1
issue_id: "015"
tags: [flip-my-era, stripe, subscriptions, billing, revenue]
dependencies: []
---

# 015 — Wire Subscription Tiers to Real Stripe Products

## Overview

FlipMyEra has detailed subscription tier definitions in `src/modules/subscriptions/tiers.ts` and `src/modules/billing/subscriptionTiers.ts` with four tiers (Debut/Free, Basic/$9.99, Pro/$19.99, Enterprise/$49.99). However, the Stripe Price IDs are placeholders (`price_basic_monthly`, `price_pro_monthly`) read from `VITE_STRIPE_*` env vars — it's unclear if real Stripe products exist and are wired. The `PlanSelector.tsx` page and `UpgradePlan.tsx` exist but may not complete a real checkout flow.

**Why P1:** This is revenue. Subscription tiers should be the primary monetization path. Without working subscription checkout, the app can only sell ad-hoc credits.

## Coding Prompt

You are working on FlipMyEra, a React 18 + TypeScript + Vite + Supabase + Stripe SaaS app at `/data/workspace/projects/flip-my-era/`.

**Task:** Audit and complete the subscription tier checkout flow end-to-end.

### Step 1 — Audit current state

Read these files thoroughly:
1. `src/modules/subscriptions/tiers.ts` — tier definitions and Stripe price ID references
2. `src/modules/billing/subscriptionTiers.ts` — billing tier logic
3. `src/app/pages/PlanSelector.tsx` — the plan selection UI
4. `src/app/pages/UpgradePlan.tsx` — the upgrade flow
5. `supabase/functions/create-checkout/index.ts` — the Stripe checkout session creator
6. `supabase/functions/check-subscription/index.ts` — subscription status checker
7. `supabase/functions/stripe-webhook/index.ts` — Stripe event handler

Document the complete data flow: User selects plan → checkout session created → Stripe checkout → webhook fires → subscription updated in DB → feature gates enforced.

### Step 2 — Identify and fix gaps

Common gaps to look for and fix:

**A. Missing Stripe Price IDs in env vars**
Ensure `.env.example` (or `src/modules/shared/components/EnvironmentValidator.tsx`) documents that these env vars are required:
```
VITE_STRIPE_BASIC_MONTHLY=price_...
VITE_STRIPE_BASIC_ANNUAL=price_...
VITE_STRIPE_PRO_MONTHLY=price_...
VITE_STRIPE_PRO_ANNUAL=price_...
```
Add a runtime warning in the PlanSelector if these are missing.

**B. Stripe webhook handler for subscriptions**
Verify `supabase/functions/stripe-webhook/index.ts` handles:
- `customer.subscription.created`
- `customer.subscription.updated`
- `customer.subscription.deleted`

Each should update a `subscriptions` table or `user_profiles.subscription_tier` column in Supabase. If the webhook handler is missing these events, add them.

**C. Feature gating**
Check `src/modules/shared/components/FeatureGate.tsx` — does it actually check the user's subscription tier? If it's a stub that always returns `true`, implement real tier checking:
```typescript
// Should check user's subscription from Supabase/auth context
const userTier = useSubscriptionTier(); // hook that reads from user profile
const hasAccess = tierHasFeature(userTier, feature);
```

**D. Subscription tier stored in DB**
Check Supabase migrations for a `subscription_tier` or `subscriptions` table. If not present, create a migration:
```sql
-- supabase/migrations/{timestamp}_add_subscription_tier.sql
ALTER TABLE public.user_profiles
  ADD COLUMN IF NOT EXISTS subscription_tier TEXT NOT NULL DEFAULT 'free'
  CHECK (subscription_tier IN ('free', 'basic', 'pro', 'enterprise'));

CREATE INDEX IF NOT EXISTS idx_user_profiles_subscription_tier
  ON public.user_profiles(subscription_tier);
```

### Step 3 — Create subscription tier hook

Create `src/modules/subscriptions/hooks/useSubscriptionTier.ts`:

```typescript
import { useEffect, useState } from 'react';
import { supabase } from '@/core/integrations/supabase/client';
import type { SubscriptionTier } from '../billing';

export function useSubscriptionTier(): {
  tier: SubscriptionTier;
  loading: boolean;
  refresh: () => void;
} {
  const [tier, setTier] = useState<SubscriptionTier>('free');
  const [loading, setLoading] = useState(true);

  const fetchTier = async () => {
    const { data: { user } } = await supabase.auth.getUser();
    if (!user) { setTier('free'); setLoading(false); return; }
    
    const { data } = await supabase
      .from('user_profiles')
      .select('subscription_tier')
      .eq('id', user.id)
      .single();
    
    setTier((data?.subscription_tier as SubscriptionTier) || 'free');
    setLoading(false);
  };

  useEffect(() => { fetchTier(); }, []);

  return { tier, loading, refresh: fetchTier };
}
```

### Step 4 — Upgrade PlanSelector UI

In `src/app/pages/PlanSelector.tsx`, wire the "Upgrade" buttons to call the `create-checkout` edge function:
```typescript
const handleUpgrade = async (priceId: string) => {
  const { data } = await supabase.functions.invoke('create-checkout', {
    body: { priceId, successUrl: '/checkout-success', cancelUrl: '/plans' }
  });
  if (data?.url) window.location.href = data.url;
};
```

### Step 5 — Customer Portal

Verify `supabase/functions/customer-portal/index.ts` or `stripe-portal/index.ts` works and is linked from the Settings page so users can manage/cancel their subscription.

## Dependencies

None — but coordinate with TODO #016 (secrets in edge functions) since Stripe API key should be a server-side secret.

## Effort

L (3-5 days)

## Acceptance Criteria

- [ ] Complete checkout flow documented (README or PLAN.md section)
- [ ] `create-checkout` edge function creates real Stripe checkout sessions
- [ ] Stripe webhook handles `subscription.*` events and updates DB
- [ ] `useSubscriptionTier` hook reads real tier from DB
- [ ] `FeatureGate` component checks actual subscription tier
- [ ] PlanSelector "Upgrade" buttons trigger real Stripe checkout
- [ ] Customer Portal link works from Settings page
- [ ] All four tiers visible and correctly priced on `/plans`
- [ ] Subscription tier persists after user logs out and back in
- [ ] `npm run typecheck` passes
- [ ] `npm run test:ci` passes (billing tests updated)
