# TODO-444: Implement Token Refresh / Rotation in Axios Interceptor

**Repo:** signal-builder-frontend  
**Priority:** P1  
**Effort:** Small (1 day)  
**Created:** 2026-03-03

## Description

Current `getAxiosInstance.ts` reads a Bearer token from cookie/localStorage but has no refresh logic. When a token expires, users get silent 401s with no retry. Need to add token refresh interceptor with queue-based retry.

## Motivation

- Enterprise advisors (Invesco) need uninterrupted sessions
- Silent 401s cause data not loading without visible error
- JWT expiry is typically 1hr — sessions often last longer

## Coding Prompt

```
Add token refresh logic to /data/workspace/projects/signal-builder-frontend/src/shared/lib/getAxiosInstance.ts

Implementation:
1. Add a refresh token endpoint config (from appConfig.ts or env var: VITE_REFRESH_TOKEN_URL)
2. In the response interceptor, when error.response?.status === 401:
   a. Queue the failed request
   b. Make a POST to refresh endpoint with refresh token (from cookie: forwardlane_refresh_token)
   c. On success: update stored token, retry queued requests
   d. On failure: clear tokens, redirect to login / emit logout event
3. Use a isRefreshing flag + subscribers pattern to prevent multiple simultaneous refresh calls
4. Add unit tests in src/shared/lib/getAxiosInstance.test.ts using msw

Example pattern:
let isRefreshing = false;
let failedQueue: Array<{resolve: Function; reject: Function}> = [];
```

## Acceptance Criteria

- [ ] 401 responses trigger one refresh attempt (not multiple)
- [ ] Failed requests after 401 are retried with new token
- [ ] Double-refresh race condition handled (queue pattern)
- [ ] Failed refresh redirects/emits logout
- [ ] Unit tests cover: happy path, refresh failure, concurrent 401s

## Dependencies

- TODO-364 (token refresh interceptor) — may overlap, check if completed first
