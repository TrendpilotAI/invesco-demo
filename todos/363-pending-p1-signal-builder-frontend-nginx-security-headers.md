# TODO-339: nginx Security Headers (CSP, HSTS, X-Frame-Options)

**Repo:** signal-builder-frontend  
**Priority:** P1 | **Effort:** XS (1h)  
**Status:** pending

## Problem
Current `nginx.conf` has no security headers. App is vulnerable to XSS, clickjacking, MIME sniffing.

## Task
Add to nginx.conf:
- `Content-Security-Policy` (restrict script/style sources to self + CDN whitelist)
- `X-Frame-Options: DENY`
- `X-Content-Type-Options: nosniff`
- `Strict-Transport-Security: max-age=31536000; includeSubDomains`
- `Referrer-Policy: strict-origin-when-cross-origin`
- `Permissions-Policy: camera=(), microphone=(), geolocation=()`

## Coding Prompt
```
Edit /data/workspace/projects/signal-builder-frontend/nginx.conf
In the server block, add a header block with all recommended security headers.
CSP should allow: self, data: (for SVG icons), the API domain (from env), Sentry CDN.
Test with: curl -I https://your-domain.com | grep -i "x-frame\|content-security\|strict-transport"
```

## Acceptance Criteria
- [ ] All 6 security headers present in nginx.conf
- [ ] CSP does not break the app (ReactFlow SVGs, Sentry SDK work)
- [ ] securityheaders.com score: A or A+
