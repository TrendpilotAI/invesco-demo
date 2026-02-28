# 240 · P1 · Trendpilot — Add Stripe Subscription Payments

## Status
pending

## Priority
P1 — revenue gate

## Description
Add Stripe subscription billing with three tiers: Free, Pro ($29/mo), Business ($99/mo). Implement: Stripe Checkout session creation, webhook handler (subscription created/updated/cancelled), feature gating based on plan, and a billing portal link in the dashboard.

## Dependencies
- TODO #238 (Auth) — users must be authenticated before subscribing
- TODO #239 (Email) — receipts via SendGrid
- `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`, `STRIPE_PRICE_PRO`, `STRIPE_PRICE_BUSINESS` env vars

## Estimated Effort
2 days

## Coding Prompt

```
You are working on the Trendpilot project at /data/workspace/projects/Trendpilot/.

TASK: Implement Stripe subscription billing with checkout, webhooks, and feature gating.

STEP 1 — Install Stripe:
```bash
npm install stripe
```

STEP 2 — Create `src/services/billing/stripe.ts`:
```ts
import Stripe from 'stripe';

export const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2024-12-18.acacia',
});

export const PLANS = {
  free: { name: 'Free', price: 0, priceId: null, limits: { newsletters: 2, subscribers: 100 } },
  pro: { name: 'Pro', price: 29, priceId: process.env.STRIPE_PRICE_PRO!, limits: { newsletters: 50, subscribers: 5000 } },
  business: { name: 'Business', price: 99, priceId: process.env.STRIPE_PRICE_BUSINESS!, limits: { newsletters: -1, subscribers: -1 } },
} as const;

export type PlanKey = keyof typeof PLANS;

export async function createCheckoutSession(
  userId: string,
  userEmail: string,
  plan: 'pro' | 'business',
  successUrl: string,
  cancelUrl: string
): Promise<string> {
  const session = await stripe.checkout.sessions.create({
    mode: 'subscription',
    customer_email: userEmail,
    line_items: [{ price: PLANS[plan].priceId, quantity: 1 }],
    success_url: successUrl,
    cancel_url: cancelUrl,
    metadata: { userId },
    subscription_data: { metadata: { userId } },
  });
  return session.url!;
}

export async function createBillingPortalSession(
  customerId: string,
  returnUrl: string
): Promise<string> {
  const session = await stripe.billingPortal.sessions.create({
    customer: customerId,
    return_url: returnUrl,
  });
  return session.url;
}
```

STEP 3 — Add `stripe_customer_id` and `plan` columns to Supabase users table:
Create migration `supabase/migrations/TIMESTAMP_add_billing.sql`:
```sql
ALTER TABLE auth.users ADD COLUMN IF NOT EXISTS raw_app_meta_data jsonb DEFAULT '{}';
-- Use a separate profiles table for billing info:
CREATE TABLE IF NOT EXISTS public.user_profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  stripe_customer_id TEXT,
  plan TEXT NOT NULL DEFAULT 'free',
  plan_expires_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT now()
);
ALTER TABLE public.user_profiles ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can view own profile" ON public.user_profiles
  FOR SELECT USING (auth.uid() = id);
```

STEP 4 — Billing API routes in `src/api/index.ts`:
```ts
import { stripe, createCheckoutSession, createBillingPortalSession } from '@/services/billing/stripe.js';
import * as db from '@/services/db.js';

// POST /api/billing/checkout — create Stripe Checkout session
app.post('/api/billing/checkout', requireAuth, async (req, res) => {
  const { plan } = req.body as { plan: 'pro' | 'business' };
  const user = (req as any).user;
  
  const url = await createCheckoutSession(
    user.id,
    user.email,
    plan,
    `${process.env.NEXT_PUBLIC_APP_URL}/dashboard?upgraded=true`,
    `${process.env.NEXT_PUBLIC_APP_URL}/pricing`
  );
  
  res.json({ url });
});

// POST /api/billing/portal — create Stripe Customer Portal session
app.post('/api/billing/portal', requireAuth, async (req, res) => {
  const user = (req as any).user;
  const profile = await db.userProfiles.findByUserId(user.id);
  if (!profile?.stripe_customer_id) return res.status(400).json({ error: 'No billing account found' });
  
  const url = await createBillingPortalSession(
    profile.stripe_customer_id,
    `${process.env.NEXT_PUBLIC_APP_URL}/dashboard`
  );
  res.json({ url });
});

// POST /api/webhooks/stripe — Stripe webhook handler
app.post('/api/webhooks/stripe', express.raw({ type: 'application/json' }), async (req, res) => {
  const sig = req.headers['stripe-signature']!;
  let event: Stripe.Event;
  
  try {
    event = stripe.webhooks.constructEvent(req.body, sig, process.env.STRIPE_WEBHOOK_SECRET!);
  } catch (err) {
    return res.status(400).send(`Webhook error: ${err}`);
  }
  
  switch (event.type) {
    case 'checkout.session.completed': {
      const session = event.data.object as Stripe.CheckoutSession;
      const userId = session.metadata?.userId;
      const customerId = session.customer as string;
      if (userId) {
        await db.userProfiles.upsert(userId, {
          stripe_customer_id: customerId,
          plan: 'pro', // determine from line items
        });
      }
      break;
    }
    
    case 'customer.subscription.updated':
    case 'customer.subscription.deleted': {
      const sub = event.data.object as Stripe.Subscription;
      const userId = sub.metadata?.userId;
      const plan = event.type === 'customer.subscription.deleted' ? 'free' : 'pro';
      if (userId) await db.userProfiles.upsert(userId, { plan });
      break;
    }
  }
  
  res.json({ received: true });
});
```

STEP 5 — Add `db.userProfiles` methods to `src/services/db.ts`:
```ts
export const userProfiles = {
  findByUserId: async (userId: string) => {
    const { data } = await supabase.from('user_profiles').select().eq('id', userId).maybeSingle();
    return data;
  },
  upsert: async (userId: string, data: Partial<{ stripe_customer_id: string; plan: string; plan_expires_at: string }>) => {
    return throwOnError(await supabase.from('user_profiles').upsert({ id: userId, ...data }).select().single());
  },
};
```

STEP 6 — Feature gating middleware:
```ts
export function requirePlan(minPlan: 'pro' | 'business') {
  return async (req: Request, res: Response, next: NextFunction) => {
    const user = (req as any).user;
    const profile = await db.userProfiles.findByUserId(user.id);
    const plan = profile?.plan ?? 'free';
    const planOrder = { free: 0, pro: 1, business: 2 };
    if (planOrder[plan as keyof typeof planOrder] < planOrder[minPlan]) {
      return res.status(403).json({ error: 'Upgrade required', upgradeUrl: '/pricing' });
    }
    next();
  };
}

// Apply to premium routes:
app.post('/api/newsletters', requireAuth, requirePlan('pro'), async (req, res) => { ... });
```

STEP 7 — Dashboard billing UI:
In `dashboard/src/pages/Settings.tsx`, add:
- Current plan display (fetch from `/api/billing/status`)
- "Upgrade to Pro" button → POST /api/billing/checkout → redirect to Stripe
- "Manage Billing" button → POST /api/billing/portal → redirect to portal
- Show feature limits (newsletters remaining, subscriber count)

STEP 8 — Testing with Stripe CLI:
```bash
stripe listen --forward-to localhost:3001/api/webhooks/stripe
stripe trigger checkout.session.completed
```
```

## Acceptance Criteria
- [ ] `POST /api/billing/checkout?plan=pro` returns a valid Stripe Checkout URL
- [ ] Completing checkout → user's `plan` updated to 'pro' in Supabase `user_profiles`
- [ ] Free users get 403 on `POST /api/newsletters` (plan-gated route)
- [ ] Pro users can create newsletters without 403
- [ ] `POST /api/billing/portal` returns Stripe Customer Portal URL
- [ ] Cancelling subscription via portal → plan reverted to 'free' in Supabase
- [ ] Webhook signature verification rejects invalid signatures with 400
- [ ] Dashboard shows current plan and upgrade/manage buttons
