# TODO 354: Upgrade Stale Dependencies

**Repo:** forwardlane-backend  
**Priority:** HIGH  
**Effort:** M (3-5 hours)  
**Dependencies:** 351 (dj-rest-auth migration must be done first)

## Description

Multiple dependencies are significantly outdated. Most critical: pypdf2 (removed from PyPI, replaced by pypdf), boto3 (14 months stale), sentry-sdk (1.x vs 2.x breaking changes).

## Coding Prompt

```
You are working in /data/workspace/projects/forwardlane-backend/.

Task: Upgrade stale dependencies. Do one at a time to catch regressions.

Step 1 — Replace pypdf2 with pypdf:
  In Pipfile: remove `pypdf2 = "==1.28.*"`, add `pypdf = ">=4.0,<5.0"`
  Search for all imports: grep -r "from PyPDF2\|import PyPDF2" . --include="*.py"
  Update imports: PyPDF2 → pypdf (API is largely compatible)
  Run tests after.

Step 2 — Upgrade boto3:
  In Pipfile: change `boto3 = "==1.23.*"` to `boto3 = ">=1.34,<2.0"`
  Run: pipenv install
  Run tests.

Step 3 — Upgrade sentry-sdk:
  In Pipfile: change `sentry-sdk = "==1.5.*"` to `sentry-sdk = ">=2.0,<3.0"`
  NOTE: sentry-sdk 2.x has breaking changes in initialization
  Check settings for sentry init and update per https://docs.sentry.io/platforms/python/migration/1.x-to-2.x/
  Run tests.

Step 4 — Upgrade django-cors-headers:
  `django-cors-headers = "==3.10.*"` → `django-cors-headers = ">=4.0,<5.0"`
  Run: pipenv install && pytest -q

Step 5 — Minor celery upgrade:
  `celery = "==5.2.*"` → `celery = ">=5.4,<6.0"`
  Run: pipenv install && pytest -q

After all upgrades:
  pipenv lock
  Run full test suite: pytest --tb=short -q
  Commit: "chore: upgrade stale dependencies (pypdf2→pypdf, boto3, sentry-sdk 2.x, celery)"
```

## Acceptance Criteria
- [ ] pypdf2 replaced with pypdf, all imports updated
- [ ] boto3 upgraded to 1.34+
- [ ] sentry-sdk upgraded to 2.x with updated init config
- [ ] No test regressions
- [ ] Pipfile.lock updated
