# TODO-879: Fix Axios Error Interceptor — Use Promise.reject() Not Return Object

**Repo:** signal-builder-frontend  
**Priority:** P1 (Critical)  
**Effort:** XS (1 hour)  
**Status:** pending

## Problem

The Axios response interceptor in `src/shared/lib/getAxiosInstance.ts` returns an error-shaped object `{ error: {...} }` on failure instead of calling `Promise.reject()`. This breaks React Query fundamentally:
- `onError` callbacks never fire
- Error states in components never trigger
- TypeScript generics are bypassed (callers expect `T`, receive `{ error: {...} } | T`)
- Users see no error feedback on failed API calls

## Files to Change

- `src/shared/lib/getAxiosInstance.ts` — response interceptor error handler

## Coding Prompt

```
In src/shared/lib/getAxiosInstance.ts, find the response interceptor error handler:

// Current (WRONG):
(error: AxiosError<any, any>) => {
  handleApiResponseError(error);
  return {
    error: {
      status: error.response?.status,
      data: error.response?.data.detail || error.message,
    },
  };
}

// Replace with (CORRECT):
(error: AxiosError<any, any>) => {
  handleApiResponseError(error);
  return Promise.reject(error);
}

After this change, audit all call sites that pattern-match on `result.error`:
  grep -r "result\.error\|response\.error\|\.error\.status" src/
  
For each call site, update to use try/catch or React Query's error state instead
of manually checking for the error property.

Also verify that handleApiResponseError doesn't need to return a value —
it should just log/display the error, then the Promise.reject propagates up.
```

## Acceptance Criteria
- [ ] `Promise.reject(error)` returned in interceptor (not object)
- [ ] All downstream callers updated to handle rejected promises properly
- [ ] React Query `onError` callbacks now fire on API failures
- [ ] Error toast/notification still displays to user on failure
- [ ] TypeScript compiles without errors after refactor
