# TODO-446: Supabase Realtime — Live Signal Run Status

**Repo:** signal-studio-frontend  
**Priority:** High  
**Effort:** M (2-3 days)  
**Status:** pending

## Description

Signal execution status updates currently require page refresh. Implement Supabase Realtime subscriptions to receive live `signal_runs` table changes and update the UI without polling.

## Coding Prompt

```
In /data/workspace/projects/signal-studio-frontend/:

1. Create src/hooks/use-signal-run-status.ts:

```typescript
import { useEffect, useState } from 'react'
import { createClient } from '@/lib/supabase/client'
import type { SignalRun } from '@/lib/types'

export function useSignalRunStatus(signalId: string) {
  const [run, setRun] = useState<SignalRun | null>(null)
  const supabase = createClient()

  useEffect(() => {
    const channel = supabase
      .channel(`signal-run-${signalId}`)
      .on(
        'postgres_changes',
        {
          event: '*',
          schema: 'public',
          table: 'signal_runs',
          filter: `signal_id=eq.${signalId}`,
        },
        (payload) => {
          setRun(payload.new as SignalRun)
        }
      )
      .subscribe()

    return () => { supabase.removeChannel(channel) }
  }, [signalId, supabase])

  return run
}
```

2. Wire into Signal card component — show live status badge (running/completed/failed)
3. Add animated progress indicator when status = 'running'
4. On completion, invalidate TanStack Query cache: queryClient.invalidateQueries(['signal', signalId])
```

## Dependencies
- TODO-445 (API hooks must be wired first)

## Acceptance Criteria
- [ ] Signal run status updates in real-time without page refresh
- [ ] "Running" state shows animated progress indicator
- [ ] "Completed" state shows results preview
- [ ] "Failed" state shows error with retry button
- [ ] Realtime channel is properly cleaned up on unmount
