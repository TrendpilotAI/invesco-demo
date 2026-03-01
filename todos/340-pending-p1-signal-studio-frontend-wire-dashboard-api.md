# TODO-340: Wire Dashboard to Real API

**Repo:** signal-studio-frontend  
**Priority:** P1  
**Effort:** S (2-3 hours)  
**Dependencies:** TODO-337 (loading/error states)

## Description
Dashboard page uses hardcoded mock stats and activity data. Replace with real `useDashboardStats` hook.

## Coding Prompt
```
In /data/workspace/projects/signal-studio-frontend/src/app/(app)/dashboard/page.tsx:

1. Import useDashboardStats, useAppStore
2. Get currentOrgId from useAppStore
3. Call useDashboardStats(currentOrgId)
4. Replace hardcoded stats array with data from API response:
   - total_signals → "Total Signals"
   - active_signals → "Active Signals"  
   - recent_runs → "Recent Runs"
   - data_health → "Data Health %"
5. Replace hardcoded recentActivity with data.activity
6. Show skeleton cards while loading (from TODO-337)
7. Show error state if query fails

Also update signals/page.tsx:
1. Import useSignals, useAppStore
2. Render signal list from API
3. Add empty state when no signals exist
4. Add "Create Signal" CTA button
```

## Acceptance Criteria
- [ ] Dashboard shows live data when API is available
- [ ] Falls back gracefully to empty/error states
- [ ] orgId is read from Zustand store
