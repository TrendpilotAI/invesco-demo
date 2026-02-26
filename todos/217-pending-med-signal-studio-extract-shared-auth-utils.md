# 217 · MED · signal-studio · Extract shared lib/auth-utils.ts and lib/api-error.ts (DRY fixes)

## Status
pending

## Priority
med

## Project
signal-studio (`/data/workspace/projects/signal-studio/`)

## Task Description
Auth validation and error response construction are duplicated across many route handlers. Each route re-implements:
- Checking for `x-user-id` header
- Constructing JSON error responses
- Logging errors with consistent structure

This creates maintenance burden and increases risk of inconsistent security behavior. Extract into shared utilities.

## Dependencies
- 212 (middleware establishes the `x-user-id` header pattern)
- 213, 214 (both reference the new header pattern)

## Estimated Effort
2 hours

## Acceptance Criteria
- [ ] `lib/auth-utils.ts` exports `requireAuth(req)` that returns `{userId, email, orgId}` or throws
- [ ] `lib/api-error.ts` exports typed error factory functions
- [ ] At least 5 route handlers refactored to use shared utils
- [ ] No duplicate auth-check code in route handlers
- [ ] `__tests__/lib/auth-utils.test.ts` covers all branches

## Coding Prompt

```
You are working in the Next.js 14 App Router project at /data/workspace/projects/signal-studio/.

TASK: Extract shared auth utilities and API error helpers to eliminate DRY violations.

### Step 1 — Create lib/auth-utils.ts

```typescript
// lib/auth-utils.ts
// Shared authentication utilities for API route handlers.
// Middleware (middleware.ts) sets these headers — this util reads them.

import { NextRequest, NextResponse } from "next/server"

export interface AuthUser {
  userId: string
  email: string
  orgId: string
}

export class AuthError extends Error {
  readonly statusCode = 401
  constructor(message = "Authentication required") {
    super(message)
    this.name = "AuthError"
  }
}

/**
 * Extract authenticated user from request headers.
 * Throws AuthError if headers are missing (middleware bypass or misconfiguration).
 * 
 * Usage in route handlers:
 *   const user = requireAuth(req)  // throws if not authed
 *   const user = getAuthUser(req)  // returns null if not authed
 */
export function requireAuth(req: NextRequest): AuthUser {
  const userId = req.headers.get("x-user-id")
  const email = req.headers.get("x-user-email") ?? ""
  const orgId = req.headers.get("x-user-org") ?? ""

  if (!userId) {
    throw new AuthError()
  }

  return { userId, email, orgId }
}

export function getAuthUser(req: NextRequest): AuthUser | null {
  const userId = req.headers.get("x-user-id")
  if (!userId) return null
  return {
    userId,
    email: req.headers.get("x-user-email") ?? "",
    orgId: req.headers.get("x-user-org") ?? "",
  }
}

/**
 * Wrap a route handler with automatic auth checking.
 * Returns 401 if auth fails instead of throwing.
 * 
 * Usage:
 *   export const POST = withAuth(async (req, user) => {
 *     // user is guaranteed non-null here
 *   })
 */
export function withAuth(
  handler: (req: NextRequest, user: AuthUser) => Promise<NextResponse>
) {
  return async (req: NextRequest): Promise<NextResponse> => {
    try {
      const user = requireAuth(req)
      return await handler(req, user)
    } catch (err) {
      if (err instanceof AuthError) {
        return NextResponse.json(
          { error: "Unauthorized", message: err.message },
          { status: 401 }
        )
      }
      throw err
    }
  }
}
```

### Step 2 — Create lib/api-error.ts

```typescript
// lib/api-error.ts
// Typed API error factory functions for consistent error responses.

import { NextResponse } from "next/server"

export type ApiErrorCode =
  | "UNAUTHORIZED"
  | "FORBIDDEN"
  | "NOT_FOUND"
  | "VALIDATION_ERROR"
  | "INTERNAL_ERROR"
  | "RATE_LIMITED"
  | "BAD_REQUEST"

export interface ApiErrorBody {
  error: ApiErrorCode
  message: string
  details?: unknown
}

export function apiError(
  code: ApiErrorCode,
  message: string,
  status: number,
  details?: unknown
): NextResponse<ApiErrorBody> {
  console.error(`[API Error] ${code}: ${message}`, details ?? "")
  return NextResponse.json({ error: code, message, details }, { status })
}

// Convenience factories
export const unauthorized = (msg = "Authentication required") =>
  apiError("UNAUTHORIZED", msg, 401)

export const forbidden = (msg = "You do not have permission to perform this action") =>
  apiError("FORBIDDEN", msg, 403)

export const notFound = (resource: string) =>
  apiError("NOT_FOUND", `${resource} not found`, 404)

export const validationError = (msg: string, details?: unknown) =>
  apiError("VALIDATION_ERROR", msg, 400, details)

export const internalError = (msg = "An internal error occurred", details?: unknown) =>
  apiError("INTERNAL_ERROR", msg, 500, details)

export const badRequest = (msg: string, details?: unknown) =>
  apiError("BAD_REQUEST", msg, 400, details)
```

### Step 3 — Refactor route handlers to use shared utils

Apply to at least these 5 handlers:

**app/api/agent/route.ts:**
```typescript
import { withAuth } from "@/lib/auth-utils"
import { validationError, internalError } from "@/lib/api-error"

export const POST = withAuth(async (req, user) => {
  const body = await req.json()
  if (!body.messages) return validationError("messages is required")
  // ... rest of handler using user.userId, user.orgId
})
```

**app/api/oracle/query/route.ts:**
```typescript
import { requireAuth } from "@/lib/auth-utils"
import { unauthorized, validationError, internalError } from "@/lib/api-error"

export async function POST(req: NextRequest) {
  const user = getAuthUser(req)
  if (!user) return unauthorized()
  // ...
}
```

Repeat for:
- `app/api/oracle/tables/route.ts`
- `app/api/signals/route.ts`
- `app/api/data/query/route.ts`

### Step 4 — Write tests

Create `__tests__/lib/auth-utils.test.ts`:
```typescript
import { requireAuth, getAuthUser, withAuth, AuthError } from "@/lib/auth-utils"
import { NextRequest } from "next/server"

const makeReq = (headers: Record<string, string>) => {
  const req = new NextRequest("http://localhost/api/test")
  Object.entries(headers).forEach(([k, v]) => req.headers.set(k, v))
  return req
}

describe("requireAuth", () => {
  it("returns user when x-user-id header is set", () => {
    const req = makeReq({ "x-user-id": "u123", "x-user-email": "a@b.com" })
    const user = requireAuth(req)
    expect(user.userId).toBe("u123")
    expect(user.email).toBe("a@b.com")
  })

  it("throws AuthError when x-user-id is missing", () => {
    const req = makeReq({})
    expect(() => requireAuth(req)).toThrow(AuthError)
  })
})

describe("withAuth wrapper", () => {
  it("returns 401 when auth headers missing", async () => {
    const handler = withAuth(async (req, user) => {
      return new Response("ok") as any
    })
    const req = makeReq({})
    const res = await handler(req as any)
    expect(res.status).toBe(401)
  })

  it("calls handler with user when authenticated", async () => {
    const mockHandler = jest.fn().mockResolvedValue(new Response("ok"))
    const handler = withAuth(mockHandler)
    const req = makeReq({ "x-user-id": "u123" })
    await handler(req as any)
    expect(mockHandler).toHaveBeenCalledWith(req, expect.objectContaining({ userId: "u123" }))
  })
})
```

### Step 5 — Run tests
```bash
cd /data/workspace/projects/signal-studio && pnpm test __tests__/lib/auth-utils.test.ts
```
```

## Related Files
- `lib/auth-utils.ts` (CREATE)
- `lib/api-error.ts` (CREATE)
- `app/api/agent/route.ts` (REFACTOR)
- `app/api/oracle/query/route.ts` (REFACTOR)
- `app/api/oracle/tables/route.ts` (REFACTOR)
- `app/api/signals/route.ts` (REFACTOR)
- `app/api/data/query/route.ts` (REFACTOR)
- `__tests__/lib/auth-utils.test.ts` (CREATE)
