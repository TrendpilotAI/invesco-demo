# TODO-848: Guard TestCredits Page Behind Admin Flag in Production

**Priority:** P1 — Security
**Repo:** flip-my-era
**Effort:** XS (30 min)
**Created:** 2026-03-08 by Judge Agent v2

## Problem

`/test-credits` route is publicly accessible to all users in production, allowing anyone to trigger free credit grants.

## Task

1. Open `src/app/App.tsx`
2. Find the `TestCredits` route registration
3. Wrap in admin check:
   ```tsx
   {isAdmin && <Route path="/test-credits" element={<TestCredits />} />}
   ```
4. Or use feature flag: `{featureFlags.testCredits && ...}`
5. Alternatively: remove the route entirely from production build using `import.meta.env.DEV`

## Acceptance Criteria
- [ ] Non-admin users get 404 on `/test-credits`
- [ ] Admin users can still access it (or it's dev-only)
- [ ] No regression in auth flow
