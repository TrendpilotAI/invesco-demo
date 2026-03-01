# TODO-337: Loading/Error States + Skeleton Components

**Repo:** signal-studio-frontend  
**Priority:** P1  
**Effort:** S (3-5 hours)  
**Dependencies:** none

## Description
Pages that fetch data via React Query have no loading or error UI. Add skeleton loaders and error components.

## Coding Prompt
```
In /data/workspace/projects/signal-studio-frontend/:

1. Create src/components/ui/skeleton.tsx — basic shimmer skeleton component

2. Create src/components/ui/error-state.tsx — error display with retry button:
   props: message, onRetry

3. Create src/components/error-boundary.tsx — React ErrorBoundary class component

4. Add skeleton variants:
   - SkeletonCard — for dashboard stat cards
   - SkeletonRow — for table rows (signals list)
   - SkeletonText — for text content

5. Update src/app/(app)/dashboard/page.tsx:
   - Use useDashboardStats hook instead of mock data
   - Show SkeletonCard x4 while loading
   - Show ErrorState if query errors

6. Update src/app/(app)/signals/page.tsx similarly

7. Wrap app layout with ErrorBoundary
```

## Acceptance Criteria
- [ ] Dashboard shows skeletons while loading
- [ ] Error state shown with retry on fetch failure
- [ ] ErrorBoundary catches unexpected errors gracefully
