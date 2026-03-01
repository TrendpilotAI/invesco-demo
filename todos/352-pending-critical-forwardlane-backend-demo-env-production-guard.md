# TODO 352: DEMO_ENV Production Auth Guard

**Repo:** forwardlane-backend  
**Priority:** CRITICAL  
**Effort:** S (30-60 min)  
**Dependencies:** None

## Description

The `EasyButtonPermission` class allows unauthenticated access when `DEMO_ENV` is set to `demo`, `staging`, `true`, or `1`. If this env var accidentally leaks into production, the entire easy_button API becomes public. Add an explicit production guard.

## File
`easy_button/views.py` — `EasyButtonPermission.has_permission()`

## Coding Prompt

```
You are working in /data/workspace/projects/forwardlane-backend/easy_button/views.py

Task: Harden the EasyButtonPermission class to prevent accidental production auth bypass.

Current code (~line 48):
    def has_permission(self, request, view):
        if os.environ.get('DEMO_ENV') in ('demo', 'staging', 'true', '1'):
            return True
        return bool(request.user and request.user.is_authenticated)

Replace with:
    def has_permission(self, request, view):
        # Never allow demo bypass in production
        railway_env = os.environ.get('RAILWAY_ENVIRONMENT', '').lower()
        django_env = os.environ.get('DJANGO_ENV', '').lower()
        is_production = railway_env == 'production' or django_env == 'production'
        
        if not is_production:
            demo_env = os.environ.get('DEMO_ENV', '').lower()
            if demo_env in ('demo', 'staging', 'true', '1'):
                return True
        
        return bool(request.user and request.user.is_authenticated)

Also add a startup check in easy_button/apps.py ready() method to log a WARNING 
if DEMO_ENV is set and RAILWAY_ENVIRONMENT=production.

Run: pytest easy_button/ -q
Commit: "security: guard DEMO_ENV bypass against production environment"
```

## Acceptance Criteria
- [ ] Production env (RAILWAY_ENVIRONMENT=production) forces auth even with DEMO_ENV=true
- [ ] Demo/staging env still allows bypass with DEMO_ENV set
- [ ] Warning logged at startup if unsafe config detected
- [ ] Tests pass
