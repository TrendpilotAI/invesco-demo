# TODO-834: Auth Hardening

**Repo**: signal-studio-frontend  
**Priority**: P1  
**Effort**: S (1-2 days)  
**Status**: pending

## Description
middleware.ts exempts ALL `/api/` routes from authentication. This is a security hole — signal execution, agent runs, and AI chat are all accessible without auth.

## Coding Prompt
```
1. In middleware.ts, replace blanket /api/ exemption:
   BEFORE: pathname.startsWith('/api/')
   AFTER: pathname.startsWith('/api/auth/') || pathname === '/api/health'

2. Create lib/middleware/auth.ts:
   export function validateAuthToken(request: NextRequest): { userId: string } | null {
     const token = request.cookies.get('auth-token')?.value
     if (!token) return null
     try {
       return jwt.verify(token, process.env.JWT_SECRET!) as { userId: string }
     } catch { return null }
   }

3. In POST /api/auth/login response, set cookie:
   response.cookies.set('auth-token', token, {
     httpOnly: true,
     secure: process.env.NODE_ENV === 'production',
     sameSite: 'strict',
     maxAge: 86400,
     path: '/'
   })

4. Add 401 response helper for unauthorized API requests

5. Write tests in __tests__/api/auth.test.ts:
   - Test: protected routes return 401 without token
   - Test: protected routes return 200 with valid token
   - Test: expired tokens return 401
```

## Acceptance Criteria
- GET /api/signals without auth returns 401
- POST /api/signals/run without auth returns 401
- Login sets httpOnly cookie
- All existing auth tests pass
