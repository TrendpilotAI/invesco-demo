# TODO-478: Axios Token Refresh Interceptor

**Project:** signal-builder-frontend
**Priority:** P1 (MEDIUM impact, S effort)
**Estimated Effort:** 2-3 hours
**Dependencies:** None

## Description

Auth interceptor injects Bearer token but has no refresh logic. If token expires mid-session, users get silent 401 failures. Implement axios response interceptor: on 401 → attempt token refresh → retry original request.

## Coding Prompt

```
You are working on signal-builder-frontend at /data/workspace/projects/signal-builder-frontend/.

TASK: Add token refresh logic to axios interceptor.

STEPS:
1. Read src/shared/lib/getAxiosInstance.ts and src/shared/lib/auth.ts to understand current auth flow
2. Read src/redux/auth/ to understand token storage

3. Add response interceptor to the axios instance:
   - On 401 response:
     a. Check if already refreshing (prevent infinite loop with a flag)
     b. Call refresh token endpoint (check backend API for refresh route)
     c. On success: update stored token, retry original request
     d. On failure: clear auth state, redirect to login
   - Queue concurrent requests during refresh (don't fire multiple refreshes)

4. Implementation pattern:
   let isRefreshing = false;
   let failedQueue: Array<{resolve, reject}> = [];

   axiosInstance.interceptors.response.use(
     (response) => response,
     async (error) => {
       const originalRequest = error.config;
       if (error.response?.status === 401 && !originalRequest._retry) {
         if (isRefreshing) {
           return new Promise((resolve, reject) => {
             failedQueue.push({ resolve, reject });
           });
         }
         originalRequest._retry = true;
         isRefreshing = true;
         try {
           const newToken = await refreshToken();
           // update stored token
           // process queued requests
           return axiosInstance(originalRequest);
         } catch {
           // clear auth, redirect to login
         } finally {
           isRefreshing = false;
         }
       }
       return Promise.reject(error);
     }
   );

5. Run: pnpm typecheck && pnpm test

CONSTRAINTS:
- Must handle concurrent 401s (queue pattern, not multiple refresh calls)
- Must prevent infinite retry loops
- Must redirect to login on refresh failure
- Must work with existing Redux auth state
```

## Acceptance Criteria
- [ ] 401 responses trigger automatic token refresh
- [ ] Concurrent 401s queued (single refresh call)
- [ ] Failed refresh redirects to login
- [ ] No infinite retry loops
- [ ] `pnpm typecheck` passes
