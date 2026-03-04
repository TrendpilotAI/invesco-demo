# TODO 524: Add Sentry Error Monitoring
**Repo:** Second-Opinion  
**Priority:** P2 — Production Stability  
**Effort:** 2h  
**Status:** pending

## Description
Production app at gen-lang-client-0003791133.web.app has zero error visibility. Sentry integration gives real-time alerts for patient-facing crashes.

## Coding Prompt
```
In /data/workspace/projects/Second-Opinion/:

1. npm install @sentry/react @sentry/vite-plugin
2. Create services/monitoring.ts:
   - initSentry(dsn) — call in index.tsx
   - captureError(error, context) — wrapper around Sentry.captureException
3. Wrap App.tsx in Sentry.ErrorBoundary with fallback UI
4. Add Sentry.withProfiler to main analysis components
5. Add SENTRY_DSN to .env.example and Firebase Secret Manager
6. Update vite.config.ts to use @sentry/vite-plugin for source maps
```

## Acceptance Criteria
- [ ] Errors surfaced in Sentry dashboard within 30s
- [ ] Source maps uploaded for readable stack traces
- [ ] React error boundary shows friendly error UI to users
- [ ] PII/PHI scrubbing configured (beforeSend hook filters medical data)

## Dependencies
None
