# TODO: Add Rate Limiting to Cloud Functions

- **Project:** Second-Opinion
- **Priority:** HIGH
- **Status:** pending
- **Category:** Security
- **Effort:** S (half day)
- **Created:** 2026-03-14

## Description
No rate limiting on AI analysis endpoints. Cloud Functions can be abused for expensive API calls (MedGemma, Gemini).

## Action Items
1. Add per-user rate limiting (e.g., 10 analyses/day free tier)
2. Use Firestore counter pattern or in-memory rate limiter
3. Return 429 Too Many Requests when exceeded
4. Log rate limit hits for abuse detection
