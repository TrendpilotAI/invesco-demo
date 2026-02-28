Title: 309 — Signal Studio Frontend: Wire Supabase auth token injection & realtime updates
Repo: signal-studio-frontend
Priority: P1
Owner: Frontend engineer
Estimated effort: 1–2 days

Description:
Ensure the frontend API client includes Supabase JWT for authenticated requests and wire real-time updates for signal run statuses.

Acceptance criteria:
- All API calls include Authorization header with Supabase JWT
- Protected endpoints return 200 in integration tests when token provided
- Real-time signal run updates (websocket/Supabase Realtime) reflected in UI

Execution steps / Agent-executable prompt:
1. Inspect API client and add token injection logic (use Supabase JS client or fetch wrapper)
2. Add integration tests mocking Supabase JWT flows
3. Wire real-time updates via Supabase Realtime or WebSocket and add UI hook
4. Add smoke tests verifying live update behavior

Verification tests:
- CI integration tests pass
- Manual smoke test shows real-time update in UI

Notes:
- Ensure token refresh logic handles expiry
