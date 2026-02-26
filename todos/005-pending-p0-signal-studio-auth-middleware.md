---
status: pending
priority: p0
issue_id: "005"
tags: [signal-studio, security, auth, middleware, nextjs]
dependencies: []
---

# 005 — Signal Studio: Add Authentication Middleware to Protect All API Routes

## Problem Statement

Signal Studio's API routes are currently unprotected. The `lib/auth-context.tsx` stores tokens in
`localStorage` and passes them via `Authorization` headers, but there is no `middleware.ts` file
enforcing auth server-side. Any unauthenticated request can hit `/api/signals`, `/api/oracle/query`,
`/api/chat`, etc. — exposing financial data and AI inference costs to anyone with the URL.

This is a critical security vulnerability for an enterprise financial product serving Invesco.

## Findings

- No `middleware.ts` exists in project root (only vendored copies in node_modules)
- `app/api/signals/route.ts` calls `getAuthHeaders()` but does not reject unauthenticated requests
- `app/api/oracle/query/route.ts` — no auth check found
- `lib/auth-context.tsx` stores token in `localStorage` under `signal-studio-auth-token`
- Django backend validates tokens via `/api/auth/login` which returns a DRF token
- `app/api/auth/login/route.ts` is the one public route that must remain open
- Demo/embed routes (`/easy-button/embed`) may need special token or CORS handling

## Proposed Solutions

### Option A: Next.js Edge Middleware (Recommended)
- `middleware.ts` at project root — runs on Vercel/Railway Edge runtime
- Checks `Authorization: Token <token>` header OR `signal-studio-auth-token` cookie
- Unauthenticated → redirect to `/login` (pages) or 401 JSON (API routes)
- Public routes whitelist: `/api/auth/login`, `/api/oracle/health`, `/login`, `/_next/`
- **Effort:** 3h | **Risk:** Low

### Option B: Per-route auth helper
- `lib/auth-server.ts` helper called at top of every route handler
- Manually added to each route
- **Cons:** Error-prone, easy to miss new routes

### Option C: Django handles auth
- Rely 100% on Django to reject unauthorized requests
- **Cons:** Oracle routes (`/api/oracle/*`) bypass Django; Next.js server-side costs exposed

## Recommended Action

Implement Option A: Next.js Edge middleware with JWT/token validation + whitelist.

## Acceptance Criteria

- [ ] `middleware.ts` exists at project root (`/data/workspace/projects/signal-studio/middleware.ts`)
- [ ] All `/api/*` routes except `/api/auth/login` return `401` without valid token
- [ ] All page routes except `/login` redirect to `/login` without valid session
- [ ] Token extracted from both `Authorization` header and `signal-studio-auth-token` cookie
- [ ] `/api/oracle/health` added to public whitelist (health check)
- [ ] `/easy-button/embed` has separate embed-token validation
- [ ] Existing Playwright e2e tests pass after middleware added (login flow tested)
- [ ] `middleware.ts` has unit test coverage for whitelist and auth logic

## Files to Create/Modify

- `middleware.ts` — NEW: Edge middleware at project root
- `lib/auth-middleware.ts` — NEW: Auth token validation helper
- `app/api/auth/login/route.ts` — verify it returns proper token format
- `app/easy-button/embed/page.tsx` — add embed token param support
- `.env.example` — add `MIDDLEWARE_SECRET` / `JWT_SECRET` vars
- `__tests__/lib/auth-middleware.test.ts` — NEW: unit tests

## Technical Details

```typescript
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

const PUBLIC_PATHS = [
  '/login',
  '/api/auth/login',
  '/api/oracle/health',
  '/api/control-plane/health',
  '/_next/',
  '/favicon.ico',
  '/easy-button/embed',
]

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl
  
  // Allow public paths
  if (PUBLIC_PATHS.some(p => pathname.startsWith(p))) {
    return NextResponse.next()
  }
  
  // Check for token in header or cookie
  const authHeader = request.headers.get('authorization')
  const cookieToken = request.cookies.get('signal-studio-auth-token')?.value
  const token = authHeader?.replace('Token ', '') || cookieToken
  
  if (!token) {
    if (pathname.startsWith('/api/')) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }
    return NextResponse.redirect(new URL('/login', request.url))
  }
  
  return NextResponse.next()
}

export const config = {
  matcher: ['/((?!_next/static|_next/image|favicon.ico).*)'],
}
```

## Estimated Effort

3 hours

## Work Log

### 2026-02-26 — Initial Planning

**By:** Honey Planning Agent

**Actions:**
- Audited all API routes for auth enforcement
- Found zero server-side auth enforcement
- Designed Edge middleware approach with whitelist
