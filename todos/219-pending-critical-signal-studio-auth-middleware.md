# TODO 219 — [CRITICAL] Add Next.js Auth Middleware to Signal Studio

**Repo:** signal-studio  
**Priority:** CRITICAL  
**Effort:** 2 hours  
**Dependencies:** None (prerequisite for all other tasks)

---

## Description

Signal Studio has **no `middleware.ts`** at the project root. This means every API route — including LLM proxies, Oracle SQL execution, and financial data endpoints — is publicly accessible with zero authentication. This must be fixed before any Invesco production use.

## Acceptance Criteria
- [ ] `middleware.ts` exists at `/data/workspace/projects/signal-studio/middleware.ts`
- [ ] All `/api/*` routes except `/api/health` require a valid session token
- [ ] Unauthenticated requests receive `401 Unauthorized`
- [ ] Login page (`/login`) is excluded from middleware protection
- [ ] Existing session/auth flow continues to work

## Coding Prompt

```
Create /data/workspace/projects/signal-studio/middleware.ts:

import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

const PUBLIC_PATHS = ['/login', '/api/health', '/easy-button/embed']

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl
  
  // Allow public paths
  if (PUBLIC_PATHS.some(p => pathname.startsWith(p))) {
    return NextResponse.next()
  }
  
  // Check for auth token (cookie or Authorization header)
  const token = request.cookies.get('auth-token')?.value 
    || request.headers.get('Authorization')?.replace('Bearer ', '')
  
  if (!token) {
    if (pathname.startsWith('/api/')) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }
    return NextResponse.redirect(new URL('/login', request.url))
  }
  
  // TODO: Add JWT verification here
  return NextResponse.next()
}

export const config = {
  matcher: ['/((?!_next/static|_next/image|favicon.ico|public).*)'],
}
```

Also add rate limiting to LLM routes using Upstash Redis or in-memory LRU cache.
```
