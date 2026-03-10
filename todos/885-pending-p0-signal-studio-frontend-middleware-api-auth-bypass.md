# TODO-885: Fix Critical Auth Bypass — 32/44 API Routes Unprotected

**Repo:** signal-studio-frontend  
**Priority:** P0 CRITICAL  
**Effort:** M (3-4 hours)  
**Status:** pending  
**Identified:** 2026-03-10 by Judge Agent v2

## Problem

Fresh audit (2026-03-10) confirmed **32 out of 44 API routes have zero authentication**:

1. `middleware.ts` explicitly whitelists ALL `/api/` routes as public:
   ```typescript
   const isPublic =
     pathname.startsWith('/login') ||
     pathname.startsWith('/auth') ||
     pathname.startsWith('/api/') ||  // ← ALL API routes bypass auth
     ...
   ```
2. Individual API route handlers do NOT self-enforce auth (no `getUser()` calls in 32 routes)

### Unprotected Routes (32 confirmed)
```
app/api/visual-builder/chat/route.ts    ← AI chat — unbounded API cost risk
app/api/models/route.ts
app/api/vectorization/health/route.ts
app/api/signals/generate/route.ts
app/api/data-pipeline/route.ts
app/api/oracle/semantic-search/route.ts  ← Oracle DB access
app/api/oracle/query/route.ts            ← Raw SQL queries
app/api/oracle/health/route.ts
app/api/oracle/tables/route.ts           ← Schema metadata
app/api/oracle/vectorize/route.ts        ← Vectorization jobs
app/api/oracle/preview/route.ts
app/api/oracle/test-connection/route.ts
app/api/oracle/columns/route.ts
app/api/schema/route.ts
app/api/data/query/route.ts
app/api/chat/openrouter/stream/route.ts  ← AI chat — unbounded API cost risk
app/api/chat/openrouter/route.ts
app/api/chat/ai-sdk/route.ts
app/api/chat/insights-memory/route.ts
app/api/chat/insights/health/route.ts
... (12 more)
```

### Risk
- Unauthenticated users can query Oracle DB directly
- Unauthenticated users can trigger AI chat (OpenAI/Anthropic cost explosion)
- Unauthenticated users can run vectorization jobs
- Schema/table metadata exposed publicly

## Coding Prompt

```
In /data/workspace/projects/signal-studio-frontend/:

STEP 1: Create lib/auth/require-auth.ts

import { createClient } from '@/lib/supabase/server'
import { NextRequest, NextResponse } from 'next/server'

export interface AuthResult {
  user: { id: string; email?: string } | null
  response: NextResponse | null
}

export async function requireAuth(req: NextRequest): Promise<AuthResult> {
  try {
    const supabase = await createClient()
    const { data: { user }, error } = await supabase.auth.getUser()
    if (!user || error) {
      return {
        user: null,
        response: NextResponse.json(
          { error: 'Unauthorized', message: 'Authentication required' },
          { status: 401 }
        )
      }
    }
    return { user, response: null }
  } catch (err) {
    return {
      user: null,
      response: NextResponse.json(
        { error: 'Unauthorized', message: 'Auth check failed' },
        { status: 401 }
      )
    }
  }
}

STEP 2: Apply requireAuth to all 32 unprotected routes

For each route file identified above, at the top of every GET/POST/PUT/DELETE handler:

const { user, response } = await requireAuth(req)
if (response) return response

STEP 3: Write a test to verify auth is enforced

In __tests__/api/auth-protection.test.ts:
- For each major API route, send a request without auth cookie/header
- Assert 401 response
- This test must PASS in CI to prevent regression

STEP 4: Update middleware.ts to NOT whitelist /api/ routes
Remove the `pathname.startsWith('/api/')` from the isPublic check.
Instead, individual routes self-enforce via requireAuth().
Some routes (like /api/auth/login, /api/health) should remain public —
list them explicitly in middleware if needed.
```

## Acceptance Criteria
- [ ] `lib/auth/require-auth.ts` created and exported
- [ ] All 32 routes updated with `requireAuth()` at top of each handler
- [ ] `__tests__/api/auth-protection.test.ts` added with 401 assertion for each route
- [ ] `/api/` removed from middleware public whitelist
- [ ] `pnpm build` passes with no errors
- [ ] `pnpm test:api` passes

## Dependencies
- Requires Supabase client to be correctly configured (`lib/supabase/server.ts`)
- Must not break `/api/auth/login`, `/api/auth/callback`, `/api/health` (public routes)

## Notes
- Prior TODO 853 (auth API routes) covers similar ground but is less specific about the middleware bypass angle
- Prior TODO 444 (auth middleware) was created when middleware didn't exist yet — now middleware exists but has the wrong approach
- This TODO supersedes both with a precise fix plan
