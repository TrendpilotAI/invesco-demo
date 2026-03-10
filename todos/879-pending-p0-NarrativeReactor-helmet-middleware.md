# TODO-879: Add helmet Security Headers Middleware

**Repo**: NarrativeReactor  
**Priority**: P0 — Security  
**Effort**: 30 minutes  
**Status**: Pending  

## Problem

`src/index.ts` has no security headers middleware. Missing:
- Content-Security-Policy (XSS protection for dashboard)
- Strict-Transport-Security (force HTTPS)
- X-Frame-Options (clickjacking protection)
- X-Content-Type-Options (MIME sniffing protection)
- Referrer-Policy

## Solution

```bash
npm install helmet
npm install -D @types/helmet
```

```typescript
// src/index.ts — add after imports, before CORS:
import helmet from 'helmet';

app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'", "'unsafe-inline'"],  // Allow inline for dashboard
      styleSrc: ["'self'", "'unsafe-inline'"],
      imgSrc: ["'self'", "data:", "https:"],
      connectSrc: ["'self'"],
      fontSrc: ["'self'"],
      objectSrc: ["'none'"],
      mediaSrc: ["'self'"],
      frameSrc: ["'none'"],
    },
  },
  hsts: {
    maxAge: 31536000,  // 1 year
    includeSubDomains: true,
    preload: true,
  },
}));
```

## Files to Change

- `src/index.ts` — add `import helmet from 'helmet'` and `app.use(helmet(...))`
- `package.json` — add `helmet` to dependencies

## Acceptance Criteria

- [ ] `helmet` middleware applied before all routes in `src/index.ts`
- [ ] CSP configured to allow dashboard inline scripts
- [ ] HSTS enabled for production
- [ ] Tests still passing (helmet doesn't break API response tests)
- [ ] Security headers visible in `/health` response headers
