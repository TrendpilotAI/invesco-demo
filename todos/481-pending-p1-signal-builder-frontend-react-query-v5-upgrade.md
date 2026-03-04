# 481 — Upgrade React Query v4 → v5

**Priority:** P1  
**Repo:** signal-builder-frontend  
**Effort:** Medium (1-2 days)  
**Dependencies:** None

## Task Description
React Query v4 is used throughout, but v5 has significant improvements: unified API, better TypeScript types, removed deprecated APIs, and improved DevTools. Upgrading now prevents accumulating migration debt.

## Coding Prompt
```
Upgrade @tanstack/react-query from v4 to v5 in /data/workspace/projects/signal-builder-frontend/.

1. Update package.json:
   "@tanstack/react-query": "^5.0.0"
   "@tanstack/react-query-devtools": "^5.0.0"

2. Key breaking changes to address:
   - `cacheTime` renamed to `gcTime`
   - `useQuery` status: `isLoading` → `isPending` for initial load
   - `keepPreviousData` → `placeholderData: keepPreviousData` import
   - `onSuccess`/`onError`/`onSettled` callbacks removed from useQuery
   - `QueryClient.invalidateQueries()` now returns a promise

3. Run: grep -r "cacheTime\|isLoading\|keepPreviousData\|onSuccess\|onError" src/ to find all instances

4. Update each file:
   - Replace cacheTime → gcTime
   - Replace isLoading → isPending where appropriate
   - Move side effects from onSuccess to useEffect watching data
   - Update QueryClient configuration in src/app/

5. Add React Query DevTools to dev build:
   import { ReactQueryDevtools } from '@tanstack/react-query-devtools'
   Add <ReactQueryDevtools /> to app root

6. Run yarn typecheck and yarn test to verify no regressions
```

## Acceptance Criteria
- [ ] @tanstack/react-query upgraded to v5
- [ ] All breaking change migrations applied
- [ ] yarn typecheck passes with no new errors
- [ ] All existing tests pass
- [ ] DevTools added in development mode
