# TODO-495: Add Rate Limiting to AI API Routes — DONE ✅

**Completed:** 2026-03-04
**Commit:** `b9dbd910` on `main` — `feat: add rate limiting to AI API routes (TODO-495)`
**Repo:** https://github.com/TrendpilotAI/signal-studio-platform

---

## What Was Done

### New File: `lib/middleware/rate-limit.ts`
- Uses `lru-cache` (already a project dependency) for in-memory sliding-window rate limiting
- `checkRateLimit(identifier, maxRequests, windowMs)` — core check returning `{ success, limit, remaining, reset }`
- `getIPIdentifier(req)` — extracts IP from `x-forwarded-for` / `x-real-ip`
- `getTokenIdentifier(req)` — extracts user token from `Authorization` header (Bearer/JWT), falls back to IP
- `rateLimit(req, max, windowMs, "ip"|"token")` — convenience wrapper returning `{ blocked, result }`
- `applyRateLimitHeaders(res, result)` — attaches `X-RateLimit-Limit/Remaining/Reset`
- `rateLimitExceededResponse(result)` — builds 429 with `Retry-After` header

### Updated Routes

| Route | Limit | Identifier |
|---|---|---|
| `POST /api/ai/completion` | 20 req/min | Per IP |
| `POST /api/chat/openrouter` | 30 req/min | Per user token |
| `POST /api/agent/research` | 10 req/min | Per user token |
| `POST /api/agent/morning-brief` | 10 req/min | Per user token |

### Response Headers Added
- `X-RateLimit-Limit` — max requests allowed in window
- `X-RateLimit-Remaining` — requests remaining in current window
- `X-RateLimit-Reset` — Unix timestamp (seconds) when window resets
- `Retry-After` — seconds until retry is allowed (only on 429 responses)

### 429 Response Format
```json
{
  "error": "Too Many Requests",
  "message": "Rate limit exceeded. Try again in N second(s).",
  "reset": 1741100000
}
```

## Build Notes
- TypeScript compilation passes cleanly for all modified/new files
- Pre-existing build failure unrelated to this change (`src/lib/api/client.ts` → missing `lib/supabase/client` alias — separate issue)
