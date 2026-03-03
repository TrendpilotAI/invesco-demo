# TODO-426 DONE — Auth Middleware for Signal Studio Templates API

**Date:** 2026-03-03
**Commit:** 9af41e8
**Branch:** main
**Repo:** TrendpilotAI/signal-studio-templates

## What was done

1. **Installed dependencies:** `express-jwt`, `jwks-rsa`, `@types/express`
2. **Created** `src/middleware/auth.ts` — JWT middleware using JWKS-RSA (RS256), with `AUTH_DISABLED=true` bypass for dev/test
3. **Wired** auth into `api/templates.ts` — `router.use(authMiddleware)` before all routes, `router.use(authErrorHandler)` at end
4. **Added** `.env.example` with `JWT_ISSUER`, `JWT_AUDIENCE`, `JWKS_URI`, `AUTH_DISABLED`
5. **Updated tests** — added `jest.setup.js` with `AUTH_DISABLED=true` and registered it in `package.json` `jest.setupFiles`
6. All 18 tests pass ✅
7. Pushed to GitHub

## Config

- JWKS URI: `https://auth.forwardlane.com/.well-known/jwks.json`
- Audience: `signal-studio-api`
- Issuer: `https://auth.forwardlane.com/`
- Algorithm: RS256
- Error response: `401 { error: "Invalid or missing token", code: "UNAUTHORIZED" }`
