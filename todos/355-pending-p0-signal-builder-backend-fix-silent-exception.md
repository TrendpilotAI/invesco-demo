# TODO-355: Fix Silent WebServiceException in Signal Delete Endpoint
**Project:** signal-builder-backend  
**Priority:** P0  
**Effort:** XS (2–4 hours)  
**Status:** pending  
**Created:** 2026-03-01

---

## Description

In `apps/signals/routers/signal.py` around lines 67–70, a `WebServiceException` raised during signal deletion from the ForwardLane API is silently swallowed with `pass`. This means deletion failures are invisible — no logging, no error response to the client, no alerting. The signal appears to delete successfully even when the upstream delete fails.

**Current bad code:**
```python
try:
    await ForwardlaneApiService().delete_signal(signal.id)
except WebServiceException:
    # TODO: add errors handling
    pass
```

---

## Full Autonomous Coding Prompt

```
You are working on the signal-builder-backend FastAPI service at /data/workspace/projects/signal-builder-backend/.

TASK: Fix the silent exception swallowing in the signal delete endpoint.

STEP 1 — Read the file:
```
cat -n /data/workspace/projects/signal-builder-backend/apps/signals/routers/signal.py
```
Find the `except WebServiceException: pass` block around lines 67–70.

STEP 2 — Understand the context:
- Is `delete_signal` in ForwardlaneApiService a critical step (should we fail if it fails)?
- Or is it a best-effort notification (signal can be deleted locally even if upstream fails)?
- Check what `WebServiceException` represents: `grep -rn "WebServiceException" apps/ --include="*.py"`
- Check `ForwardlaneApiService.delete_signal` implementation

STEP 3 — Implement the fix based on what you find:

**Option A (Recommended if upstream delete is critical):**
```python
from loguru import logger
from fastapi import HTTPException

try:
    await ForwardlaneApiService().delete_signal(signal.id)
except WebServiceException as exc:
    logger.error(
        f"Failed to delete signal {signal.id} from ForwardLane API: {exc}",
        extra={"signal_id": signal.id, "error": str(exc)}
    )
    raise HTTPException(
        status_code=502,
        detail=f"Signal deleted locally but failed to sync with ForwardLane: {exc}"
    )
```

**Option B (If upstream is best-effort):**
```python
from loguru import logger

try:
    await ForwardlaneApiService().delete_signal(signal.id)
except WebServiceException as exc:
    logger.warning(
        f"Non-critical: failed to notify ForwardLane of signal {signal.id} deletion: {exc}",
        extra={"signal_id": signal.id, "error": str(exc)}
    )
    # Continue — local deletion proceeds regardless
```

STEP 4 — If you choose Option A, also ensure the local DB delete only happens if the upstream call succeeds. Review the endpoint logic — the ordering matters:
- If upstream delete should happen first (and block local delete on failure): move it before the DB delete
- If local delete should always happen: use Option B

STEP 5 — Also check for the TODO comment in the broader delete endpoint logic:
```
grep -n "TODO\|pass$\|except.*:" apps/signals/routers/signal.py
```
Fix any other bare `pass` in except blocks while you're here.

STEP 6 — Add a test for the failure case:
Create or update `apps/signals/tests/test_signal_router.py`:
```python
import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from apps.main import app

client = TestClient(app)

@pytest.mark.asyncio
async def test_delete_signal_forwardlane_failure_returns_error():
    """WebServiceException from ForwardLane should NOT be silently swallowed."""
    from apps.web_services.exceptions import WebServiceException
    
    with patch("apps.signals.routers.signal.ForwardlaneApiService") as mock_service:
        mock_instance = AsyncMock()
        mock_instance.delete_signal.side_effect = WebServiceException("Connection failed")
        mock_service.return_value = mock_instance
        
        # Assuming auth is handled — adjust headers as needed
        response = client.delete("/signals/123", headers={"Authorization": "Bearer test"})
        
        # Should NOT return 200/204 — failure must surface
        assert response.status_code in [500, 502, 400], (
            f"Expected error status, got {response.status_code}. "
            "WebServiceException is being silently swallowed!"
        )
```

STEP 7 — Run the test:
```
cd /data/workspace/projects/signal-builder-backend
pipenv run pytest apps/signals/tests/test_signal_router.py -v -k "delete"
```

STEP 8 — Verify with grep that no bare `pass` remains in except blocks:
```
grep -n "except.*:" apps/signals/routers/signal.py -A 1 | grep -E "^\s+pass$"
```
Should return empty.

STEP 9 — Remove the `# TODO: add errors handling` comment.

STEP 10 — Commit:
```
git add apps/signals/routers/signal.py
git commit -m "fix: surface WebServiceException in signal delete endpoint, add logging"
```
```

---

## Dependencies

- None — this is a surgical bug fix, can be done immediately
- Should be done FIRST before other P0 tasks (quick win, high visibility)

---

## Effort Estimate

**2–4 hours** — Very targeted change. Most time goes to reading the code to understand whether upstream delete is critical or best-effort, and writing the test.

---

## Acceptance Criteria

- [ ] No `except WebServiceException: pass` (bare pass) in `apps/signals/routers/signal.py`
- [ ] `WebServiceException` is logged with `logger.error()` or `logger.warning()` with signal ID context
- [ ] Clients receive a non-2xx response when deletion fails (if Option A chosen)
- [ ] Test `test_delete_signal_forwardlane_failure_returns_error` passes
- [ ] `# TODO: add errors handling` comment removed
- [ ] `grep -n "except.*pass" apps/signals/routers/signal.py` returns empty
