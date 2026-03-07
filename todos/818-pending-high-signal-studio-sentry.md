# TODO-818: Add Sentry error monitoring

**Priority**: HIGH (P1)
**Repo**: signal-studio
**Source**: BRAINSTORM.md → 4.1, AUDIT.md → AUDIT-009

## Description
No error monitoring exists. Production errors are silent. Add Sentry for client + server error tracking.

## Coding Prompt
```
In /data/workspace/projects/signal-studio:

1. Install: pnpm add @sentry/nextjs

2. Run Sentry wizard: npx @sentry/wizard@latest -i nextjs
   This creates: sentry.client.config.ts, sentry.server.config.ts, sentry.edge.config.ts
   And updates next.config.mjs with withSentryConfig wrapper.

3. Add env vars to .env.example:
   SENTRY_DSN=https://...@sentry.io/...
   SENTRY_AUTH_TOKEN=... # for source map upload

4. Add to bitbucket-pipelines.yml after build step:
   # Source maps are uploaded automatically by @sentry/nextjs during build

5. Configure in sentry.client.config.ts:
   - tracesSampleRate: 0.1 (10% in prod)
   - environment: process.env.NODE_ENV
   - ignoreErrors: ['ResizeObserver loop limit exceeded']

6. Add SENTRY_DSN and SENTRY_AUTH_TOKEN to Railway environment variables.

7. Test: trigger a deliberate error in dev and verify it appears in Sentry dashboard.
```

## Acceptance Criteria
- [ ] Client errors captured in Sentry
- [ ] Server (API route) errors captured in Sentry
- [ ] Source maps uploaded so stack traces are readable
- [ ] Sentry integrated in both staging and production Railway environments

## Effort
4 hours

## Dependencies
Sentry account + project creation required
