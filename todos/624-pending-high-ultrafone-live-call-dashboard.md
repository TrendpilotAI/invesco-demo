# TODO 624 — Live Call Dashboard with WebSocket Streaming

**Repo:** Ultrafone  
**Priority:** HIGH  
**Effort:** 2 days  
**Depends on:** None

## Problem
Frontend dashboard shows static call history. No real-time visibility into active call screening. User can't see what's happening during a call.

## Task
Add WebSocket-based live dashboard panel showing real-time call state and streaming transcript.

## Execution Prompt
```typescript
// frontend/src/components/LiveCallPanel.tsx
// WebSocket connection to /api/ws/live-calls

const LiveCallPanel = () => {
  const [activeCalls, setActiveCalls] = useState([]);
  const ws = useWebSocket(`${WS_BASE_URL}/api/ws/live-calls`);
  
  // Display:
  // - Caller info + suspicion score badge
  // - Live transcript (streaming tokens)
  // - Connect/Block buttons
  // - Real-time status: CONNECTING → SCREENING → DECISION → ENDED
};
```

```python
# backend/api/websockets.py
# Broadcast call events to subscribed frontend clients
# Subscribe to Redis pub/sub channel: call-events:{user_id}
# Forward: call_started, transcript_chunk, screening_result, call_ended
```

## Acceptance Criteria
- [ ] Dashboard shows active calls in real-time
- [ ] Transcript streams word-by-word during AI screening
- [ ] Connect/Block buttons work without page refresh
- [ ] Handles reconnection gracefully
