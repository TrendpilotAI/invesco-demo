# TODO-006: MEDIUM — Enforce Application-Level Rate Limiting

**Priority:** MEDIUM
**Status:** pending
**Category:** security

## Problem
Rate limiter utility exists (`functions/src/utils/rateLimiter.ts`) and Firestore `_rateLimits` collection is defined in rules, but needs verification that all Cloud Function endpoints consistently apply rate limiting.

## Tasks
- Audit all callable Cloud Functions for rate limit middleware
- Ensure GPU-intensive endpoints (MedGemma inference) have strict per-user limits
- Add rate limit response headers (X-RateLimit-Remaining, Retry-After)

## Files
- `functions/src/utils/rateLimiter.ts`
- `functions/src/index.ts`
