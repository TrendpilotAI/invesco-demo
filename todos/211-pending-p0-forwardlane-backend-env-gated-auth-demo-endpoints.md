# 211 · ENV-GATED AUTH ON EASY_BUTTON DEMO ENDPOINTS

**Repo:** forwardlane-backend  
**Priority:** P0 (security — unauthenticated analytical DB exposed to internet)  
**Effort:** S (2–3 hours)  
**Status:** pending

---

## Task Description

All 8 endpoints in `easy_button/views.py` use `AllowAny` (`_EASY_BUTTON_PERMISSIONS = [AllowAny]`).
This means anyone who discovers the URL can query the analytical database, run SQL template
executions (`SignalRunView`), and trigger LLM-generated SQL queries (`NLQueryView`).

The fix is an environment-gated permission class:
- `DEMO_ENV=local` → AllowAny (dev mode)
- `DEMO_ENV=staging` + `EASY_BUTTON_DEMO_TOKEN=<token>` → static token auth via `X-Demo-Token` header
- `DEMO_ENV=prod` → Django `IsAuthenticated` (requires session/JWT)

---

## Coding Prompt (Agent-Executable)

```
You are modifying the forwardlane-backend Django project at /data/workspace/projects/forwardlane-backend/.

TASK: Replace AllowAny on easy_button endpoints with an environment-gated permission class.

STEP 1 — Create easy_button/permissions.py:
---
import os
from rest_framework.permissions import BasePermission

DEMO_ENV = os.environ.get('DEMO_ENV', 'local')   # 'prod' | 'staging' | 'local'
DEMO_TOKEN = os.environ.get('EASY_BUTTON_DEMO_TOKEN', '')

class EasyButtonPermission(BasePermission):
    """
    Environment-gated permission for Invesco demo endpoints.
    - local: open (AllowAny) — developer convenience
    - staging: static X-Demo-Token header check
    - prod: standard Django IsAuthenticated
    """
    def has_permission(self, request, view):
        if DEMO_ENV == 'local':
            return True
        if DEMO_ENV == 'staging':
            if not DEMO_TOKEN:
                return True  # Token not configured → open (allows unset staging envs)
            return request.headers.get('X-Demo-Token') == DEMO_TOKEN
        # Default (prod): require authentication
        return bool(request.user and request.user.is_authenticated)
---

STEP 2 — Update easy_button/views.py:
Replace:
  from rest_framework.permissions import AllowAny
  ...
  _EASY_BUTTON_PERMISSIONS = [AllowAny]

With:
  from easy_button.permissions import EasyButtonPermission
  ...
  _EASY_BUTTON_PERMISSIONS = [EasyButtonPermission]

Remove the AllowAny import entirely (it's no longer needed).

STEP 3 — Update analytical/views.py:
The 5 views in analytical/views.py also lack authentication. Apply EasyButtonPermission there too.
Each view uses @method_decorator(csrf_exempt) and Django's View base class.
Convert each view from Django View → DRF APIView and add:
  permission_classes = [EasyButtonPermission]

For each view class (DashboardView, AdvisorsListView, AdvisorDetailView, SignalsView, EasyButtonView):
- Change inheritance from View → APIView
- Remove @method_decorator(csrf_exempt) (not needed on DRF APIView with token auth)
- Return rest_framework.response.Response instead of JsonResponse
- Add: permission_classes = [EasyButtonPermission]

STEP 4 — Document env vars needed in README or settings docstring:
Add a comment block to easy_button/permissions.py:
# Required env vars:
# DEMO_ENV: 'local' (default) | 'staging' | 'prod'
# EASY_BUTTON_DEMO_TOKEN: required when DEMO_ENV=staging (any secure random string)
# Example: EASY_BUTTON_DEMO_TOKEN=$(openssl rand -hex 32)

STEP 5 — Verify no imports break:
Run: cd /data/workspace/projects/forwardlane-backend && python manage.py check
Fix any import errors.
```

---

## Files to Modify

| File | Change |
|------|--------|
| `easy_button/permissions.py` | **CREATE** — new permission class |
| `easy_button/views.py` | Replace `AllowAny` with `EasyButtonPermission` |
| `analytical/views.py` | Convert to APIView, add `permission_classes` |

---

## Acceptance Criteria

- [ ] `easy_button/permissions.py` exists with `EasyButtonPermission` class
- [ ] All 8 `easy_button/views.py` views use `EasyButtonPermission` (not `AllowAny`)
- [ ] `analytical/views.py` views use `EasyButtonPermission`
- [ ] `DEMO_ENV=local` → unauthenticated request returns 200
- [ ] `DEMO_ENV=staging`, `EASY_BUTTON_DEMO_TOKEN=test123` → request with `X-Demo-Token: test123` returns 200
- [ ] `DEMO_ENV=staging`, `EASY_BUTTON_DEMO_TOKEN=test123` → request without header returns 403
- [ ] `DEMO_ENV=prod` → unauthenticated request returns 401/403
- [ ] `python manage.py check` passes with no errors
- [ ] No existing tests broken

---

## Risk Notes

⚠️ **Before deploying to production:** Confirm the Signal Studio Next.js frontend sends auth
credentials to easy_button endpoints (check `signal-studio` repo for easy-button API calls).
Deploy with `DEMO_ENV=staging` first and validate demo flow before switching to `DEMO_ENV=prod`.
