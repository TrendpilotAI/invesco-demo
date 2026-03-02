# TODO-384: Fix ignoreBuildErrors in next.config.mjs

**Repo:** signal-studio
**Priority:** P0 (HIGH severity — hides TypeScript bugs in production)
**Effort:** S (2-4 hours)
**Status:** pending
**Audit ref:** QUALITY-002

## Description
`next.config.mjs` has `typescript: { ignoreBuildErrors: true }` which silently suppresses TypeScript compilation errors during `next build`. On a financial platform this means type-unsafe code ships to production undetected.

## Task
1. Remove `typescript: { ignoreBuildErrors: true }` from `next.config.mjs`
2. Run `pnpm tsc --noEmit` to surface all current type errors
3. Fix each type error — common patterns:
   - Add explicit return types to API route handlers
   - Fix `any` types in Oracle response objects
   - Fix missing null checks on optional chaining
4. Verify `pnpm build` completes without errors
5. Add to CI: `pnpm tsc --noEmit` step in bitbucket-pipelines.yml

## Coding Prompt (autonomous execution)
```
In /data/workspace/projects/signal-studio/next.config.mjs:
1. Remove the typescript.ignoreBuildErrors block entirely
2. Run: cd /data/workspace/projects/signal-studio && pnpm tsc --noEmit 2>&1 | head -100
3. For each error, fix it. Focus on:
   - app/api/**/*.ts — add proper Response types
   - lib/oracle*.ts — type Oracle query results
   - components/**/*.tsx — fix prop types
4. Run pnpm build to verify clean build
5. Update bitbucket-pipelines.yml to add tsc check step
```

## Acceptance Criteria
- [ ] `ignoreBuildErrors` removed from next.config.mjs
- [ ] `pnpm tsc --noEmit` exits 0
- [ ] `pnpm build` completes without errors
- [ ] CI pipeline includes type check step

## Dependencies
None — do this first.
