# TODO-351: Remove ignoreBuildErrors from next.config.mjs

**Priority:** P0 (Critical)
**Effort:** M
**Repo:** signal-studio
**Status:** pending

## Description
`next.config.mjs` has `typescript: { ignoreBuildErrors: true }` which silently swallows all TypeScript errors. This means type bugs ship to production undetected.

## Coding Prompt
```
In /data/workspace/projects/signal-studio/next.config.mjs:
1. Remove the entire `typescript: { ignoreBuildErrors: true }` block
2. Run: cd /data/workspace/projects/signal-studio && npx tsc --noEmit 2>&1 | head -50
3. Fix all TypeScript errors that surface (one by one, start with the most critical)
4. Also remove the deprecated `experimental.serverComponentsExternalPackages` key — keep only `serverExternalPackages`
5. Run `pnpm build` to confirm clean build
6. Commit: "fix(config): remove ignoreBuildErrors and deprecated experimental key"
```

## Dependencies
None

## Acceptance Criteria
- `next.config.mjs` has no `ignoreBuildErrors` key
- `npx tsc --noEmit` exits with 0 errors
- `pnpm build` succeeds
- `experimental.serverComponentsExternalPackages` removed (keep `serverExternalPackages`)
