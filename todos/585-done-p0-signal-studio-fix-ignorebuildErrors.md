# TODO-585: Fix ignoreBuildErrors in next.config.mjs

**Repo:** signal-studio
**Priority:** P0
**Effort:** S (1-2 hours)
**Status:** pending

## Problem
`next.config.mjs` line 8 has `typescript: { ignoreBuildErrors: true }`. This silently swallows TypeScript 
errors during production builds on Railway. For a financial platform this is a compliance risk — type 
errors may hide data shape mismatches, API contract violations, or security issues.

## Task
1. Remove `ignoreBuildErrors: true` from `next.config.mjs`
2. Run `tsc --noEmit` to surface all hidden errors
3. Fix each error (may be 10-50 depending on accumulated debt)
4. Confirm `next build` succeeds with no type errors
5. Update CI pipeline to block merge if TypeScript errors present

## Coding Prompt
```
In /data/workspace/projects/signal-studio/next.config.mjs, remove the typescript.ignoreBuildErrors flag.
Then run: cd /data/workspace/projects/signal-studio && npx tsc --noEmit 2>&1 | head -100
Fix the top errors first (focus on any `any` casts that hide real type issues in API routes).
Goal: clean tsc output with 0 errors.
```

## Acceptance Criteria
- [ ] `ignoreBuildErrors` removed from next.config.mjs
- [ ] `tsc --noEmit` exits 0
- [ ] `next build` succeeds
- [ ] CI enforces this going forward

## Dependencies
None — can execute immediately
