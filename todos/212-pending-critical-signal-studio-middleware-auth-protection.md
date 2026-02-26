# 212 · CRITICAL · signal-studio · Add Next.js middleware.ts auth protection for all /api/* routes

## Status
pending

## Priority
critical

## Project
signal-studio (`/data/workspace/projects/signal-studio/`)

## Task Description
Signal Studio currently has **no `middleware.ts`** at the project root. All `/api/*` routes are publicly accessible without authentication. Any unauthenticated caller can hit `/api/oracle/query`, `/api/agent`, `/api/chat/*`, `/api/signals/*`, and every other route handler.

Create a Next.js Edge Middleware that:
1. Intercepts all `/api/*` and protected page routes
2. Validates a session token (JWT or NextAuth session cookie)
3. Returns `401 Unauthorized` for missing/invalid tokens
4. Allows unauthenticated access only to `/api/health`, `/api/oracle/health`, and `/login`
5. Propagates user identity to downstream handlers via request headers

## Dependencies
- None (this is foundational — all other auth fixes depend on this)

## Estimated Effort
3 hours

## Acceptance Criteria
- [ ] `middleware.ts` exists at `/data/workspace/projects/signal-studio/middleware.ts`
- [ ] All `POST /api/*` routes return `401` when called without a valid session
- [ ] `/api/oracle/health` and `/login` remain publicly accessible
- [ ] Unit test in `__tests__/middleware.test.ts` verifies protected/public route matrix
- [ ] No regression on existing passing tests (`pnpm test`)

## Coding Prompt

```
You are working in the Next.js 14 App Router project at /data/workspace/projects/signal-studio/.

TASK: Create middleware.ts to protect all API routes with auth.

### Step 1 — Create /data/workspace/projects/signal-studio/middleware.ts

The project uses NextAuth.js (check package.json for the exact package — likely `next-auth`).
Use `getToken` from `next-auth/jwt` to validate the session cookie.

```typescript
// middleware.ts
import { NextResponse } from "next/server"
import type { NextRequest } from "next/server"
import { getToken } from "next-auth/jwt"

// Routes that are always public (no auth required)
const PUBLIC_PATHS = [
  "/login",
  "/api/auth",           // NextAuth internal routes
  "/api/oracle/health",  // Health check (monitoring)
  "/api/vectorization/health",
]

function isPublicPath(pathname: string): boolean {
  return PUBLIC_PATHS.some(p => pathname.startsWith(p))
}

export async function middleware(req: NextRequest) {
  const { pathname } = req.nextUrl

  // Allow public paths unconditionally
  if (isPublicPath(pathname)) {
    return NextResponse.next()
  }

  // Protect all /api/* routes and all pages except /login
  const isApiRoute = pathname.startsWith("/api/")
  const isPageRoute = !pathname.startsWith("/_next") && !pathname.startsWith("/static")

  if (isApiRoute || isPageRoute) {
    const token = await getToken({
      req,
      secret: process.env.NEXTAUTH_SECRET,
    })

    if (!token) {
      if (isApiRoute) {
        return new NextResponse(
          JSON.stringify({ error: "Unauthorized", message: "Authentication required" }),
          {
            status: 401,
            headers: { "Content-Type": "application/json" },
          }
        )
      }
      // Redirect pages to login
      const loginUrl = new URL("/login", req.url)
      loginUrl.searchParams.set("callbackUrl", req.url)
      return NextResponse.redirect(loginUrl)
    }

    // Propagate user identity to downstream route handlers
    const requestHeaders = new Headers(req.headers)
    requestHeaders.set("x-user-id", token.sub ?? "")
    requestHeaders.set("x-user-email", (token.email as string) ?? "")
    requestHeaders.set("x-user-org", (token.orgId as string) ?? "")

    return NextResponse.next({ request: { headers: requestHeaders } })
  }

  return NextResponse.next()
}

export const config = {
  matcher: [
    // Match all routes except Next.js internals and static files
    "/((?!_next/static|_next/image|favicon.ico|public/).*)",
  ],
}
```

### Step 2 — Verify NEXTAUTH_SECRET is set

Check `.env.local` or `.env.example` for `NEXTAUTH_SECRET`. If missing, add it to `.env.example`:
```
NEXTAUTH_SECRET=your-secret-here-generate-with-openssl-rand-base64-32
```

### Step 3 — Create __tests__/middleware.test.ts

```typescript
import { middleware } from "../middleware"
import { NextRequest } from "next/server"

// Mock next-auth/jwt
jest.mock("next-auth/jwt", () => ({
  getToken: jest.fn(),
}))

import { getToken } from "next-auth/jwt"
const mockGetToken = getToken as jest.Mock

describe("middleware auth protection", () => {
  const makeReq = (pathname: string) =>
    new NextRequest(new URL(`http://localhost${pathname}`))

  beforeEach(() => jest.clearAllMocks())

  test("allows /login without token", async () => {
    mockGetToken.mockResolvedValue(null)
    const res = await middleware(makeReq("/login"))
    expect(res.status).not.toBe(401)
  })

  test("allows /api/oracle/health without token", async () => {
    mockGetToken.mockResolvedValue(null)
    const res = await middleware(makeReq("/api/oracle/health"))
    expect(res.status).not.toBe(401)
  })

  test("blocks /api/oracle/query without token", async () => {
    mockGetToken.mockResolvedValue(null)
    const res = await middleware(makeReq("/api/oracle/query"))
    expect(res.status).toBe(401)
  })

  test("blocks /api/agent without token", async () => {
    mockGetToken.mockResolvedValue(null)
    const res = await middleware(makeReq("/api/agent"))
    expect(res.status).toBe(401)
  })

  test("allows /api/chat with valid token", async () => {
    mockGetToken.mockResolvedValue({ sub: "user-123", email: "test@example.com" })
    const res = await middleware(makeReq("/api/chat/ai-sdk"))
    expect(res.status).not.toBe(401)
  })

  test("propagates x-user-id header with valid token", async () => {
    mockGetToken.mockResolvedValue({ sub: "user-abc", email: "a@b.com" })
    const res = await middleware(makeReq("/api/agent"))
    // NextResponse.next() with modified headers — verify no 401
    expect(res.status).not.toBe(401)
  })
})
```

### Step 4 — Run tests
```bash
cd /data/workspace/projects/signal-studio && pnpm test __tests__/middleware.test.ts
```
```

## Related Files
- `/data/workspace/projects/signal-studio/middleware.ts` (CREATE)
- `/data/workspace/projects/signal-studio/__tests__/middleware.test.ts` (CREATE)
- `/data/workspace/projects/signal-studio/.env.example` (UPDATE)
