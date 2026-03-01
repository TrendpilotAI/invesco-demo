# TODO 351: Migrate django-rest-auth → dj-rest-auth

**Repo:** forwardlane-backend  
**Priority:** CRITICAL  
**Effort:** M (2-4 hours)  
**Dependencies:** None

## Description

`django-rest-auth==0.9.*` is an abandoned package (archived 2020, no security updates). Replace with the actively maintained fork `dj-rest-auth`.

## Coding Prompt

```
You are working in /data/workspace/projects/forwardlane-backend/.

Task: Migrate from abandoned django-rest-auth to dj-rest-auth.

Steps:
1. In Pipfile, remove: django-rest-auth = "==0.9.*"
   Add: dj-rest-auth = ">=5.0,<6.0"

2. Search for all imports of rest_auth:
   grep -r "from rest_auth" . --include="*.py"
   grep -r "import rest_auth" . --include="*.py"

3. Update each import: `rest_auth` → `dj_rest_auth`
   Example: `from rest_auth.registration.views import RegisterView`
          → `from dj_rest_auth.registration.views import RegisterView`

4. Update INSTALLED_APPS in any settings files:
   'rest_auth' → 'dj_rest_auth'
   'rest_auth.registration' → 'dj_rest_auth.registration'

5. Update urls.py files that include rest_auth urls:
   `include('rest_auth.urls')` → `include('dj_rest_auth.urls')`

6. Run: pipenv install

7. Run tests: pytest --tb=short -q

8. Commit: "fix: migrate django-rest-auth → dj-rest-auth (security)"
```

## Acceptance Criteria
- [ ] Pipfile no longer references django-rest-auth
- [ ] dj-rest-auth is installed and listed in Pipfile
- [ ] All auth endpoints still work (login, logout, password reset)
- [ ] Tests pass
