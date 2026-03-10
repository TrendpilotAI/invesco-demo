# TODO-884: Add nginx Security Headers (CSP, X-Frame-Options, HSTS)

**Repo:** signal-builder-frontend  
**Priority:** P2 (Medium)  
**Effort:** XS (1 hour)  
**Status:** pending

## Problem

`nginx.conf` has no Content Security Policy, X-Frame-Options, X-Content-Type-Options, or HSTS headers. This leaves the app vulnerable to clickjacking and XSS amplification.

## Coding Prompt

```
In /data/workspace/projects/signal-builder-frontend/nginx.conf,
inside the `server {}` block, add these security headers:

    # Security Headers
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob: https:; connect-src 'self' https: wss:; font-src 'self' data:; frame-ancestors 'none';" always;

Note: 'unsafe-inline' and 'unsafe-eval' may be needed for ReactFlow/Vite in production.
Tighten CSP progressively after verifying no violations in browser console.

Also add cache control for static assets:
    location ~* \.(js|css|png|jpg|jpeg|gif|svg|woff|woff2)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
```

## Acceptance Criteria
- [ ] X-Frame-Options: DENY in response headers
- [ ] X-Content-Type-Options: nosniff in response headers
- [ ] Strict-Transport-Security present for HTTPS deployments
- [ ] Content-Security-Policy does not break app functionality
- [ ] No CSP violations in browser console for normal app usage
- [ ] Static asset caching headers set (1 year for hashed assets)
