# TODO-323: Signal Run Status Polling — Signal Studio Frontend

**Priority:** P1  
**Repo:** signal-studio-frontend  
**Effort:** M (4h)  
**Status:** pending  

## Description
Signal runs have `status: "running" | "completed" | "failed"`. Currently no real-time update — user must refresh. Add TanStack Query polling that activates while a run is in progress.

## Coding Prompt (Autonomous Agent)
```
In /data/workspace/projects/signal-studio-frontend/src/lib/api/hooks.ts:

Update useSignalRuns to support polling:
export function useSignalRuns(signalId: string) {
  const { data: runs, ...rest } = useQuery({
    queryKey: ["signal-runs", signalId],
    queryFn: () => apiClient<SignalRun[]>(`/signals/${signalId}/runs`),
    enabled: !!signalId,
  });
  
  // Enable polling when any run is active
  const hasActiveRun = runs?.some(r => r.status === "running") ?? false;
  
  return useQuery({
    queryKey: ["signal-runs", signalId],
    queryFn: () => apiClient<SignalRun[]>(`/signals/${signalId}/runs`),
    enabled: !!signalId,
    refetchInterval: hasActiveRun ? 3000 : false,
    ...rest,
  });
}

In the signal detail page, update run status display:
- "running" → yellow Badge with pulsing dot
- "completed" → green Badge  
- "failed" → red Badge with error message expandable

Add a toast notification when a running signal completes.
```

## Dependencies
- TODO-321 (real API wiring)

## Acceptance Criteria
- [ ] Running signals poll every 3 seconds automatically
- [ ] Polling stops when all runs complete
- [ ] Status badge colors match run state
- [ ] Toast fires on completion
