Title: 308 — Signal Studio Auth: RBAC & rate-limiting on invite/login (Critical)
Repo: signal-studio-auth
Priority: P1 (Critical)
Owner: Auth engineer
Estimated effort: 4–8 hours

Description:
Add role-based access control to invite endpoint, and rate-limit login/signup routes. Harden admin flows and add tests.

Acceptance criteria:
- Invite endpoint requires admin role/claim
- Login/signup rate-limited (e.g., 10 attempts per 10 minutes by IP or user)
- Tests validate RBAC and rate-limiting

Execution steps / Agent-executable prompt:
1. Review auth code and current invite flow
2. Add RBAC check in invite endpoint (requires admin role in JWT claims)
3. Integrate rate-limiter (Redis-backed) for auth endpoints
4. Add tests for RBAC and rate-limiter

Verification tests:
- Unit/integration tests pass in CI
- Manual test: invite endpoint returns 403 for non-admin

Notes:
- Do not remove legacy invite migration flows; add guard checks
