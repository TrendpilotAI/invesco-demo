# Fix Silent Exception Swallowing in Signal Delete Endpoint

**Repo:** signal-builder-backend  
**Priority:** critical  
**Effort:** S (1-2 hours)  
**Phase:** 0

## Problem
`apps/signals/routers/signal.py:67-70` silently swallows `WebServiceException` when deleting a signal from ForwardLane:

```python
try:
    await ForwardlaneApiService().delete_signal(signal.id)
except WebServiceException:
    # TODO: add errors handling
    pass
```

No logging, no alerting. Orphaned signals in FL backend go unnoticed.

## Task
1. Add `logger.error(...)` call with exception details
2. Decide: should delete fail if FL sync fails, or soft-fail with warning?
3. Return appropriate HTTP response (500 or 207 partial success)
4. Add test case for FL service failure during delete

## Acceptance Criteria
- Exception is logged with signal ID and error details
- Monitoring/Sentry captures the error
- API returns appropriate status (not silent 204 on failure)
- Unit test covers failure path
