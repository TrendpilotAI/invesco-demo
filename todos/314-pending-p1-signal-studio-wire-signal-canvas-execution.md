# TODO-314: Wire Signal Canvas to Backend Execution API

**Repo:** signal-studio
**Priority:** P1
**Effort:** L (1-2 days)
**Status:** pending

## Description
The `/signals/canvas` page was shipped (TODO-222) but signal execution isn't connected.
The "Run Signal" action needs to call `/api/signals/run` → Django backend → Oracle execution → return results.
Currently results are mocked or empty.

## Acceptance Criteria
- Signal canvas "Run" button POSTs to `/api/signals/run` with signal config
- Django backend executes signal SQL against Oracle 23ai
- Results stream back via SSE or polling
- Results render in the canvas results panel
- Error states handled (Oracle connection failure, SQL error, timeout)

## Coding Prompt
```
1. Inspect current canvas implementation:
   cat /data/workspace/projects/signal-studio/app/signals/canvas/page.tsx
   cat /data/workspace/projects/signal-studio/app/api/signals/run/route.ts

2. Check Django backend signal execution endpoint:
   - Django runs at http://Django-Backend.railway.internal:8000
   - Find signal execution endpoint in BFF proxy config

3. Update /app/api/signals/run/route.ts to:
   - Accept { signal_id, params, filters } in POST body
   - Forward to Django: POST http://Django-Backend.railway.internal:8000/api/signals/{id}/execute/
   - Return { status, results, fields, execution_time }

4. Update canvas page to:
   - Add "Run Signal" button with loading state
   - POST to /api/signals/run with current signal config
   - Display results in a data table component
   - Show execution time + row count
   - Handle errors with user-friendly messages

5. Add SSE support (stretch):
   - Create /app/api/signals/[id]/stream/route.ts
   - Use ReadableStream for live result streaming
```

## Dependencies
- Django backend must have signal execution endpoint
- Oracle 23ai credentials must be configured in Railway env

## Notes
PLAN.md Sprint 2 item 5
