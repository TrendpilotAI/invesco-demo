# TODO-422: Replace DEMO_ENV AllowAny with API Key Auth

**Repo:** forwardlane-backend  
**Priority:** CRITICAL  
**Effort:** S (2-4 hours)  
**Depends on:** None

## Problem
`EasyButtonPermission` in `easy_button/views.py` grants full access to ALL easy_button endpoints when `DEMO_ENV` env var is set to `demo`, `staging`, `true`, or `1`. Any URL discoverer with knowledge of the env var setting gets unrestricted access to Invesco advisor data.

## Task
Implement `X-Demo-Token` header validation using HMAC signature against a `DEMO_TOKEN` secret env var.

## Coding Prompt
```python
# In easy_button/views.py, replace EasyButtonPermission:
import hashlib, hmac

class EasyButtonPermission(BasePermission):
    def has_permission(self, request, view):
        demo_token = os.environ.get('DEMO_TOKEN', '')
        if demo_token and os.environ.get('DEMO_ENV') in ('demo', 'staging', 'true', '1'):
            provided = request.META.get('HTTP_X_DEMO_TOKEN', '')
            return hmac.compare_digest(provided, demo_token)
        return bool(request.user and request.user.is_authenticated)
```

Set `DEMO_TOKEN` in Railway env vars. Update frontend to send `X-Demo-Token` header.

## Acceptance Criteria
- [ ] `DEMO_ENV=demo` without valid `X-Demo-Token` returns 403
- [ ] Valid token allows access
- [ ] Authenticated users always bypass token check
- [ ] Unit test covers all three cases
