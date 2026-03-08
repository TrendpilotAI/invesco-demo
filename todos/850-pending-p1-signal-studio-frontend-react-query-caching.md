# TODO-850: Add React Query Caching Layer

## Repo
signal-studio-frontend

## Priority
P1

## Description
Signal library page fetches data on every render with no caching. Heavy Oracle queries run repeatedly causing poor UX and unnecessary database load.

## Task
1. Install `@tanstack/react-query` if not present
2. Wrap app in `QueryClientProvider` in `app/layout.tsx`
3. Create `lib/query/signals.ts` with typed query hooks (useSignals, useSignal, useCollections)
4. Add stale-while-revalidate with 60s TTL for Oracle data
5. Add optimistic updates for signal weight changes
6. Add cache invalidation on signal mutations

## Acceptance Criteria
- [ ] Signal list loads from cache on subsequent renders
- [ ] Cache invalidates correctly after mutations
- [ ] Loading/error states work correctly
- [ ] No unnecessary Oracle queries on page focus

## Effort
M (2-3 days)
