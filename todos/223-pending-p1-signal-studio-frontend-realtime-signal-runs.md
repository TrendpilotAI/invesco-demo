# TODO-223: Real-Time Signal Run Status

**Repo:** signal-studio-frontend  
**Priority:** P1  
**Effort:** M (1-2 days)  
**Status:** pending

## Problem
Signal runs are fire-and-forget. After clicking "Run", users have no live feedback on status.

## Acceptance Criteria
- After triggering a run, status updates appear in real-time (running → completed/failed)
- Supabase Realtime subscription updates TanStack Query cache
- No polling — push-based updates only

## Coding Prompt

```
In /src/lib/api/hooks.ts, add a useSignalRunRealtime(signalId) hook:

import { useEffect } from 'react'
import { useQueryClient } from '@tanstack/react-query'
import { createBrowserClient } from '@supabase/ssr'

export function useSignalRunRealtime(signalId: string) {
  const qc = useQueryClient()
  useEffect(() => {
    const supabase = createBrowserClient(...)
    const channel = supabase
      .channel(`signal-runs-${signalId}`)
      .on('postgres_changes', {
        event: '*',
        schema: 'public',
        table: 'signal_runs',
        filter: `signal_id=eq.${signalId}`
      }, (payload) => {
        qc.invalidateQueries({ queryKey: ['signal-runs', signalId] })
        // Optionally update cache directly with payload.new
      })
      .subscribe()
    return () => { supabase.removeChannel(channel) }
  }, [signalId, qc])
}

Add this hook to the signal detail page.
Also add a live status badge component that shows running/completed/failed with animation.
```

## Dependencies
- TODO-221 (auth token)
- Supabase must have Realtime enabled on signal_runs table (backend task)
