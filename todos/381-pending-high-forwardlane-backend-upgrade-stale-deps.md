# 381 — Upgrade Stale/Vulnerable Dependencies

**Repo:** forwardlane-backend  
**Priority:** high  
**Effort:** M (2-4h)  
**Status:** pending

## Description
Several deps are significantly behind: sentry-sdk 1.5 (current: 2.x), elastic-apm 6.13 (current: 6.22+), pypdf2 1.28 (deprecated — use pypdf), django-rest-auth 0.9 (deprecated — use dj-rest-auth). These carry security risks and miss bug fixes.

## Coding Prompt
```
In /data/workspace/projects/forwardlane-backend/Pipfile:

1. Run: pipenv check (show known CVEs)
2. Upgrade priority deps:
   - sentry-sdk: "==1.5.*" → ">=2.0"
   - elastic-apm: "==6.13.*" → ">=6.22"
   - pypdf2: "==1.28.*" → switch to pypdf (pip name: pypdf)
   - django-rest-auth: "==0.9.*" → replace with dj-rest-auth (drop-in replacement)
   - boto3: "==1.23.*" → ">=1.34"
3. Run pipenv install
4. Fix any import/API changes (pypdf2 → pypdf has different import path)
5. Run tox — fix any test failures
6. Run bandit for security scan: bandit -r . -x ./libs
7. Commit: "chore: upgrade stale deps — sentry 2.x, pypdf, dj-rest-auth"
```

## Acceptance Criteria
- `pipenv check` returns no known CVEs
- All tests pass after upgrade
- No pypdf2 imports remain (use pypdf)
