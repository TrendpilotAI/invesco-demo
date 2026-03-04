# TODO-477: nginx.conf Security Headers

**Project:** signal-builder-frontend
**Priority:** P0 (HIGH impact, S effort)
**Estimated Effort:** 1-2 hours
**Dependencies:** None

## Description

Current nginx.conf lacks CSP, X-Frame-Options, X-Content-Type-Options, HSTS, and other security headers. Add comprehensive security header block.

## Coding Prompt

```
You are working on signal-builder-frontend at /data/workspace/projects/signal-builder-frontend/.

TASK: Add security headers to nginx.conf.

STEPS:
1. Read nginx.conf

2. Add the following headers inside the server block:

   # Security headers
   add_header X-Frame-Options "SAMEORIGIN" always;
   add_header X-Content-Type-Options "nosniff" always;
   add_header X-XSS-Protection "1; mode=block" always;
   add_header Referrer-Policy "strict-origin-when-cross-origin" always;
   add_header Permissions-Policy "camera=(), microphone=(), geolocation=()" always;
   add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;
   add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval' https://*.sentry.io; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; connect-src 'self' https://*.sentry.io https://django-backend-production-3b94.up.railway.app https://signal-builder-api-production.up.railway.app; font-src 'self' data:; frame-ancestors 'self'" always;

3. Test CSP doesn't break ReactFlow or Sentry:
   - ReactFlow uses inline styles → 'unsafe-inline' in style-src
   - Sentry needs connect-src to *.sentry.io
   - Backend API URLs in connect-src

4. Validate nginx config: nginx -t (in Docker context)

CONSTRAINTS:
- CSP must allow ReactFlow rendering (uses inline styles + SVG)
- CSP must allow Sentry error reporting
- CSP must allow API calls to backend
- Don't break existing functionality
```

## Acceptance Criteria
- [ ] nginx.conf has all 7 security headers
- [ ] CSP allows ReactFlow, Sentry, and backend API
- [ ] `nginx -t` passes (syntax valid)
- [ ] Score B+ or better on securityheaders.com after deploy
