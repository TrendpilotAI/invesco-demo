# TODO-726: Subscription Upsell Flow — DONE

**Commit:** e6a7d9a  
**Status:** completed  
**Pushed:** main branch on TrendpilotAI/flip-my-era

## What was implemented

### New files
- `src/modules/credits/hooks/useCredits.ts` — `useCredits()` hook with `isExhausted` boolean and `checkBeforeGenerate()` helper. Fires `credits:exhausted` custom DOM event when balance is 0 during a generation attempt.
- `src/modules/credits/components/CreditExhaustionModal.tsx` — Global upsell modal that listens to `credits:exhausted` event. Displays three upgrade tiers (Swiftie Starter $12.99, Swiftie Deluxe $25, Opus VIP $49.99) with plan highlights and "Upgrade Now" CTAs wired to `/checkout?plan=xxx`.
- `src/modules/credits/index.ts` — module barrel export.

### Updated files
- `src/app/App.tsx` — mounts `<CreditExhaustionModal />` globally next to `<Toaster />` so it's available everywhere.
- `src/modules/ebook/components/EbookGenerator.tsx` — fires `credits:exhausted` event when `current_balance === 0` (opens upsell modal), falls back to legacy credit modal for partial balances.
- `supabase/functions/create-checkout/index.ts` — subscription success URL → `/dashboard?upgrade=success`; cancel URL → `/pricing?cancelled=true`.
- `src/modules/user/components/UserDashboard.tsx` — detects `?upgrade=success` and `?cancelled=true` query params, shows toasts, cleans URL.
- `src/modules/shared/components/PricingPage.tsx` — detects `?cancelled=true` on mount and shows "Checkout cancelled" toast.

## Acceptance criteria status
- ✅ Free user with 0 credits hitting generate sees upsell modal
- ✅ Modal links to pricing page with plan comparison ("Compare all plans →")
- ✅ Pricing page has "Subscribe" buttons for each paid tier → Stripe checkout
- ✅ Stripe checkout success/cancel return URLs properly set
- ✅ Webhook already handles `checkout.session.completed` → credits + plan update
- ✅ Upgrade success toast shown on dashboard post-payment
- ✅ Build passes, zero TypeScript errors
