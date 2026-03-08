# TODO-851: Enable TypeScript Strict Mode

## Repo
signal-studio-frontend

## Priority
P2

## Description
TypeScript strict mode is not fully enabled, allowing unsafe `any` types to slip through. Estimated 30-50 `any` occurrences across the codebase.

## Task
1. Enable `strict: true` in `tsconfig.json`
2. Fix all type errors introduced by strict mode
3. Replace all `any` usages with proper types
4. Add Zod validation schemas to all API routes using `lib/validators/`
5. Add t3-env for runtime environment variable validation

## Acceptance Criteria
- [ ] `tsc --noEmit` passes with zero errors under strict mode
- [ ] No `any` types in lib/ or components/ (eslint rule)
- [ ] All API routes validate input with Zod
- [ ] ENV validation catches missing vars at build time

## Effort
L (3-5 days)
