# TODO 426: Add Authentication Middleware to Signal Studio Templates API

**Repo:** signal-studio-templates  
**Priority:** P0 (Critical — blocker for production)  
**Effort:** S (2–4 hours)  
**Status:** pending

## Description

The Express router in `api/templates.ts` has zero authentication. Any caller with network access can list all templates, read SQL, and fire execution requests against live Invesco data. This is a hard blocker for production deployment.

## Acceptance Criteria

- [ ] JWT validation middleware added to all routes in `api/templates.ts`
- [ ] Unauthenticated requests return `401 Unauthorized`
- [ ] Token issuer configurable via environment variable (`JWT_ISSUER`, `JWT_AUDIENCE`)
- [ ] API tests updated to include auth headers in requests
- [ ] README updated with auth setup instructions

## Coding Prompt

```
In /data/workspace/projects/signal-studio-templates/api/templates.ts:

1. Install express-jwt: `pnpm add express-jwt jwks-rsa`
2. Create auth middleware:

import { expressjwt as jwt } from 'express-jwt';
import jwksRsa from 'jwks-rsa';

const checkJwt = jwt({
  secret: jwksRsa.expressJwtSecret({
    cache: true,
    rateLimit: true,
    jwksUri: process.env.JWKS_URI || 'https://auth.forwardlane.com/.well-known/jwks.json',
  }),
  audience: process.env.JWT_AUDIENCE || 'signal-studio-api',
  issuer: process.env.JWT_ISSUER || 'https://auth.forwardlane.com/',
  algorithms: ['RS256'],
});

3. Apply before all routes: router.use(checkJwt);

4. Add error handler for auth failures:
router.use((err, req, res, next) => {
  if (err.name === 'UnauthorizedError') {
    return res.status(401).json({ error: 'Invalid or missing token', code: 'UNAUTHORIZED' });
  }
  next(err);
});

5. Update __tests__/api.test.ts to pass valid mock JWTs.
6. Add .env.example with JWT_ISSUER, JWT_AUDIENCE, JWKS_URI placeholders.
```

## Dependencies

- None (can be done independently)

## Notes

For development/testing, add an `AUTH_DISABLED=true` env override that bypasses JWT validation.
