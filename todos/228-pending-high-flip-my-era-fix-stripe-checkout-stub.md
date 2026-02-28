## Task: Fix Stubbed Stripe Checkout Integration
## Priority: HIGH 🔴
## Effort: 6 hours
## Description:
The billing module's `createCheckoutSession` function returns a fake `checkout.stripe.com/stub/...` URL instead of calling the real Stripe API. This means checkout is silently broken in production — users cannot actually purchase. Must be fixed immediately.

Also check: email module stubs all sends as `{success: true}` — transactional emails (welcome, receipt, password reset) may also not be sending.

## Coding Prompt:
You are fixing a critical billing bug in FlipMyEra at /data/workspace/projects/flip-my-era/.

**Step 1: Find the stubs**
```bash
grep -rn "stub\|checkout.stripe.com/stub" /data/workspace/projects/flip-my-era/src/ | grep -v node_modules | grep -v ".test."
grep -rn "success: true" /data/workspace/projects/flip-my-era/src/modules/ | grep -v ".test."
```

**Step 2: Fix Stripe checkout**
The real checkout should call the Supabase Edge Function `create-checkout`:
```typescript
// src/modules/billing/services/billing.ts (or wherever the stub is)
export async function createCheckoutSession(planId: string, userId: string) {
  const { data, error } = await supabase.functions.invoke('create-checkout', {
    body: { planId, userId, returnUrl: window.location.origin + '/checkout/success' }
  });
  if (error) throw error;
  // Redirect to real Stripe URL
  window.location.href = data.url;
}
```

**Step 3: Verify Edge Function is wired**
Check `supabase/functions/create-checkout/index.ts`:
- Must use `STRIPE_SECRET_KEY` from Deno env (not VITE_ prefix)
- Must create a real Stripe checkout session
- Must return `{ url: string }` with the real Stripe URL

**Step 4: Fix email stubs**
Find email service stubs and wire to Brevo (the brevo-email edge function exists):
```bash
grep -rn "success: true" /data/workspace/projects/flip-my-era/src/ | grep -i email
```
Wire to `supabase/functions/brevo-email/` for actual delivery.

**Step 5: Test**
- Manually test checkout flow in Stripe test mode
- Verify real session URL is returned
- Verify webhook receives payment success event

## Acceptance Criteria:
- [ ] `createCheckoutSession` calls real Stripe API (via Edge Function)
- [ ] Real Stripe checkout URL returned and user redirected
- [ ] Stripe webhook receives and processes payment events
- [ ] Transactional emails actually send via Brevo
- [ ] No stub URLs in production code
- [ ] E2E checkout test passes

## Dependencies: 016-pending-P1-flip-my-era-move-secrets-to-edge-functions.md
