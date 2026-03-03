# TODO-450: PostHog Analytics + Sentry Error Tracking

**Repo:** signal-studio-frontend  
**Priority:** Medium  
**Effort:** S (4-6 hours)  
**Status:** pending

## Description

No product analytics or error tracking exists. PostHog gives event-level analytics for feature adoption. Sentry captures frontend exceptions with stack traces and source maps.

## Coding Prompt

```
In /data/workspace/projects/signal-studio-frontend/:

### PostHog Setup

1. npm install posthog-js posthog-node

2. Create src/lib/posthog.ts:
```typescript
import posthog from 'posthog-js'

export function initPostHog() {
  if (typeof window !== 'undefined' && process.env.NEXT_PUBLIC_POSTHOG_KEY) {
    posthog.init(process.env.NEXT_PUBLIC_POSTHOG_KEY, {
      api_host: process.env.NEXT_PUBLIC_POSTHOG_HOST || 'https://us.i.posthog.com',
      capture_pageview: false, // manual control
    })
  }
}

export { posthog }
```

3. Create src/components/providers/posthog-provider.tsx with PostHogProvider wrapper
4. Add to app/layout.tsx providers
5. Add event tracking to key actions:
   - `posthog.capture('signal_created', { type, name })`
   - `posthog.capture('signal_run_triggered', { signalId })`
   - `posthog.capture('template_used', { templateId })`
   - `posthog.capture('chat_message_sent', { model })`

### Sentry Setup

1. npx @sentry/wizard@latest -i nextjs
2. Wire Sentry to error.tsx boundaries:
```typescript
import * as Sentry from '@sentry/nextjs'
// In error.tsx useEffect:
useEffect(() => { Sentry.captureException(error) }, [error])
```
3. Add SENTRY_DSN to Railway environment variables
4. Enable source maps upload in Sentry Next.js config
```

## Acceptance Criteria
- [ ] PostHog receives pageview events on navigation
- [ ] Signal creation/run events tracked in PostHog
- [ ] Sentry captures unhandled exceptions
- [ ] Source maps uploaded to Sentry for readable stack traces
