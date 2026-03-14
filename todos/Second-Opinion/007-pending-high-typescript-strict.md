# TODO: Enable TypeScript Strict Mode + Fix `any` Types

- **Project:** Second-Opinion
- **Priority:** HIGH
- **Status:** pending
- **Category:** Code Quality
- **Effort:** M (1-2 days)
- **Created:** 2026-03-14

## Description
tsconfig.json lacks `strict: true`, `noImplicitAny`, `strictNullChecks`. 11 explicit `any` types found across components. 1 JSX file (ErrorBoundary.jsx) needs TypeScript conversion.

## Action Items
1. Convert `ErrorBoundary.jsx` → `ErrorBoundary.tsx` with proper interfaces
2. Add to tsconfig.json:
   ```json
   "strict": true,
   "noImplicitAny": true,
   "strictNullChecks": true,
   "noUncheckedIndexedAccess": true
   ```
3. Fix all 11 `any` type usages with proper types
4. Extract shared medical data types to `/types/` directory
