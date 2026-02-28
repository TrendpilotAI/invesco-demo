# 239 · P2 · signal-builder-frontend · Nginx Security Headers + Content Security Policy

## Status
pending

## Priority
P2 — Financial SaaS with no CSP headers; XSS attack surface is unmitigated

## Description
The `nginx.conf` likely lacks security headers. A financial application must have Content Security Policy, X-Frame-Options, X-Content-Type-Options, and Referrer-Policy headers to protect users from XSS and clickjacking.

## Coding Prompt

```
Repo: /data/workspace/projects/signal-builder-frontend

Step 1: Read current nginx.conf
cat nginx.conf  (or find it: find . -name "nginx.conf" -not -path "*/node_modules/*")

Step 2: Add security headers to the server block
Add these headers to the `server { ... }` block or the `location / { ... }` block:

```nginx
# Security headers
add_header Content-Security-Policy "default-src 'self'; connect-src 'self' https://*.forwardlane.com https://o*.ingest.sentry.io; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data:; frame-ancestors 'none';" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-Frame-Options "SAMEORIGIN" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Permissions-Policy "camera=(), microphone=(), geolocation=()" always;

# Remove server version from headers
server_tokens off;
```

Note on CSP `connect-src`: Add all API domains the frontend calls:
- The `REACT_APP_API_BASE_URL` domain
- Sentry ingestion URL (if Sentry is added, see TODO 230)
- Any analytics endpoints (Segment, Mixpanel)

Note on `style-src 'unsafe-inline'`: Required if CSS-in-JS or inline styles are used. Audit first:
grep -rn "style=" src/ --include="*.tsx" | wc -l
If minimal, prefer `'nonce-...'` approach; if pervasive, keep `unsafe-inline` for now.

Step 3: Verify cookies are set securely
Find where `js-cookie` sets the auth cookie. Verify:
```typescript
Cookies.set(AUTH_TOKEN_COOKIE_KEY, token, {
  secure: true,          // HTTPS only
  sameSite: 'strict',    // No cross-site sending
  domain: APP_CONFIG.authCookieDomain,
  expires: 7,            // days
});
```
If `httpOnly` is needed, the cookie must be set server-side (cannot be done in JS).

Step 4: Remove auth token from localStorage
In `src/shared/lib/auth.ts`, find `localStorage.setItem(TOKEN_STORAGE_KEY, token)`.
If the cookie approach is the primary mechanism:
1. Remove the localStorage save
2. Remove the localStorage retrieve
3. Update `getToken()` to only read from cookies
4. Add a migration: on app load, if token is in localStorage but not cookie, migrate and clear localStorage

Step 5: Test CSP doesn't break the application
Build: yarn build
Serve locally with the new nginx.conf: docker run -v $(pwd)/build:/usr/share/nginx/html -v $(pwd)/nginx.conf:/etc/nginx/conf.d/default.conf nginx
Open browser DevTools Console and check for CSP violations.
Fix any violations by adding necessary domains to the appropriate CSP directive.

Commit: "security: add CSP and security headers to nginx, secure auth cookie storage"
```

## Dependencies
- 230 (Sentry) — need Sentry DSN domain in CSP connect-src before adding Sentry
- Backend team must verify cookie security settings

## Effort Estimate
S (4–6 hours)

## Acceptance Criteria
- [ ] `nginx.conf` includes all 5 security headers
- [ ] `Content-Security-Policy` header is present and not blocking app functionality
- [ ] `X-Frame-Options: SAMEORIGIN` prevents clickjacking
- [ ] Auth token no longer stored in `localStorage` (cookie-only)
- [ ] Browser DevTools shows no CSP violations when app is running
- [ ] `yarn build` succeeds
