# TODO-323: Sentry Integration — Signal Builder Frontend

**Priority:** P0 (High)
**Status:** Pending
**Project:** signal-builder-frontend
**Effort:** S (4 hours)
**Source:** PLAN.md → P0-001

---

## Task Description

Add Sentry error monitoring to the Signal Builder Frontend for immediate production error visibility. This includes SDK setup, React Router integration, and an error boundary around the ReactFlow builder canvas.

---

## Coding Prompt

```
You are working in the Signal Builder Frontend repo at /data/workspace/projects/signal-builder-frontend.

Implement Sentry error monitoring:

1. Install the Sentry React SDK:
   ```
   yarn add @sentry/react
   ```

2. Initialize Sentry in `src/index.tsx` (before ReactDOM.render / createRoot):
   ```ts
   import * as Sentry from '@sentry/react';

   Sentry.init({
     dsn: process.env.REACT_APP_SENTRY_DSN,
     environment: process.env.REACT_APP_ENV || 'production',
     integrations: [
       new Sentry.BrowserTracing({
         routingInstrumentation: Sentry.reactRouterV6Instrumentation(
           React.useEffect,
           useLocation,
           useNavigationType,
           createRoutesFromChildren,
           matchRoutes
         ),
       }),
     ],
     tracesSampleRate: 0.2,
   });
   ```

3. Wrap the ReactFlow builder canvas component with a Sentry error boundary:
   - Find the main canvas component in `src/modules/builder/`
   - Wrap it: `<Sentry.ErrorBoundary fallback={<BuilderErrorFallback />}>`
   - Create a simple `BuilderErrorFallback` component that shows a friendly error message with a "Reload" button

4. Add environment variable to `.env.schema` (or `.env.example` if schema doesn't exist):
   ```
   REACT_APP_SENTRY_DSN=your_sentry_dsn_here
   REACT_APP_ENV=production
   ```

5. Add Sentry to the app-level error boundary if one exists in `src/App.tsx`.

6. Test by throwing a test error in dev and confirming it's captured.

Do NOT hardcode DSN values. All config via environment variables only.
```

---

## Acceptance Criteria

- [ ] `@sentry/react` installed and initialized in `src/index.tsx`
- [ ] React Router v6 routing instrumentation wired up
- [ ] ReactFlow builder canvas wrapped in `Sentry.ErrorBoundary`
- [ ] `REACT_APP_SENTRY_DSN` documented in `.env.schema` / `.env.example`
- [ ] No DSN or credentials hardcoded in source
- [ ] Errors thrown in dev appear captured (verify via Sentry dashboard or console)
- [ ] Build passes (`yarn build`)
