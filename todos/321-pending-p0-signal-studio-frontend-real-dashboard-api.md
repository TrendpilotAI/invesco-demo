# TODO-321: Wire Dashboard to Real API — Signal Studio Frontend

**Priority:** P0  
**Repo:** signal-studio-frontend  
**Effort:** S (2h)  
**Status:** pending  

## Description
Dashboard page (`src/app/(app)/dashboard/page.tsx`) uses hardcoded mock stats (47 signals, 32 active, 156 runs) and fake activity feed. Replace with real TanStack Query API calls.

## Task
1. Add `useDashboardStats(orgId)` hook to `src/lib/api/hooks.ts`
2. Add `useActivityFeed(orgId)` hook
3. Update dashboard page to use hooks with skeleton loading states
4. Get orgId from Zustand app-store

## Coding Prompt (Autonomous Agent)
```
In /data/workspace/projects/signal-studio-frontend:

1. In src/lib/api/hooks.ts, add:
export function useDashboardStats(orgId?: string) {
  return useQuery({
    queryKey: ["dashboard-stats", orgId],
    queryFn: () => apiClient<DashboardStats>(`/dashboard/stats?org_id=${orgId}`),
    enabled: !!orgId,
    staleTime: 30_000,
  });
}

export function useActivityFeed(orgId?: string) {
  return useQuery({
    queryKey: ["activity", orgId],
    queryFn: () => apiClient<ActivityItem[]>(`/activity?org_id=${orgId}&limit=10`),
    enabled: !!orgId,
    staleTime: 15_000,
  });
}

2. In src/app/(app)/dashboard/page.tsx:
- Remove all hardcoded mock data constants
- Import useAppStore from @/lib/stores/app-store, get orgId
- Use useDashboardStats(orgId) and useActivityFeed(orgId)
- Show skeleton cards (animate-pulse bg-muted rounded) while loading
- Show error badge if fetch fails
- Map real DashboardStats fields to the stat cards
```

## Dependencies
- Error boundaries (TODO-322) recommended first

## Acceptance Criteria
- [ ] No hardcoded mock data remains in dashboard
- [ ] Skeleton loaders show during fetch
- [ ] Error state shown on API failure
- [ ] Real stats render when API responds
