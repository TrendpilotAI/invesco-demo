# TODO 627: Trendpilot — Fix SSO Stub Implementations (Security Risk)

**Priority:** P1 — High (security hazard in production)
**Effort:** M (1-2 days per provider)
**Repo:** /data/workspace/projects/Trendpilot/
**Created:** 2026-03-05

## Problem
`src/services/sso/index.ts` contains stub implementations for SAML and OAuth that silently return hardcoded credentials:
- `handleSAMLCallback()` returns `{ email: 'user@example.com', tenantId: 'stub-tenant' }`
- `handleOAuthCallback()` returns similar hardcoded values

In production, anyone hitting the SSO callback endpoint would be authenticated as `user@example.com` with `stub-tenant` access. This is a critical auth bypass.

## Acceptance Criteria
- [ ] SAML/OAuth handlers throw `NotImplementedError` with clear message if real credentials not configured
- [ ] OR: Implement real OAuth 2.0 flow (Google OAuth is simplest starting point)
- [ ] SSO routes return 501 Not Implemented when provider not configured
- [ ] Tests verify stubs are not accessible without proper config

## Coding Prompt
```
Fix /data/workspace/projects/Trendpilot/src/services/sso/index.ts

Immediate fix (prevent silent auth bypass):
1. Replace stub returns with: throw new Error('SSO not implemented. Configure SAML/OAuth provider credentials.')
2. In src/api/index.ts, wrap SSO callback routes in try/catch returning 501

Optional (implement Google OAuth):
1. npm install passport passport-google-oauth20
2. Add GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET to .env.example
3. Implement real OAuth code exchange in handleOAuthCallback
4. Map Google profile email to tenant via TenantStore lookup
```

## Dependencies
None — this is a standalone security fix.
