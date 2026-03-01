# TODO-354: Wire Signal Canvas to Backend Execution (SSE Streaming)

**Priority:** P0
**Effort:** L
**Repo:** signal-studio
**Status:** pending

## Description
The `/signals/canvas` page exists but signal execution (run/compile) isn't connected to real backend results. Users can build signals but can't run them and see live data.

## Coding Prompt
```
In /data/workspace/projects/signal-studio:

1. Create SSE endpoint at app/api/signals/[id]/stream/route.ts:
```typescript
import { NextRequest } from 'next/server'
import { auth } from '@/lib/auth'

export async function GET(req: NextRequest, { params }: { params: { id: string } }) {
  const session = await auth()
  if (!session) return new Response('Unauthorized', { status: 401 })
  
  const stream = new TransformStream()
  const writer = stream.writable.getWriter()
  const encoder = new TextEncoder()
  
  // Forward SSE from Django backend
  const djangoUrl = `${process.env.NEXT_PUBLIC_API_URL}/api/signals/${params.id}/stream/`
  const djangoResponse = await fetch(djangoUrl, {
    headers: { 'Authorization': `Bearer ${session.accessToken}` }
  })
  
  const reader = djangoResponse.body?.getReader()
  if (!reader) {
    await writer.close()
    return new Response(stream.readable, { headers: { 'Content-Type': 'text/event-stream' } })
  }
  
  // Pipe Django SSE to client
  ;(async () => {
    try {
      while (true) {
        const { done, value } = await reader.read()
        if (done) break
        await writer.write(value)
      }
    } finally {
      await writer.close()
    }
  })()
  
  return new Response(stream.readable, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
    }
  })
}
```

2. Create app/api/signals/run/route.ts to trigger signal execution:
   - POST { signal_id, params } → forward to Django /api/signals/run/
   - Return { task_id } for polling or SSE connection

3. In the signal canvas component (/signals/canvas page):
   - Add "Run Signal" button
   - On click: POST to /api/signals/run → get task_id
   - Open SSE connection to /api/signals/{id}/stream
   - Display streaming results in a results panel below the canvas
   - Show loading/running/complete states

4. Add result display: table or chart depending on signal output type

5. Test with a real signal against Oracle 23ai

6. Commit: "feat(canvas): wire signal execution to SSE streaming results"
```

## Dependencies
- TODO-351, TODO-353

## Acceptance Criteria
- Run button visible on signal canvas
- Signal execution streams results in real-time
- Results display as table/chart
- Error states handled gracefully
