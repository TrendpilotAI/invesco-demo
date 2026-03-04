# TODO-459: Streaming LLM Responses via SSE

**Priority:** HIGH  
**Repo:** forwardlane-backend  
**Effort:** M (4-8 hours)  
**Dependencies:** TODO-458 (shared LLM client)

## Description
MeetingPrepView currently blocks until full LLM response returns (can be 5-15s). Add Server-Sent Events (SSE) streaming so the frontend receives tokens as they generate. Massive UX improvement for enterprise demos.

## Coding Prompt
```
In /data/workspace/projects/forwardlane-backend/:

1. Add SSE support to MeetingPrepView:
   - New endpoint: GET /api/v1/meeting-prep/<client_id>/stream/
   - Use Django StreamingHttpResponse with content_type='text/event-stream'
   - Stream Gemini response chunks as SSE events: data: {chunk}\n\n
   - Include heartbeat events every 5s to keep connection alive
   - Add Cache-Control: no-cache header

2. Update ai/llm_client.py to support streaming mode:
   - complete_stream(prompt) -> Generator[str, None, None]
   - Use Gemini streaming API (generate_content with stream=True)
   - Kimi streaming fallback if Gemini fails

3. Add authentication check on streaming endpoint (same as existing MeetingPrepView)

4. Add test: test streaming response returns SSE format headers and data chunks

5. Document the SSE event format in API docs

6. Commit: "feat: streaming LLM responses via SSE for MeetingPrep endpoint"
```

## Acceptance Criteria
- [ ] `/meeting-prep/<id>/stream/` returns SSE stream
- [ ] Frontend can consume with EventSource API
- [ ] Fallback to Kimi if Gemini streaming fails
- [ ] Auth enforced on streaming endpoint
