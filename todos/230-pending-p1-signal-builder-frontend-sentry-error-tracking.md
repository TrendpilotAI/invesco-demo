# 230 · P1 · signal-builder-frontend · Integrate Sentry Error Tracking

## Status
pending

## Priority
P1 — 4 `console.error` TODO placeholders in production code; financial SaaS needs real error tracking

## Description
The builder API has 4 catch blocks marked `// TODO:` that only call `console.error`. This task installs Sentry, creates a logger utility, wires up the ErrorBoundary, and replaces all console calls with structured error tracking.

## Coding Prompt

```
Repo: /data/workspace/projects/signal-builder-frontend

Step 1: Install Sentry
yarn add @sentry/react

Step 2: Create logger utility at `src/shared/lib/logger.ts`
```typescript
import * as Sentry from '@sentry/react';

export const logger = {
  error: (message: string, error?: unknown, context?: Record<string, unknown>) => {
    if (process.env.NODE_ENV === 'development') {
      console.error('[ERROR]', message, error, context);
    }
    if (error instanceof Error) {
      Sentry.captureException(error, { extra: { message, ...context } });
    } else {
      Sentry.captureMessage(message, { level: 'error', extra: { error, ...context } });
    }
  },
  warn: (message: string, context?: Record<string, unknown>) => {
    if (process.env.NODE_ENV === 'development') {
      console.warn('[WARN]', message, context);
    }
    Sentry.captureMessage(message, { level: 'warning', extra: context });
  },
};
```

Step 3: Initialize Sentry in `src/index.tsx`
Add before ReactDOM.render / createRoot:
```typescript
import * as Sentry from '@sentry/react';

if (process.env.REACT_APP_SENTRY_DSN) {
  Sentry.init({
    dsn: process.env.REACT_APP_SENTRY_DSN,
    environment: process.env.REACT_APP_ENV || 'development',
    tracesSampleRate: 0.1,
    release: process.env.REACT_APP_VERSION,
  });
}
```

Step 4: Replace all console calls in `src/redux/builder/api.ts`
Replace each `console.error(error)` / `console.log(error)` with:
```typescript
import { logger } from 'shared/lib/logger';
// in catch block:
logger.error('Builder API error: getSchema', error, { endpoint: 'getSchema' });
```

Step 5: Wrap App with Sentry ErrorBoundary in `src/index.tsx` or `src/app/App.tsx`
```typescript
import { ErrorBoundary } from '@sentry/react';
// Wrap or replace existing ErrorBoundary widget:
<ErrorBoundary fallback={<ErrorFallback />}>
  <App />
</ErrorBoundary>
```

Step 6: Add `REACT_APP_SENTRY_DSN` and `REACT_APP_ENV` to `.env.schema`

Step 7: Remove mock fallback from getSchema transform in `src/redux/builder/api.ts`:
```typescript
// REMOVE THIS:
transformResponse: (response: TSchemaDTO) => response || mockSchema,
// REPLACE WITH:
transformResponse: (response: TSchemaDTO) => response,
```
Also remove the `import { mockSchema } from '../mocks/schema.mock'` if it's only used for this fallback.

Commit: "feat: add Sentry error tracking, replace console.error placeholders"
```

## Dependencies
- 229 (any type fixes) recommended first, but not strictly required

## Effort Estimate
S (4–6 hours)

## Acceptance Criteria
- [ ] `@sentry/react` in package.json
- [ ] `src/shared/lib/logger.ts` exists with error/warn methods
- [ ] Zero `console.error` / `console.log` calls in `src/redux/builder/api.ts`
- [ ] `REACT_APP_SENTRY_DSN` in `.env.schema`
- [ ] Mock schema fallback removed from production transform
- [ ] App wrapped in Sentry ErrorBoundary
- [ ] `yarn build` succeeds
