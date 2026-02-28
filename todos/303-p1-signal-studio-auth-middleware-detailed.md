Title: 303 — Signal Studio: Auth middleware + protect demo endpoints (Critical)
Repo: signal-studio
Priority: P1 (Critical)
Owner: Backend engineer / Honey
Estimated effort: 4–8 hours

Description:
Implement authentication middleware for Next.js / API routes used by Signal Studio and secure all demo endpoints. Support Supabase JWT tokens for production and short-lived demo tokens for dry-runs.

Acceptance criteria:
- All API routes that return sensitive or demo data require a valid auth token
- Demo endpoints reject unauthenticated requests with 401
- Integration test added: unauthenticated request => 401; authenticated => 200
- Rate limiting applied to demo endpoints (configurable)

Execution steps / Agent-executable prompt:
1. Review /data/workspace/projects/signal-studio to find unprotected API routes
2. Add middleware that checks for Supabase JWT or demo token; validate signature/claims
3. Add rate-limiter (e.g., express-rate-limit or edge function) for demo endpoints
4. Add integration tests using Playwright/Supertest to verify protection
5. Open PR with code changes and tests

Verification tests:
- CI runs integration tests and they pass
- Manual smoke test: curl protected endpoint without token => 401

Notes:
- Don't rotate Supabase keys in this task; only validate tokens
- For demo tokens, use short-lived HMAC-signed tokens stored in Vercel env for the demo
