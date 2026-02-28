Title: 305 — Backend: SQL injection & hardcoded secrets fixes (forwardlane-backend & signal-builder-backend)
Repos: forwardlane-backend, signal-builder-backend
Priority: P0 (Critical)
Owner: Backend security lead
Estimated effort: 1-2 days

Description:
Patch known SQL injection hotspots, remove hardcoded secrets, rotate secrets and add CI scanning that fails on new secrets or risky patterns.

Acceptance criteria:
- No endpoints construct SQL via untrusted f-strings (order_by, EXPLAIN, list_objects)
- All secrets removed from codebase; CI secret-scan passes
- Tests exist asserting parameterized queries for previously vulnerable endpoints

Execution steps / Agent-executable prompt:
1. Run grep for patterns: f"{, format(), + string concat around SQL" and identify hotspots
2. Rewrite vulnerable code to use parameterized queries or ORM-safe APIs
3. Search for hardcoded secrets (API keys, JWT secrets) and move to env vars; update README
4. Add GitHub Action with truffleHog or detect-secrets to fail on secret commits
5. Add unit tests for the fixed endpoints

Verification tests:
- Static scan returns zero hardcoded secrets
- Integration/unit tests for endpoints asserting safe SQL usage

Notes:
- Coordinate secret rotation with ops (do not rotate live secrets without ops coordination)
- Prioritize endpoints marked in TODOs list (EXPLAIN, order_by, write_back)
