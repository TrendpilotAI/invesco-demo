# TODO-349: Security Headers (CSP + HSTS)

**Repo:** signal-studio-frontend  
**Priority:** P1  
**Effort:** S (1-2 hours)  
**Dependencies:** none

## Description
No security headers configured. Add CSP, HSTS, X-Frame-Options, and other security headers via next.config.ts.

## Coding Prompt
```
In /data/workspace/projects/signal-studio-frontend/next.config.ts:

Add headers() async function returning security headers for all routes:

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
      "script-src 'self' 'unsafe-eval' 'unsafe-inline'",  // Next.js requires these
      "style-src 'self' 'unsafe-inline'",
      "img-src 'self' data: https:",
      "font-src 'self'",
      `connect-src 'self' ${process.env.NEXT_PUBLIC_SUPABASE_URL} ${process.env.NEXT_PUBLIC_API_URL}`,
      "frame-ancestors 'none'",
    ].join('; ')
  }
];

Also:
- Ensure NEXT_PUBLIC_SUPABASE_ANON_KEY only contains the anon key (never service_role)
- Add .env.example with documented env vars (no real values)
- Ensure .gitignore includes .env.local
```

## Acceptance Criteria
- [ ] Security headers present in prod build (verify with securityheaders.com)
- [ ] CSP does not break app functionality
- [ ] .env.example committed with placeholder values
- [ ] No secrets in .env.local committed to git
