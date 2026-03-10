# FL-013: Tenant-Scoped API Keys

**Repo:** forwardlane-backend  
**Priority:** P1  
**Effort:** M (3-4 days)  
**Status:** pending

## Task Description
Implement self-service tenant API key generation with plan-tier-based rate limiting. Clients generate keys to build their own integrations without going through SAML SSO. Keys are hashed at rest, rate-limited by tier.

## Problem
Currently the only way to access the API is via SAML SSO (Invesco) or the easy_button demo token. Enterprise clients building integrations need programmatic API access. Without API keys, we can't support client-side integration development or machine-to-machine access.

## Coding Prompt
```
Create a new Django app: api_keys/

1. api_keys/models.py:
```python
import secrets
import hashlib
from django.db import models
from core.models import BaseModel

RATE_LIMIT_TIERS = {
    'bronze': {'hour': 100, 'day': 500},
    'silver': {'hour': 1000, 'day': 10000},
    'gold': {'hour': None, 'day': None},  # Unlimited
}

def generate_key():
    return 'fl_' + secrets.token_urlsafe(32)

def hash_key(key: str) -> str:
    return hashlib.sha256(key.encode()).hexdigest()

class APIKey(BaseModel):
    TIER_CHOICES = [('bronze', 'Bronze'), ('silver', 'Silver'), ('gold', 'Gold')]
    
    tenant = models.ForeignKey('customers.Tenant', on_delete=models.CASCADE, related_name='api_keys')
    name = models.CharField(max_length=100)  # Human-readable label e.g. "Invesco Integration"
    key_prefix = models.CharField(max_length=10)  # First 8 chars for identification: 'fl_abc123'
    key_hash = models.CharField(max_length=64, unique=True)  # SHA-256 hash of full key
    rate_limit_tier = models.CharField(max_length=20, choices=TIER_CHOICES, default='silver')
    is_active = models.BooleanField(default=True)
    last_used_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)  # None = never expires
    created_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
    
    class Meta:
        db_table = 'api_keys_apikey'
    
    @classmethod
    def create_key(cls, tenant, name, tier='silver', created_by=None):
        """Generate a new API key — returns (APIKey instance, raw_key)"""
        raw_key = generate_key()
        obj = cls.objects.create(
            tenant=tenant,
            name=name,
            key_prefix=raw_key[:10],
            key_hash=hash_key(raw_key),
            rate_limit_tier=tier,
            created_by=created_by,
        )
        return obj, raw_key  # raw_key shown ONCE to user, then discarded
    
    @classmethod
    def authenticate(cls, raw_key: str):
        """Returns APIKey if valid, None otherwise"""
        key_hash = hash_key(raw_key)
        try:
            key = cls.objects.select_related('tenant').get(
                key_hash=key_hash, is_active=True
            )
            if key.expires_at and key.expires_at < timezone.now():
                return None
            return key
        except cls.DoesNotExist:
            return None
```

2. api_keys/authentication.py (DRF authentication backend):
```python
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

class APIKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer fl_'):
            return None  # Not API key auth — try other backends
        
        raw_key = auth_header[7:]  # Strip 'Bearer '
        api_key = APIKey.authenticate(raw_key)
        if not api_key:
            raise AuthenticationFailed('Invalid or expired API key')
        
        # Update last_used_at async
        APIKey.objects.filter(id=api_key.id).update(last_used_at=timezone.now())
        
        # Return (user, auth) tuple — use a synthetic user object scoped to tenant
        return (api_key.tenant.admin_user, api_key)
    
    def authenticate_header(self, request):
        return 'Bearer realm="api"'
```

3. api_keys/throttling.py:
```python
from rest_framework.throttling import BaseThrottle
from django.core.cache import cache

class APIKeyRateThrottle(BaseThrottle):
    def allow_request(self, request, view):
        if not isinstance(request.auth, APIKey):
            return True  # Only throttle API key requests
        
        api_key = request.auth
        tier = RATE_LIMIT_TIERS.get(api_key.rate_limit_tier, {})
        hourly_limit = tier.get('hour')
        if hourly_limit is None:
            return True  # Gold = unlimited
        
        cache_key = f'api_key_throttle:{api_key.id}:hour'
        count = cache.get(cache_key, 0)
        if count >= hourly_limit:
            return False
        cache.set(cache_key, count + 1, timeout=3600)
        return True
    
    def wait(self):
        return 60  # Retry after 1 minute
```

4. api_keys/views.py:
- GET/POST /api/v1/api-keys/ — list/create (tenant-scoped)
- DELETE /api/v1/api-keys/{id}/ — revoke key
- POST /api/v1/api-keys/{id}/rotate/ — rotate (revoke + create new)
- Never return the full key after creation (only key_prefix for identification)

5. Add APIKeyAuthentication to DEFAULT_AUTHENTICATION_CLASSES in settings:
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'access_guardian.authentication.JWTAuthentication',
        'api_keys.authentication.APIKeyAuthentication',  # Add this
    ],
    ...
}
```

6. api_keys/tests/test_authentication.py:
- Test valid key authenticates successfully
- Test invalid key returns 401
- Test expired key returns 401
- Test rate limiting returns 429 on Bronze tier after 100 requests/hr
- Test Gold tier has no rate limit

Files to create:
- api_keys/__init__.py, apps.py, models.py, views.py, serializers.py, urls.py
- api_keys/authentication.py, throttling.py
- api_keys/migrations/ (initial migration)
- api_keys/tests/
- Update forwardlane/settings/base.py
- Update forwardlane/urls.py
```

## Acceptance Criteria
- [ ] `fl_` prefixed API keys generated and stored as SHA-256 hash
- [ ] Raw key shown exactly once at creation, never retrievable again
- [ ] `Authorization: Bearer fl_xxx` header authenticates requests
- [ ] Bronze tier: 100 req/hr, Silver: 1000 req/hr, Gold: unlimited
- [ ] Rate limiting uses Redis cache (not database)
- [ ] Key rotation endpoint revokes old + creates new key atomically
- [ ] Tests for auth, rate limiting, expiration all pass

## Dependencies
- FL-034 (audit logging) — API key usage auto-logged in audit middleware.
- Redis must be configured (already done for caching).
