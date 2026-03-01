# TODO 360 — Signal Studio Frontend: Analytics (PostHog) + Error Tracking (Sentry)

**Status:** pending  
**Priority:** medium  
**Project:** signal-studio-frontend  
**Estimated Effort:** 4–6 hours  

---

## Description

Production frontend needs error capture (Sentry) and usage analytics (PostHog) to understand user behavior and catch runtime errors. Both integrate cleanly with Next.js App Router.

---

## Coding Prompt (Autonomous Agent)

```
Repo: /data/workspace/projects/signal-studio-frontend

Task: Integrate Sentry error tracking and PostHog analytics into the Next.js app.

=== SENTRY ===

Step 1 — Install
  pnpm add @sentry/nextjs

Step 2 — Init
  Run: npx @sentry/wizard@latest -i nextjs --skip-connect (or manually create config)
  
  Create `sentry.client.config.ts`:
    import * as Sentry from '@sentry/nextjs';
    Sentry.init({
      dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
      tracesSampleRate: 0.1,
      environment: process.env.NODE_ENV,
    });
  
  Create `sentry.server.config.ts` and `sentry.edge.config.ts` similarly.

Step 3 — next.config.ts
  Wrap the Next.js config with `withSentryConfig()`.

Step 4 — Error Boundary
  Update the ErrorBoundary component (from TODO 356) to also call
  `Sentry.captureException(error)` in componentDidCatch.

=== POSTHOG ===

Step 5 — Install
  pnpm add posthog-js posthog-node

Step 6 — Client Provider
  Create `src/components/PostHogProvider.tsx`:
  ```tsx
  'use client';
  import posthog from 'posthog-js';
  import { PostHogProvider as PHProvider } from 'posthog-js/react';
  import { useEffect } from 'react';
  
  export function PostHogProvider({ children }) {
    useEffect(() => {
      posthog.init(process.env.NEXT_PUBLIC_POSTHOG_KEY!, {
        api_host: process.env.NEXT_PUBLIC_POSTHOG_HOST ?? 'https://app.posthog.com',
        capture_pageview: false, // handled manually for SPA routing
      });
    }, []);
    return <PHProvider client={posthog}>{children}</PHProvider>;
  }
  ```
  
  Wrap the body in `layout.tsx` with `<PostHogProvider>`.

Step 7 — Page View Tracking
  Create `src/components/PostHogPageView.tsx` — a client component that calls
  `posthog.capture('$pageview')` on route changes using `usePathname()` and
  `useSearchParams()` in a useEffect.
  
  Mount `<PostHogPageView />` in layout.tsx.

Step 8 — Event Tracking Helpers
  Create `src/lib/analytics.ts`:
    export const track = (event: string, props?: Record<string, unknown>) =>
      posthog.capture(event, props);
  
  Add tracking calls to key user actions:
    - Signal created: track('signal_created')
    - Signal run triggered: track('signal_run_triggered')
    - Template used: track('template_used', { templateId })

Step 9 — Environment Variables
  Add to `.env.example`:
    NEXT_PUBLIC_SENTRY_DSN=
    NEXT_PUBLIC_POSTHOG_KEY=
    NEXT_PUBLIC_POSTHOG_HOST=

Step 10 — Verify
  `pnpm tsc --noEmit` + `pnpm build` pass.
  Sentry source maps upload during build (verify in build output).
```

---

## Dependencies

- TODO 356 (error boundary) — Sentry hooks into the ErrorBoundary

---

## Acceptance Criteria

- [ ] Sentry initialized; unhandled errors are captured in componentDidCatch
- [ ] PostHog initialized; pageviews tracked on route change
- [ ] Key user actions tracked: signal_created, signal_run_triggered, template_used
- [ ] `.env.example` updated with required env vars
- [ ] `pnpm tsc --noEmit` passes, `pnpm build` succeeds (with source maps uploading)
