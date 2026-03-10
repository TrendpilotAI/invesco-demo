# TODO-880: Remove localStorage Auth Token Fallback (XSS Risk)

**Repo:** signal-builder-frontend  
**Priority:** P1 (High)  
**Effort:** S (half day)  
**Status:** pending

## Problem

`src/shared/lib/getAxiosInstance.ts` falls back to `localStorage.getItem(TOKEN_STORAGE_KEY)` when the auth cookie is absent. localStorage is accessible via JavaScript, making the token vulnerable to XSS attacks. The app should use httpOnly cookies exclusively — these cannot be read by JS.

## Files to Change

- `src/shared/lib/getAxiosInstance.ts` — remove localStorage fallback
- `src/redux/auth/slice.ts` — remove any localStorage token writes
- `src/shared/lib/auth.ts` (if exists) — remove localStorage references

## Coding Prompt

```
In src/shared/lib/getAxiosInstance.ts, find getStoredToken():

// Current (WRONG):
const getStoredToken = (): string | null =>
  Cookies.get(AUTH_TOKEN_COOKIE_KEY) || localStorage.getItem(TOKEN_STORAGE_KEY) || null;

// Replace with (CORRECT — cookie only):
const getStoredToken = (): string | null =>
  Cookies.get(AUTH_TOKEN_COOKIE_KEY) ?? null;

Then:
1. Search for all localStorage references related to auth tokens:
   grep -r "localStorage" src/ | grep -i "token\|auth"
   
2. Remove all token writes to localStorage in auth slice or helpers.

3. In the request interceptor: if getStoredToken() returns null AND the request
   is not to the login/public endpoint, redirect to login page instead of 
   sending unauthenticated request:
   if (!token && !isPublicEndpoint(config.url)) {
     window.location.href = '/login';
     return Promise.reject(new Error('Unauthenticated'));
   }

4. Update .env.schema: remove VITE_DEV_AUTH_EMAIL and VITE_DEV_AUTH_PASSWORD.
   Instead, create an MSW handler for dev auth that sets the cookie locally.
```

## Acceptance Criteria
- [ ] No `localStorage.getItem` calls for auth tokens
- [ ] No `localStorage.setItem` calls for auth tokens
- [ ] Auth cookie (httpOnly) is sole token source
- [ ] Unauthenticated requests redirect to login
- [ ] Dev auth uses MSW mock, not real credentials in env vars
- [ ] No regressions in auth flow
