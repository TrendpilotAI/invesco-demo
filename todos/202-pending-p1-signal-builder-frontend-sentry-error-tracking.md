---
status: pending
priority: p1
issue_id: "202"
tags: [integrations, sentry, observability, signal-builder-frontend]
dependencies: ["210"]
---

# 202 — Sentry Error Tracking Integration

## Problem Statement

The Signal Builder Frontend runs in production for financial clients with no error observability. There are 4 `console.error` calls in `builder/api.ts` marked `// TODO:` that silently swallow exceptions. When signals fail to load, save, or publish, there is no alerting, no stack trace, and no context to debug. For a financial SaaS product, this is a critical gap.

## Findings

- `src/redux/builder/api.ts` has `console.error(error)` in `getSchema.onQueryStarted` (line ~36) and `getSignalUI.onQueryStarted` (line ~173), both marked `// TODO:`
- `createSignal.onQueryStarted` uses `console.log(error)` (not even error-level)
- `src/shared/widgets/ErrorBoundary/ErrorBoundary.tsx` exists — can be augmented with Sentry
- No `@sentry/react` in `package.json`
- `.env.schema` doesn't include `REACT_APP_SENTRY_DSN`

## Proposed Solutions

### Option A: @sentry/react with ErrorBoundary (Recommended)
Install `@sentry/react`, initialize in `src/index.tsx`, wrap app in Sentry ErrorBoundary.
- **Pros:** Industry standard, excellent React integration, performance tracing
- **Cons:** Adds ~50KB to bundle (async chunk-loadable)
- **Effort:** S (~2-3h)
- **Risk:** Low

### Option B: Custom logger wrapper only
Create `src/shared/lib/logger.ts` that routes to a custom endpoint.
- **Pros:** No third-party dependency
- **Cons:** Requires custom error aggregation service
- **Effort:** L
- **Risk:** Medium

## Recommended Action

Implement Option A. Sentry is the industry standard and integrates directly with React.

## Coding Prompt

```
You are working on signal-builder-frontend at /data/workspace/projects/signal-builder-frontend/.

Task: Integrate Sentry error tracking

1. Install dependencies:
   cd /data/workspace/projects/signal-builder-frontend
   yarn add @sentry/react

2. Add to .env.schema:
   REACT_APP_SENTRY_DSN=

3. Initialize Sentry in src/index.tsx (before ReactDOM.render/createRoot):
   import * as Sentry from '@sentry/react';
   Sentry.init({
     dsn: process.env.REACT_APP_SENTRY_DSN,
     environment: process.env.NODE_ENV,
     enabled: process.env.NODE_ENV === 'production',
     integrations: [Sentry.browserTracingIntegration()],
     tracesSampleRate: 0.1,
   });

4. Create src/shared/lib/logger.ts:
   import * as Sentry from '@sentry/react';
   export const logger = {
     error: (error: unknown, context?: Record<string, unknown>) => {
       if (process.env.NODE_ENV === 'production') {
         Sentry.captureException(error, { extra: context });
       } else {
         console.error('[Logger]', error, context);
       }
     },
     warn: (message: string, context?: Record<string, unknown>) => {
       if (process.env.NODE_ENV === 'production') {
         Sentry.captureMessage(message, 'warning');
       } else {
         console.warn('[Logger]', message, context);
       }
     },
   };
   export default logger;

5. Replace console.log/console.error in src/redux/builder/api.ts:
   // Replace all instances of:
   //   } catch (error: any) { console.error(error); }
   //   } catch (error: any) { console.log(error); }
   // With:
   import logger from '@shared/lib/logger';
   } catch (error: unknown) {
     logger.error(error, { endpoint: 'getSchema' });
   }

6. Augment src/shared/widgets/ErrorBoundary/ErrorBoundary.tsx to report to Sentry:
   import * as Sentry from '@sentry/react';
   // In componentDidCatch: Sentry.captureException(error, { extra: errorInfo });

7. Add export to src/shared/lib/index.ts:
   export { logger } from './logger';

8. Verify build still works:
   cd /data/workspace/projects/signal-builder-frontend && yarn typecheck
```

## Dependencies

- 210 (replace console.log with proper logging) — this TODO is a prerequisite since 202 implements the logging infrastructure that 210 uses

## Estimated Effort

**Small** — 2-3 hours

## Acceptance Criteria

- [ ] `@sentry/react` is in `package.json` dependencies
- [ ] `REACT_APP_SENTRY_DSN` is in `.env.schema`
- [ ] Sentry is initialized in `src/index.tsx`
- [ ] `src/shared/lib/logger.ts` exists with `error` and `warn` methods
- [ ] All `console.log` / `console.error` calls in `builder/api.ts` are replaced with `logger.error`
- [ ] `ErrorBoundary.tsx` calls `Sentry.captureException` in `componentDidCatch`
- [ ] `yarn typecheck` passes with no new errors
- [ ] Sentry is only enabled in production (`process.env.NODE_ENV === 'production'`)

## Work Log

### 2026-02-26 — Todo created

**By:** Planning Agent

**Actions:**
- Counted 4 console.error / console.log calls in builder/api.ts with TODO comments
- Confirmed no Sentry dependency in package.json
- Confirmed ErrorBoundary widget exists and can be augmented
