# TODO-597: JWT Session Expiry — NarrativeReactor

**Priority:** P0 (Security Critical)
**Repo:** NarrativeReactor
**Effort:** 30 minutes
**Dependencies:** None

## Problem
JWT tokens signed in `src/lib/jwt.ts` have no `exp` (expiry) claim. Stolen session tokens are valid indefinitely.

## Task
Add `expiresIn: '8h'` to the `jwt.sign()` call in `src/lib/jwt.ts`. Verify that `verifyJwt()` correctly rejects expired tokens. Update any tests that check JWT payload.

## Acceptance Criteria
- [ ] JWT tokens include `exp` claim set to 8 hours from issue time
- [ ] `verifyJwt()` returns null/throws for expired tokens
- [ ] Existing JWT tests pass
- [ ] New test: expired token returns 401 on dashboard route

## Agent Prompt
```
In /data/workspace/projects/NarrativeReactor/src/lib/jwt.ts:
1. Find the jwt.sign() call
2. Add expiresIn: '8h' to the options object
3. Verify verifyJwt() uses jwt.verify() which auto-checks exp
4. Update src/__tests__/middleware/dashboardAuth.test.ts to add a test for expired token rejection
5. Run: cd /data/workspace/projects/NarrativeReactor && npm test -- --testPathPattern=dashboardAuth
```
