---
status: pending
priority: P1
issue_id: "012"
tags: [flip-my-era, refactor, dead-code, creator, creators]
dependencies: []
---

# 012 — Consolidate Duplicate creator/ vs creators/ Modules

## Overview

FlipMyEra has two nearly-identical module directories:
- `src/modules/creator/` — contains `CreatorAnalytics.tsx`, `CreatorProfile.tsx`, `FeaturedCreators.tsx`, `VerificationBadge.tsx`, `index.ts`
- `src/modules/creators/` — contains `CreatorAnalytics.tsx`, `CreatorBadges.tsx`, `CreatorProfile.tsx`, `FeaturedCreators.tsx`, `TipJar.tsx`, `index.ts`, `types.ts`, plus tests in `__tests__/`

This duplication causes confusion about the canonical module, wastes bundle size, and makes maintenance harder. The `creators/` module is more complete (has types, tests, and `TipJar`/`CreatorBadges`). The `creator/` module has `VerificationBadge.tsx` which may not exist in `creators/`.

**Why P1:** This is a code quality and maintainability issue. Double-maintaining two modules means bugs get fixed in one but not the other. Every developer touching creator features wastes time figuring out which module to use.

## Coding Prompt

You are working on FlipMyEra, a React 18 + TypeScript + Supabase SaaS app at `/data/workspace/projects/flip-my-era/`.

**Task:** Consolidate the duplicate `src/modules/creator/` and `src/modules/creators/` into a single canonical module.

### Step 1 — Audit both modules

Read every file in both modules:
- `src/modules/creator/*.tsx` and `src/modules/creator/index.ts`
- `src/modules/creators/*.tsx`, `src/modules/creators/types.ts`, `src/modules/creators/index.ts`
- `src/modules/creators/__tests__/*.test.tsx`

Document the differences:
- What does `creator/VerificationBadge.tsx` do that `creators/` doesn't have?
- Are the `CreatorProfile.tsx` files identical or do they have different implementations?
- What does `creators/TipJar.tsx` do?

### Step 2 — Find all imports

Run:
```bash
grep -r "from.*modules/creator[^s]" src/ --include="*.ts" --include="*.tsx"
grep -r "from.*modules/creators" src/ --include="*.ts" --include="*.tsx"
```

Also check routes in `src/app/App.tsx`.

### Step 3 — Merge into creators/

The canonical module is `src/modules/creators/` (more complete, has tests). 

1. Move `creator/VerificationBadge.tsx` to `creators/VerificationBadge.tsx` if it doesn't already exist there.
2. Compare any differing implementations of shared files — keep the more complete/tested version.
3. Add any missing exports to `src/modules/creators/index.ts`.

### Step 4 — Update all imports

Update every import that references `@/modules/creator` (without `s`) to `@/modules/creators`.

### Step 5 — Delete creator/ module

```bash
rm -rf src/modules/creator/
```

### Step 6 — Verify

```bash
npm run typecheck
npm run test:ci
npm run build
```

All three must pass with zero errors. If any import fails, fix it before removing the old module.

### Step 7 — Also audit affiliates/ module

While you're cleaning up, check `src/modules/affiliates/`:
- Read `src/modules/affiliates/AffiliateSystem.tsx` — is this a working feature or aspirational UI?
- Check `src/app/App.tsx` — is there a route to the affiliates page?
- If it's purely aspirational with no backend and no route, add a comment at the top of the file: `// TODO: This module is aspirational — not yet connected to backend`
- Do NOT delete it — just document its status.

## Dependencies

None.

## Effort

S (2-4 hours)

## Acceptance Criteria

- [ ] `src/modules/creator/` directory deleted
- [ ] All functionality from `creator/` preserved in `src/modules/creators/`
- [ ] All imports updated from `@/modules/creator` to `@/modules/creators`
- [ ] `npm run typecheck` — zero errors
- [ ] `npm run test:ci` — all tests pass
- [ ] `npm run build` — successful build
- [ ] `affiliates/` module status documented with comment
