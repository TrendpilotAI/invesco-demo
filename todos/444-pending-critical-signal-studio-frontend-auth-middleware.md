# TODO-444: Auth Middleware — Protect All App Routes

**Repo:** signal-studio-frontend  
**Priority:** Critical  
**Effort:** XS (2-4 hours)  
**Status:** pending

## Description

Currently, all `/app/*` routes are accessible without authentication. Users can navigate directly to the dashboard, signals, or chat pages without logging in. A Next.js middleware.ts must be added to protect all app routes and redirect unauthenticated users to `/login`.

## Coding Prompt

```
In /data/workspace/projects/signal-studio-frontend/, create middleware.ts at the project root:

```typescript
import { createServerClient } from '@supabase/ssr'
import { NextResponse, type NextRequest } from 'next/server'

export async function middleware(request: NextRequest) {
  let supabaseResponse = NextResponse.next({ request })

  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() { return request.cookies.getAll() },
        setAll(cookiesToSet) {
          cookiesToSet.forEach(({ name, value, options }) =>
            supabaseResponse.cookies.set(name, value, options)
          )
        },
      },
    }
  )

  const { data: { user } } = await supabase.auth.getUser()

  // Redirect unauthenticated users from protected routes
  const isProtectedRoute = !request.nextUrl.pathname.startsWith('/login') &&
    !request.nextUrl.pathname.startsWith('/auth') &&
    !request.nextUrl.pathname.startsWith('/_next') &&
    !request.nextUrl.pathname.startsWith('/api/auth')

  if (!user && isProtectedRoute) {
    const redirectUrl = request.nextUrl.clone()
    redirectUrl.pathname = '/login'
    redirectUrl.searchParams.set('redirectTo', request.nextUrl.pathname)
    return NextResponse.redirect(redirectUrl)
  }

  return supabaseResponse
}

export const config = {
  matcher: ['/((?!_next/static|_next/image|favicon.ico|public).*)'],
}
```

Also handle the redirect back after login in /app/login/page.tsx — read `searchParams.redirectTo` and redirect after successful auth.
```

## Dependencies
- None (Supabase client already configured)

## Acceptance Criteria
- [ ] Navigating to `/` without session redirects to `/login`
- [ ] Navigating to `/signals` without session redirects to `/login?redirectTo=/signals`
- [ ] After login, user is redirected back to the original page
- [ ] API routes are not blocked by middleware
- [ ] `/login` page itself is not blocked
