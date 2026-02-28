# 316 · NarrativeReactor — CORS & Security Hardening

**Status:** pending  
**Priority:** critical  
**Project:** NarrativeReactor  
**Effort:** ~3h  

---

## Task Description

`src/index.ts` line 22 sets `cors({ origin: '*' })` — a wildcard that allows any website to make credentialed cross-origin requests to the API. This is a significant security risk, especially since the API handles brand data, campaign configs, and social publishing credentials.

This task:
1. Replaces wildcard CORS with an environment-driven allowlist
2. Adds `helmet` for standard HTTP security headers
3. Validates that the `ALLOWED_ORIGINS` env var is set in production
4. Adds CSP headers suitable for the dashboard

## Full Coding Prompt

```
You are working in /data/workspace/projects/NarrativeReactor/.

## Step 1 — Install dependencies
```bash
pnpm add helmet
pnpm add -D @types/helmet
```

## Step 2 — Update src/lib/env.ts
Add `ALLOWED_ORIGINS` to the validated env vars:
- Required in production (NODE_ENV=production)
- Optional in development (default: 'http://localhost:3000,http://localhost:4000')
- Value is a comma-separated list of allowed origins

## Step 3 — Replace wildcard CORS in src/index.ts
Replace:
```typescript
app.use(cors({ origin: '*' }));
```
With:
```typescript
import helmet from 'helmet';

const allowedOrigins = process.env.ALLOWED_ORIGINS
  ? process.env.ALLOWED_ORIGINS.split(',').map(o => o.trim())
  : ['http://localhost:3000', 'http://localhost:4000'];

app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'", "'unsafe-inline'"], // relax for Next.js hydration
      styleSrc: ["'self'", "'unsafe-inline'"],
      imgSrc: ["'self'", "data:", "https:"],
      connectSrc: ["'self'", ...allowedOrigins],
    },
  },
}));

app.use(cors({
  origin: (origin, callback) => {
    // Allow requests with no origin (curl, server-to-server)
    if (!origin) return callback(null, true);
    if (allowedOrigins.includes(origin)) return callback(null, true);
    callback(new Error(`CORS policy: origin ${origin} not allowed`));
  },
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization', 'X-API-Key'],
}));
```

## Step 4 — Update .env.example
Add:
```
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:4000
```

## Step 5 — Add CORS test
Create tests/security/cors.test.ts using supertest:
- Test that an unlisted origin gets a CORS error
- Test that a listed origin gets Access-Control-Allow-Origin header
- Test that no-origin requests (server-to-server) pass through
```

## Dependencies
- None (standalone security fix)

## Acceptance Criteria
- [ ] `cors({ origin: '*' })` no longer appears anywhere in the codebase
- [ ] `ALLOWED_ORIGINS` env var controls allowed origins
- [ ] `helmet` headers present on all API responses (check X-Frame-Options, X-Content-Type-Options)
- [ ] CORS tests pass: blocked origin returns 500/403, allowed origin passes
- [ ] `.env.example` updated
- [ ] `pnpm build && pnpm test` pass
