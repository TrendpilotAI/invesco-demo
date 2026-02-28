# TODO-221: Auth Token Injection into API Client

**Repo:** signal-studio-frontend  
**Priority:** P0 (Critical — all API calls currently unauthenticated)  
**Effort:** S (2-4 hours)  
**Status:** pending

## Problem
`/src/lib/api/client.ts` `apiClient` function never sends the Supabase JWT. Every API call to the Django backend is unauthenticated. The backend is presumably rejecting or ignoring auth — this is a security and correctness bug.

## Acceptance Criteria
- Every `apiClient` call includes `Authorization: Bearer <supabase-access-token>`
- Token is refreshed automatically (Supabase handles this via `@supabase/ssr`)
- If user is not logged in, throw an auth error before making the API call
- No regression in existing functionality

## Coding Prompt

```
File: /data/workspace/projects/signal-studio-frontend/src/lib/api/client.ts

Current apiClient does not inject auth token. Modify it to:

1. Import createBrowserClient from @supabase/ssr
2. Before making the fetch, call supabase.auth.getSession() to get the access token
3. Inject Authorization: Bearer <token> header
4. If no session exists, throw new Error("Not authenticated")

Also update /src/lib/supabase/client.ts if needed to export a singleton browser client.

The fix should be backwards compatible — options.token override should still work for
cases where a token is explicitly passed.

After fixing, verify by checking Network tab in browser devtools: Authorization header
should appear on all /api/* requests.
```

## Dependencies
None — this is a prerequisite for everything else.
