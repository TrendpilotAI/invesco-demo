# 340 — Add Demo Token Header Auth to EasyButtonPermission

**Priority:** HIGH
**Repo:** forwardlane-backend
**Effort:** S (1 hour)
**Category:** Security

## Description
`EasyButtonPermission` in `easy_button/views.py` currently allows any request through when
`DEMO_ENV=demo`. This means anyone who discovers the easy_button endpoint URLs can access
full Invesco advisor financial data without any credentials.

Fix: require an `X-Demo-Token` header set to a shared secret when in demo mode.

## Implementation

```python
import hmac
import os

class EasyButtonPermission(BasePermission):
    """
    In demo/staging mode: require X-Demo-Token header matching DEMO_TOKEN env var.
    In production mode: require authenticated user.
    """
    def has_permission(self, request, view):
        demo_env = os.environ.get('DEMO_ENV', '')
        if demo_env in ('demo', 'staging', 'true', '1'):
            demo_token = os.environ.get('DEMO_TOKEN', '')
            if not demo_token:
                # No token configured: open access (for local dev only)
                return True
            provided = request.META.get('HTTP_X_DEMO_TOKEN', '')
            return hmac.compare_digest(provided, demo_token)
        # Production: require authenticated user
        return bool(request.user and request.user.is_authenticated)
```

## Railway Configuration
Set `DEMO_TOKEN` to a long random secret in Railway:
```bash
openssl rand -hex 32
# → Set as DEMO_TOKEN in Railway env vars
```

Frontend must send: `X-Demo-Token: <value>` header on all easy_button requests.

## Files to Change
- `easy_button/views.py` — `EasyButtonPermission.has_permission()`
- `easy_button/tests/test_permissions.py` — add token validation tests
- Railway env vars — add `DEMO_TOKEN`

## Acceptance Criteria
- [ ] Request without `X-Demo-Token` returns 403 when `DEMO_TOKEN` is set
- [ ] Request with correct token returns 200
- [ ] Request with wrong token returns 403
- [ ] Uses `hmac.compare_digest()` (constant-time comparison, no timing attack)
- [ ] When `DEMO_TOKEN` not set, behavior unchanged (backwards compatible for local dev)
