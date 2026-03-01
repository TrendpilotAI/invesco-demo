# TODO-340: Axios Token Refresh Interceptor (Silent Re-auth on 401)

**Repo:** signal-builder-frontend  
**Priority:** P1 | **Effort:** S (3h)  
**Status:** pending

## Problem
Auth token injection was fixed (TODO-221) but there's no refresh logic. When a token expires mid-session, all API calls silently fail with 401. User must manually reload.

## Task
1. Add axios response interceptor: on 401, attempt refresh → retry original request
2. Queue concurrent requests during refresh (don't fire multiple refresh requests)
3. On refresh failure → logout user with toast notification

## Coding Prompt
```
In /data/workspace/projects/signal-builder-frontend/src/redux/api.ts (or shared/lib/axios.ts):
1. Add axiosInstance.interceptors.response.use handler for 401 errors
2. Implement: 
   - isRefreshing flag to prevent duplicate refresh calls
   - failedQueue array to hold pending requests
   - Call refresh token endpoint, update stored token, retry queue
   - On refresh failure: clear auth state, redirect to login
3. Use axios-auth-refresh library if preferred (already supports queue pattern)
4. Add MSW handler for refresh endpoint in src/mocks/ for testing
5. Write unit test for refresh interceptor behavior
```

## Acceptance Criteria
- [ ] 401 response triggers token refresh
- [ ] Concurrent requests during refresh are queued and retried
- [ ] Refresh failure logs user out cleanly
- [ ] Unit tests cover the refresh flow
