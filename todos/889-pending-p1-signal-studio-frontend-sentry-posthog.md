# TODO-889: Add Sentry + PostHog for Observability

**Repo:** signal-studio-frontend  
**Priority:** P1  
**Effort:** S (2-3 hours)  
**Status:** pending  
**Identified:** 2026-03-10 by Judge Agent v2

## Description

No error tracking or product analytics in place. Once production is deployed (TODO-886),
we're flying blind. Sentry catches crashes; PostHog tracks feature usage.

## Coding Prompt

```
In /data/workspace/projects/signal-studio-frontend/:

STEP 1: Install Sentry
pnpm add @sentry/nextjs
npx @sentry/wizard@latest -i nextjs

Configure in next.config.mjs:
  import { withSentryConfig } from '@sentry/nextjs'
  export default withSentryConfig(nextConfig, { silent: true })

Add to instrumentation.ts:
  import * as Sentry from '@sentry/nextjs'
  Sentry.init({ dsn: process.env.SENTRY_DSN, tracesSampleRate: 0.1 })

STEP 2: Install PostHog
pnpm add posthog-js posthog-node

Create lib/analytics.ts:
  import posthog from 'posthog-js'
  
  export function trackEvent(event: string, properties?: Record<string, unknown>) {
    if (typeof window !== 'undefined' && process.env.NEXT_PUBLIC_POSTHOG_KEY) {
      posthog.capture(event, properties)
    }
  }

Add PostHog initialization to app/layout.tsx.

STEP 3: Track key events
- 'signal_created' — when user creates a signal
- 'ai_chat_message_sent' — model, message_length (no content)
- 'oracle_query_run' — table_count, has_filters
- 'visual_builder_node_added' — node_type
- 'report_exported' — format (when implemented)

Add trackEvent() calls at each action.

STEP 4: Add env vars
SENTRY_DSN=https://...@sentry.io/...
NEXT_PUBLIC_POSTHOG_KEY=phc_...
NEXT_PUBLIC_POSTHOG_HOST=https://app.posthog.com
```

## Acceptance Criteria
- [ ] Sentry configured and receiving errors in test environment
- [ ] PostHog receiving events in test environment
- [ ] 5+ key user actions tracked
- [ ] No PII (email, message content) sent to analytics
- [ ] Both services initialized only in production (`NODE_ENV === 'production'`)

## Dependencies
- TODO-886 (production deployment) should be complete first
