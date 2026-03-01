# TODO-345: Supabase Realtime Subscriptions

**Repo:** signal-studio-frontend  
**Priority:** P2  
**Effort:** M (3-5 hours)  
**Dependencies:** TODO-340

## Description
Dashboard and signal run views should update live without polling. Use Supabase Realtime to subscribe to relevant table changes.

## Coding Prompt
```
In /data/workspace/projects/signal-studio-frontend/:

1. Create src/lib/realtime/useRealtimeSignals.ts:
   - Subscribe to supabase.channel('signals').on('postgres_changes', ...)
   - On INSERT/UPDATE/DELETE: invalidate React Query cache for ['signals', orgId]
   - Cleanup subscription on unmount

2. Create src/lib/realtime/useRealtimeSignalRun.ts:
   - Subscribe to signal_runs changes for a specific signal_id
   - On status change: invalidate ['signal-runs', signalId]
   - Used in signal builder/detail page to show live run status

3. Create src/lib/realtime/useRealtimeActivity.ts:
   - Subscribe to activity_feed table
   - Append new items to dashboard activity list

4. Add feature flag: NEXT_PUBLIC_ENABLE_REALTIME=true/false
   - Default false until tested

5. Add connection status indicator in topbar (green dot = connected, grey = polling)
```

## Acceptance Criteria
- [ ] Dashboard activity updates live
- [ ] Signal status updates in list without refresh
- [ ] Signal run status updates live in builder
- [ ] Graceful fallback if Realtime disconnects
