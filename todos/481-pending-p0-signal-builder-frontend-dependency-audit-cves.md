# TODO-481: Dependency Audit — Fix CVEs + Remove Deprecated Packages

**Project:** signal-builder-frontend
**Priority:** P0 (HIGH impact, S effort)
**Estimated Effort:** 2-3 hours
**Dependencies:** None

## Description

Multiple security issues: @storybook v6 has webpack CVEs, @sentry/tracing is deprecated (merged into @sentry/react v7+), lodash full bundle (not tree-shakeable). Fix CVEs and remove deprecated deps.

## Coding Prompt

```
You are working on signal-builder-frontend at /data/workspace/projects/signal-builder-frontend/.

TASK: Audit and fix dependency vulnerabilities.

STEPS:
1. Run: pnpm audit --audit-level=high — document findings

2. Remove @sentry/tracing from package.json (it's deprecated, @sentry/react v7+ includes it):
   pnpm remove @sentry/tracing
   Update any imports from '@sentry/tracing' to use '@sentry/react' equivalents

3. Replace lodash with lodash-es for tree-shaking (~50KB bundle savings):
   pnpm remove lodash @types/lodash
   pnpm add lodash-es
   pnpm add -D @types/lodash-es
   Update all 28 import sites: `import { debounce } from 'lodash'` → `import { debounce } from 'lodash-es'`
   OR replace with native alternatives where possible:
   - _.cloneDeep → structuredClone
   - _.get → optional chaining
   - _.isEmpty → direct checks
   - _.isEqual → JSON.stringify for simple cases

4. Run: pnpm audit --audit-level=high — verify reduction
5. Run: pnpm typecheck && pnpm build && pnpm test

CONSTRAINTS:
- Don't break any existing functionality
- Prefer native alternatives over lodash-es where equivalent
- Document remaining unresolvable CVEs in a SECURITY.md
```

## Acceptance Criteria
- [ ] @sentry/tracing removed, Sentry still works
- [ ] lodash replaced with lodash-es or native alternatives
- [ ] `pnpm audit` shows no high/critical CVEs (or documented exceptions)
- [ ] Bundle size reduced by ≥40KB
- [ ] `pnpm build` succeeds
- [ ] `pnpm typecheck` passes
