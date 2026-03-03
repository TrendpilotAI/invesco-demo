# TODO 431 — Wire ForwardLane Integration in NarrativeReactor

**Priority:** HIGH  
**Repo:** NarrativeReactor  
**Effort:** 1-2 days  
**Status:** pending

## Description
`src/services/trendpilotBridge.ts` exists as a bridge service but needs to be connected to the actual ForwardLane API to pull client/prospect data for AI-powered personalized content generation.

## Task

1. **Audit trendpilotBridge.ts** — document current stub methods and expected interface
2. **Connect to ForwardLane API** — implement real HTTP calls to ForwardLane's data API
   - Client/prospect data pull
   - Financial advisor persona data
   - Market context signals
3. **Content personalization** — pass ForwardLane data context into Genkit content generation flows
4. **Add env vars** to `.env.example`:
   - `FORWARDLANE_API_KEY`
   - `FORWARDLANE_BASE_URL`
5. **Add tests** for the bridge with mocked API responses

## Coding Prompt for Autonomous Agent
```
Read /data/workspace/projects/NarrativeReactor/src/services/trendpilotBridge.ts
Understand the current interface and stub methods.
Connect it to ForwardLane's API (check ForwardLane docs or ask Nathan for API details).
Extend content-generation.ts flow to accept optional `clientContext` from ForwardLane.
Add FORWARDLANE_API_KEY and FORWARDLANE_BASE_URL to src/lib/env.ts validation.
Write tests in tests/trendpilotBridge.test.ts with mocked HTTP responses.
```

## Acceptance Criteria
- [ ] trendpilotBridge.ts makes real API calls to ForwardLane
- [ ] Content generation accepts ForwardLane context
- [ ] Tests pass with mocked responses
- [ ] .env.example updated with new vars

## Dependencies
- Requires ForwardLane API credentials from Nathan
