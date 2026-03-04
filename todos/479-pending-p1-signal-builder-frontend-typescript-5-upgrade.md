# TODO-479: TypeScript 4.4 → 5.x Upgrade

**Project:** signal-builder-frontend
**Priority:** P1 (MEDIUM impact, S effort)
**Estimated Effort:** 2-3 hours
**Dependencies:** None

## Description

TypeScript 4.4.2 is outdated. Upgrade to 5.x for satisfies operator, const type params, improved inference, and better performance.

## Coding Prompt

```
You are working on signal-builder-frontend at /data/workspace/projects/signal-builder-frontend/.

TASK: Upgrade TypeScript from 4.4.2 to 5.x.

STEPS:
1. pnpm add -D typescript@~5.5
2. Also upgrade related packages:
   pnpm add -D @typescript-eslint/parser@^7 @typescript-eslint/eslint-plugin@^7
3. Run: pnpm typecheck — fix any new errors (TS 5.x is stricter on some patterns)
4. Common issues to watch:
   - `import type` may be enforced differently
   - Some generic inference changes
   - `moduleResolution: "bundler"` is already set (good)
5. Run: pnpm lint && pnpm test
6. Update tsconfig.json target if beneficial (es6 → es2020 for modern browser targets)

CONSTRAINTS:
- Fix all type errors introduced by upgrade
- Do not suppress with @ts-ignore (fix properly)
- Keep strict: true
```

## Acceptance Criteria
- [ ] TypeScript ≥5.5 in package.json
- [ ] `pnpm typecheck` passes with zero errors
- [ ] `pnpm lint` passes
- [ ] `pnpm test` passes
- [ ] @typescript-eslint packages updated to compatible versions
