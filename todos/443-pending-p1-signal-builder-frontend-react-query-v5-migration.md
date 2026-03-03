# TODO-443: Migrate React Query v4 → v5

**Repo:** signal-builder-frontend  
**Priority:** P1  
**Effort:** Medium (3-4 days)  
**Created:** 2026-03-03

## Description

The project uses `@tanstack/react-query@^4.22.0`. React Query v5 (TanStack Query v5) brings breaking API changes and major improvements: simplified `useQuery` API, built-in devtools in the package, improved TypeScript inference, and `suspense` mode as first-class.

## Motivation

- v4 is no longer actively maintained for bug fixes
- v5 has improved TypeScript narrowing (no more `data | undefined` confusion)
- `isLoading` vs `isPending` semantic clarity
- Better SSR / streaming support for future use

## Coding Prompt

```
Migrate @tanstack/react-query from v4 to v5 in /data/workspace/projects/signal-builder-frontend/.

Steps:
1. Update package.json: "@tanstack/react-query": "^5.0.0"
2. Run: yarn upgrade @tanstack/react-query @tanstack/react-table
3. Fix breaking changes:
   - Replace `isLoading` with `isPending` for non-cached queries
   - `cacheTime` → `gcTime`
   - `onSuccess/onError/onSettled` callbacks removed from useQuery — move to useEffect or mutation callbacks
   - `useQuery({ queryKey, queryFn, onSuccess })` → remove onSuccess, handle in component
4. Add @tanstack/react-query-devtools to devDependencies
5. Add QueryClient devtools in development mode in App.tsx
6. Run: yarn typecheck && yarn test
7. Document migration in CHANGELOG.md
```

## Acceptance Criteria

- [ ] All `useQuery` / `useMutation` calls compile without type errors
- [ ] No `onSuccess`/`onError` in query options (moved to effects)
- [ ] DevTools visible in dev mode
- [ ] `yarn test` passes
- [ ] `yarn typecheck` passes

## Dependencies

- None (standalone upgrade)
