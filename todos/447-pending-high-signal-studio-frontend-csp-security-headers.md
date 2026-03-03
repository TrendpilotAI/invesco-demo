# TODO-447: Security Headers — Content Security Policy + CSRF

**Repo:** signal-studio-frontend  
**Priority:** High  
**Effort:** S (4-6 hours)  
**Status:** pending

## Description

The app has no Content Security Policy headers, missing CSRF protection on mutations, and the API URL defaults to localhost. These must be fixed before production launch.

## Coding Prompt

```
In /data/workspace/projects/signal-studio-frontend/next.config.mjs:

Add security headers:
```javascript
const securityHeaders = [
  { key: 'X-DNS-Prefetch-Control', value: 'on' },
  { key: 'Strict-Transport-Security', value: 'max-age=63072000; includeSubDomains; preload' },
  { key: 'X-Frame-Options', value: 'SAMEORIGIN' },
  { key: 'X-Content-Type-Options', value: 'nosniff' },
  { key: 'Referrer-Policy', value: 'origin-when-cross-origin' },
  { key: 'Permissions-Policy', value: 'camera=(), microphone=(), geolocation=()' },
  {
    key: 'Content-Security-Policy',
    value: [
      "default-src 'self'",
      "script-src 'self' 'unsafe-eval' 'unsafe-inline'", // needed for Next.js
      "style-src 'self' 'unsafe-inline'",
      "img-src 'self' data: blob: https:",
      "font-src 'self'",
      "connect-src 'self' https://*.supabase.co wss://*.supabase.co https://api.openai.com https://api.anthropic.com",
      "frame-ancestors 'none'",
    ].join('; ')
  }
]

export default {
  async headers() {
    return [{ source: '/(.*)', headers: securityHeaders }]
  }
}
```

Also:
1. Run `npm audit` and fix any high/critical CVEs
2. Ensure NEXT_PUBLIC_API_URL is set in Railway environment (not localhost)
3. Add `SameSite=Strict` to Supabase auth cookie options in client config
```

## Acceptance Criteria
- [ ] `npm audit` reports 0 high/critical vulnerabilities
- [ ] Security headers present on all routes (verify with curl -I)
- [ ] CSP blocks inline script injection attempts
- [ ] NEXT_PUBLIC_API_URL is not localhost in Railway production deploy
