# TODO-224: Error Boundaries + Loading States

**Repo:** signal-studio-frontend  
**Priority:** P1  
**Effort:** S (4-6 hours)  
**Status:** pending

## Problem
Most pages have no error UI when queries fail, and limited loading states beyond some skeleton loaders.

## Acceptance Criteria
- Global error boundary wraps (app) layout
- Each data-fetching page shows: loading skeleton, error state with retry, empty state
- No white screen of death on API failure

## Coding Prompt

```
1. Create /src/components/error-boundary.tsx — React class ErrorBoundary component
   that shows a friendly error UI with a retry button

2. Wrap the app layout in /src/app/(app)/layout.tsx with ErrorBoundary

3. Create /src/components/ui/query-states.tsx with:
   - <QueryLoading /> — skeleton placeholder (use existing Skeleton or div with animate-pulse)
   - <QueryError error={Error} onRetry={() => void} /> — error card with retry
   - <QueryEmpty message={string} /> — empty state with illustration

4. Audit all pages that use useQuery hooks and add:
   if (isLoading) return <QueryLoading />
   if (error) return <QueryError error={error} onRetry={refetch} />
   if (!data?.length) return <QueryEmpty message="..." />

Pages to audit: dashboard, signals, signals/[id], templates, chat, admin, settings
```

## Dependencies
None
