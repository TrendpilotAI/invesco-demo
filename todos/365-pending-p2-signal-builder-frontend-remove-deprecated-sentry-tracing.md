# TODO-341: Remove Deprecated @sentry/tracing Package

**Repo:** signal-builder-frontend  
**Priority:** P2 | **Effort:** XS (30min)  
**Status:** pending

## Problem
`@sentry/tracing` is deprecated since Sentry v7.x — its functionality was merged into `@sentry/react`. It's still in package.json as an explicit dependency, adding dead weight and potential CVE exposure.

## Task
1. Remove `@sentry/tracing` from package.json
2. Search codebase for any imports of `@sentry/tracing` and replace with `@sentry/react` equivalents
3. Verify Sentry still initializes correctly and captures errors

## Coding Prompt
```
cd /data/workspace/projects/signal-builder-frontend
1. grep -r "@sentry/tracing" src/ to find any imports
2. Replace BrowserTracing import: from '@sentry/tracing' → from '@sentry/react'
3. Run: npm uninstall @sentry/tracing (or remove from package.json manually)
4. npm install && npm run build to verify no breakage
```

## Acceptance Criteria
- [ ] `@sentry/tracing` removed from package.json
- [ ] No import errors in build
- [ ] Sentry integration still functional
