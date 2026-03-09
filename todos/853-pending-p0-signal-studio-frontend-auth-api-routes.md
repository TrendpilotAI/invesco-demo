# Audit & Fix Auth in All API Routes

**Repo:** signal-studio-frontend  
**Priority:** P0  
**Effort:** M (2-3 hours)

## Description
Multiple API routes in `app/api/oracle/` and `app/api/signals/` may not validate user sessions before executing queries. Unauthenticated users could access Oracle DB or manipulate signals.

## Coding Prompt
```
In /data/workspace/projects/signal-studio-frontend/app/api/:
1. List all route.ts files: find app/api -name "route.ts"
2. For each file, check if it imports createClient from @/lib/supabase/ and calls getUser()
3. For any route missing auth:
   a. Import: import { createClient } from '@/lib/supabase/server'
   b. Add at top of handler:
      const supabase = createClient()
      const { data: { user }, error } = await supabase.auth.getUser()
      if (!user || error) {
        return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
      }
4. Create lib/auth/require-auth.ts helper to DRY this up
5. Run pnpm test:ci to verify no regressions
6. Commit with message: "security: enforce auth on all API routes"
```

## Acceptance Criteria
- [ ] All `app/api/` routes validate user session
- [ ] `require-auth.ts` helper created
- [ ] Tests pass

## Dependencies
None
