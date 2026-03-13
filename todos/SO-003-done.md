# SO-003 — Rate Limiting & Abuse Prevention ✅

**Completed:** 2026-03-13
**Commit:** a4c2c50 (main branch, TrendpilotAI/Second-Opinion)

## What Was Implemented

### Firestore-Based Per-User Rate Limiting
- **File:** `functions/src/utils/rateLimiter.ts`
- Uses Firestore atomic transactions to count calls per user per minute
- Two tiers:
  - `analysis` → **10 calls/minute** (heavy AI endpoints)
  - `standard` → **30 calls/minute** (lighter endpoints)
- When exceeded: throws `HttpsError('resource-exhausted')` → HTTP 429
- Error includes `retryAfter` seconds in the details payload
- Fails **open** (not closed) if Firestore is unavailable — to avoid blocking legitimate users
- Rate limit docs expire after 5 minutes (TTL via `expiresAt` field)

### Functions Protected
| Function | Tier |
|---|---|
| `analyzeCase` | analysis (10/min) |
| `runAgenticPipeline` | analysis (10/min) |
| `startOpinionSynthesis` | analysis (10/min) |
| `synthesizeDoctorOpinion` | analysis (10/min) |
| `uploadFileToGemini` | standard (30/min) |
| `chatWithPatient` | standard (30/min) |

### Firestore Rules
- Added `_rateLimits/{document=**}` collection — admin SDK only, no client access

## Environment Variables Required
None (uses admin SDK / Firestore internally)

## Firestore Collections Created
- `_rateLimits/{userId}/{tier}/{YYYY-MM-DDTHH:mm}` — auto-expiring minute buckets

## Notes
- Firebase App Check was considered as an alternative but Firestore counters were chosen as simpler and immediately deployable without App Check enrollment
- Rate limit TTL cleanup: old documents expire naturally; a Firestore TTL policy on `expiresAt` field is recommended for production cleanup
