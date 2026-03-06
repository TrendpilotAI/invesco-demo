# TODO-587: SSE Streaming for Large Signal Preview

**Repo:** signal-builder-backend
**Priority:** P2 (Medium)
**Effort:** M (Medium, ~4-6h)
**Status:** pending
**Created:** 2026-03-06

## Description

Signal preview currently returns full result sets synchronously. Large datasets cause timeouts and block the connection. Replace with Server-Sent Events (SSE) streaming so the frontend can show progressive results.

## Acceptance Criteria

- [ ] GET /v1/signals/{id}/preview/stream returns `text/event-stream` response
- [ ] Rows are streamed in batches of 100 as SSE events
- [ ] A `done` event is sent when streaming completes, with metadata (total_rows, duration_ms)
- [ ] Error events are sent if query fails mid-stream
- [ ] Existing synchronous preview endpoint is preserved for backward compat

## Coding Prompt

```
In /data/workspace/projects/signal-builder-backend/apps/signals/routers_v1.py:

1. Add a streaming endpoint:
   @router.get("/{signal_id}/preview/stream")
   async def stream_signal_preview(signal_id: int, ...):
       async def event_generator():
           async for batch in signal_case.execute_preview_streaming(signal_id, batch_size=100):
               yield f"data: {json.dumps(batch)}\n\n"
           yield "event: done\ndata: {}\n\n"
       return StreamingResponse(event_generator(), media_type="text/event-stream")

2. In apps/signals/cases/signal.py, add execute_preview_streaming():
   - Use asyncpg cursor for server-side cursor streaming
   - Yield batches of rows as dicts

3. Add tests in tests/test_signal_preview.py for the stream endpoint:
   - Use httpx AsyncClient with stream=True
   - Verify events are emitted, verify done event at end
```

## Dependencies
- None (independent feature)
