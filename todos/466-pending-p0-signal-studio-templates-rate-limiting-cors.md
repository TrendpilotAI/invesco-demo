# TODO-466: Add Rate Limiting and CORS to Templates API

**Repo:** signal-studio-templates
**Priority:** P0
**Effort:** S (2h)
**Status:** pending
**Source:** judge-agent-v2 / AUDIT.md SEC-1, SEC-2, SEC-3

## Description

The Templates REST API has no rate limiting, no CORS configuration, and no request body size limits. For Invesco production deployment, these are blocking security requirements.

## Acceptance Criteria

- [ ] `express-rate-limit` installed and configured: global 100 req/15min, execute endpoint 20 req/min
- [ ] `cors` middleware with allowlist: `['https://*.forwardlane.com', 'https://*.invesco.com']`
- [ ] `express.json({ limit: '10kb' })` applied
- [ ] All tests still pass
- [ ] Security config documented in README

## Agent Prompt

```
In /data/workspace/projects/signal-studio-templates/api/templates.ts:

1. Install: pnpm add express-rate-limit cors && pnpm add -D @types/cors

2. Add to top of createTemplateRouter():
   - Import rateLimit from 'express-rate-limit'
   - Import cors from 'cors'
   - Add cors middleware: router.use(cors({ origin: ['https://*.forwardlane.com', 'https://*.invesco.com'] }))
   - Add global rate limit: 100 req per 15 min
   - Add execute-specific limit: 20 req per 60 sec on POST /templates/:id/execute
   - Add express.json({ limit: '10kb' }) (or document this as app-level config)

3. Run: pnpm test && pnpm build

4. Update README.md with security configuration section
```

## Dependencies

- None (standalone security fix)
