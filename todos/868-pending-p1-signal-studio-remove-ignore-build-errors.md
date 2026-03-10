# 868 — Remove ignoreBuildErrors + Enable TypeScript Strict

**Repo:** signal-studio  
**Priority:** P1 — High  
**Effort:** 1 day  
**Status:** pending

## Problem
`next.config.mjs` has `typescript: { ignoreBuildErrors: true }` which silences ALL TypeScript compilation errors during `next build`. This means broken code can ship to production without any warning.

## Task
1. Remove `ignoreBuildErrors: true` from `next.config.mjs`
2. Add `tsc --noEmit` to CI pipeline
3. Fix any remaining TypeScript errors that surface

## Coding Prompt (for autonomous agent)
```
1. Edit /data/workspace/projects/signal-studio/next.config.mjs
   Remove: typescript: { ignoreBuildErrors: true }
   (Remove the entire typescript block or set ignoreBuildErrors: false)

2. Run: cd /data/workspace/projects/signal-studio && pnpm tsc --noEmit 2>&1 | head -100
   Note all errors.

3. Fix each error:
   - Import errors: fix import paths
   - Type errors: add proper types (should mostly be covered by TODO-867)
   - Missing types: add @types/* packages if needed

4. Edit /data/workspace/projects/signal-studio/bitbucket-pipelines.yml
   Add after lint step:
     - pnpm tsc --noEmit

5. Run pnpm build to confirm build succeeds
```

## Acceptance Criteria
- [ ] `next.config.mjs` has no `ignoreBuildErrors` setting
- [ ] `pnpm build` completes successfully with no TypeScript errors
- [ ] `pnpm tsc --noEmit` runs in CI pipeline
- [ ] No regression in app functionality

## Dependencies
- Depends on #867 (fix any-types) — do that first to reduce noise
