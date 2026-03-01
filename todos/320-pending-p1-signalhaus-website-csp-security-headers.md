# TODO 320 — Add CSP / Security Headers to signalhaus-website

**Priority:** P1 — High  
**Repo:** signalhaus-website  
**Effort:** S (1-2 hours)  
**Dependencies:** None

---

## Description

The site has no Content-Security-Policy, X-Frame-Options, or X-Content-Type-Options headers. The site is live (signalhaus.ai) and lacks basic security headers that modern web apps require.

Also: fix `CONTACT_EMAIL` fallback to personal email (lines 3 of `/api/contact/route.ts`).

---

## Coding Prompt

```
In /data/workspace/projects/signalhaus-website/:

1. Edit `next.config.ts` to add a `headers()` async function returning security headers for all routes:
   - X-Frame-Options: DENY
   - X-Content-Type-Options: nosniff
   - Referrer-Policy: strict-origin-when-cross-origin
   - Permissions-Policy: camera=(), microphone=(), geolocation=()
   - Content-Security-Policy: Allow self, Google Analytics (gtm, ga), Calendly embed, inline styles/scripts for Next.js
     Sample CSP: "default-src 'self'; script-src 'self' 'unsafe-inline' https://www.googletagmanager.com https://www.google-analytics.com https://assets.calendly.com; frame-src https://calendly.com; img-src 'self' data: https:; style-src 'self' 'unsafe-inline'; connect-src 'self' https://www.google-analytics.com"

2. Edit `src/app/api/contact/route.ts` line 3:
   - Remove the `|| "nathan@forwardlane.com"` fallback
   - Add an explicit check alongside RESEND_API_KEY: if (!CONTACT_EMAIL) return 500 with "Mailer not configured"

3. Run `yarn build` to verify no TypeScript errors.
```

---

## Acceptance Criteria
- [ ] `next.config.ts` includes security headers returned by `headers()` function
- [ ] Running `curl -I https://signalhaus.ai` shows `X-Frame-Options: DENY`
- [ ] CSP allows Google Analytics and Calendly without breaking functionality
- [ ] Contact API returns 500 (not route to personal email) if CONTACT_EMAIL env var missing
- [ ] `yarn build` passes
