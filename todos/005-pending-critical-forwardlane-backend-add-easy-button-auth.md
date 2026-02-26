# 005 — Add Configurable Auth to Easy Button Endpoints

**Repo:** forwardlane-backend  
**Priority:** critical  
**Effort:** M (3-5h)  
**Status:** pending

## Description

All `easy_button/` endpoints use `permission_classes = [AllowAny]` (hardcoded as `_EASY_BUTTON_PERMISSIONS = [AllowAny]`). This was intentional for the Invesco demo, but creates a security risk if/when the backend is exposed beyond the demo context. Any attacker who discovers the endpoint can query all advisor data without authentication.

## Coding Prompt

File: `/data/workspace/projects/forwardlane-backend/easy_button/views.py`

1. Replace the hardcoded `_EASY_BUTTON_PERMISSIONS = [AllowAny]` with an environment-controlled flag:

```python
import os
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

_EASY_BUTTON_AUTH_REQUIRED = os.environ.get('EASY_BUTTON_AUTH_REQUIRED', 'false').lower() == 'true'

if _EASY_BUTTON_AUTH_REQUIRED:
    _EASY_BUTTON_PERMISSIONS = [IsAuthenticated]
    _EASY_BUTTON_AUTHENTICATION = [JWTAuthentication]
else:
    _EASY_BUTTON_PERMISSIONS = [AllowAny]
    _EASY_BUTTON_AUTHENTICATION = []
```

2. Apply `authentication_classes = _EASY_BUTTON_AUTHENTICATION` to all APIView classes in easy_button/views.py.

3. Update `.env.example` to document `EASY_BUTTON_AUTH_REQUIRED=false # Set true for production`.

4. Add to Railway env documentation in README.md.

5. Add rate limiting regardless of auth state using Django's cache framework:
   - Max 60 requests/minute per IP for all easy_button endpoints
   - Use a decorator or mixin applied to all views

## Dependencies
- None (standalone)

## Acceptance Criteria
- [ ] `EASY_BUTTON_AUTH_REQUIRED=false` → AllowAny (demo mode works unchanged)
- [ ] `EASY_BUTTON_AUTH_REQUIRED=true` → IsAuthenticated (JWT required)
- [ ] .env.example updated
- [ ] Rate limiting applied (60 req/min per IP)
- [ ] Tests cover both auth modes
