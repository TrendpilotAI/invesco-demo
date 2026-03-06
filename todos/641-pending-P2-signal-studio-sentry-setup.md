# TODO-641: Add Sentry Error Tracking to Signal Studio

**Priority:** P2  
**Effort:** XS (2hrs)  
**Repo:** signal-studio  
**Category:** Operations / Observability  

## Problem

No production error tracking. Unhandled promise rejections, React rendering errors, and API failures are silent in production. Only visible via Railway logs (no alerting, no context, no stack traces linked to code).

## Coding Prompt (Autonomous Execution)

```
In /data/workspace/projects/signal-studio:
1. Run: pnpm add @sentry/nextjs
2. Run: npx @sentry/wizard@latest -i nextjs
   - This generates sentry.client.config.ts, sentry.server.config.ts, sentry.edge.config.ts
   - Set DSN to process.env.NEXT_PUBLIC_SENTRY_DSN
3. Add NEXT_PUBLIC_SENTRY_DSN to .env.example (without real value)
4. Add real DSN as Railway env var (get from sentry.io free tier)
5. Add SENTRY_AUTH_TOKEN to Railway env vars (for source map uploads)
6. Verify next.config.mjs wraps with withSentryConfig
7. Deploy and trigger a test error to verify Sentry receives it
```

## Acceptance Criteria

- [ ] `@sentry/nextjs` installed and configured
- [ ] Sentry config files present (client/server/edge)
- [ ] DSN stored in env vars only (never committed)
- [ ] Source maps uploaded to Sentry on build
- [ ] Test error appears in Sentry dashboard within 60s of triggering

## Dependencies

None
