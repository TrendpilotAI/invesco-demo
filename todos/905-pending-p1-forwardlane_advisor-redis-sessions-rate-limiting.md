# TODO: Migrate to Redis Sessions and Add LLM Endpoint Rate Limiting

## Priority: P1
## Repo: forwardlane_advisor

### Problem
File-based session store does not scale horizontally. No rate limiting on LLM endpoints exposes risk of abuse and cost spikes.

### Action Items
- Replace connect-session-filestore with connect-redis + Redis
- Configure Redis with TTL for session expiry
- Add express-rate-limit middleware to all LLM endpoints (e.g., /api/advisor/chat)
- Set reasonable limits: 10 req/min per user for LLM calls, 60 req/min for general API
- Add Redis health check to app startup

### Impact
- Enables horizontal scaling (Railway multi-instance deployment)
- Prevents LLM cost runaway from abuse
- Required for production readiness

### References
- PLAN.md architecture section
- TODO-573 (redis-sessions)
