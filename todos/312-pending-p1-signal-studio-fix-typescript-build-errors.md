# TODO-312: Fix TypeScript Build Errors (Remove ignoreBuildErrors)

**Repo:** signal-studio
**Priority:** P1
**Effort:** M (3-6 hours)
**Status:** pending

## Description
`next.config.mjs` has `typescript: { ignoreBuildErrors: true }` which silently swallows all TypeScript errors.
This means bugs ship to production undetected. Must remove this flag and fix all surfaced errors.

## Acceptance Criteria
- `ignoreBuildErrors: true` removed from next.config.mjs
- `pnpm tsc --noEmit` runs with zero errors
- `pnpm build` succeeds
- No type: any shortcuts added to silence errors (fix properly)

## Coding Prompt
```
1. Edit /data/workspace/projects/signal-studio/next.config.mjs:
   Remove lines:
     typescript: {
       ignoreBuildErrors: true,
     },

2. Run type check:
   cd /data/workspace/projects/signal-studio && pnpm tsc --noEmit 2>&1 | head -50

3. For each error:
   - Fix the root cause (add proper types, fix null checks, etc.)
   - Do NOT use `as any` or `// @ts-ignore` unless absolutely necessary
   - Common patterns to fix:
     - Missing return types on API route handlers
     - Untyped Oracle/DB result rows
     - Missing null checks on optional chaining

4. After fixing, verify: pnpm build succeeds
```

## Dependencies
- Should do TODO-311 first (removes reactflow which may have type conflicts)

## Notes
AUDIT.md QUALITY-002
