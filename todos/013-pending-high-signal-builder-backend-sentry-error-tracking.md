---
status: pending
priority: high
issue_id: "013"
tags: [signal-builder-backend, observability, sentry, monitoring, errors]
dependencies: []
---

# TODO 013 — Sentry Error Tracking Integration

**Status:** pending  
**Priority:** high  
**Repo:** signal-builder-backend  
**Effort:** S (0.5-1 day)

## Problem Statement

The backend has no error tracking or alerting. When exceptions occur in production (Railway deployment), they are visible only in raw Railway logs — no grouping, no alerts, no context (user, org, request params). This means:

- Bugs discovered by users, not engineering
- No insight into frequency or impact of errors
- Celery task failures are completely silent
- Custom exceptions (`TranslationError`, `SignalDataPreparationError`) disappear into logs

## Findings

- `core/exceptions/` has custom exception hierarchy
- `core/loggers/logger.py` uses `loguru` — structured but no remote sink
- `api.py` is the FastAPI entry point — Sentry SDK hooks here
- `core/celery.py` defines the Celery app — Sentry has native Celery integration
- Deployment is Railway — `SENTRY_DSN` should be an env var

## Proposed Solutions

### Option A: sentry-sdk with FastAPI + Celery integration (Recommended)
Single SDK handles both FastAPI exceptions and Celery task failures.

**Pros:** 5-minute setup, rich context (user, request, breadcrumbs), Celery support  
**Cons:** Adds external dependency, data leaves the server

### Option B: Custom error webhook to Slack/PagerDuty
Catch unhandled exceptions and POST to webhook.

**Pros:** No external SaaS  
**Cons:** Much more implementation effort, no grouping/dedup

**Recommendation:** Option A — sentry-sdk is the industry standard and setup is trivial.

## Coding Prompt

```
You are integrating Sentry error tracking into signal-builder-backend.

Repository: /data/workspace/projects/signal-builder-backend/
Stack: FastAPI 0.92, Python 3.11, Celery, loguru

TASK: Add Sentry SDK with FastAPI and Celery integrations.

1. Add to Pipfile [packages]:
   sentry-sdk = {extras = ["fastapi", "celery"], version = "*"}

2. Create core/sentry.py:
   import sentry_sdk
   from sentry_sdk.integrations.fastapi import FastApiIntegration
   from sentry_sdk.integrations.starlette import StarletteIntegration
   from sentry_sdk.integrations.celery import CeleryIntegration
   from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
   import settings

   def init_sentry():
       if not settings.SENTRY_DSN:
           return  # Sentry disabled if no DSN configured
       sentry_sdk.init(
           dsn=settings.SENTRY_DSN,
           environment=settings.ENVIRONMENT,  # "production", "staging", "development"
           release=settings.APP_VERSION,       # git SHA or semver
           traces_sample_rate=settings.SENTRY_TRACES_RATE,  # default 0.1 (10% tracing)
           integrations=[
               StarletteIntegration(transaction_style="endpoint"),
               FastApiIntegration(transaction_style="endpoint"),
               CeleryIntegration(monitor_beat_tasks=True),
               SqlalchemyIntegration(),
           ],
           before_send=_before_send,
       )

   def _before_send(event, hint):
       # Strip PII: remove Authorization header values
       if "request" in event and "headers" in event["request"]:
           headers = event["request"]["headers"]
           if "authorization" in headers:
               headers["authorization"] = "[Filtered]"
       return event

3. Add to settings (read from env):
   SENTRY_DSN: str = os.getenv("SENTRY_DSN", "")
   ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
   APP_VERSION: str = os.getenv("APP_VERSION", "unknown")
   SENTRY_TRACES_RATE: float = float(os.getenv("SENTRY_TRACES_RATE", "0.1"))

4. Update api.py:
   - Call init_sentry() before get_application()
   - Example:
     from core.sentry import init_sentry
     init_sentry()
     fast_api = get_application()

5. Update core/celery.py:
   - Call init_sentry() after celery_app is created
   - Sentry CeleryIntegration automatically captures task failures

6. Add Sentry user context in auth middleware (core/middlewares/auth_middleware.py):
   import sentry_sdk
   # After successfully authenticating user:
   sentry_sdk.set_user({"id": str(user.id), "email": user.email})

7. Add Sentry tags for org context wherever org_id is resolved:
   sentry_sdk.set_tag("org_id", str(org_id))

8. Create tests/test_sentry_integration.py:
   - Test that init_sentry() is a no-op when SENTRY_DSN is empty
   - Test that _before_send strips Authorization header
   - Test that sentry is not called on expected 4xx responses
   - Mock sentry_sdk.capture_exception to verify it's called on 500

9. Update README.md with Sentry setup instructions:
   - Required env var: SENTRY_DSN
   - Optional: ENVIRONMENT, APP_VERSION, SENTRY_TRACES_RATE

10. Run: pipenv install && python -m pytest tests/test_sentry_integration.py -v

Constraints:
- SENTRY_DSN must be optional — app works normally if not set (SENTRY_DSN="")
- PII must be stripped before sending (Authorization headers, passwords)
- Do not capture expected exceptions (401, 403, 404) as Sentry errors
- traces_sample_rate default is 0.1 (not 1.0) to avoid Sentry quota burn
```

## Acceptance Criteria

- [ ] `sentry-sdk[fastapi,celery]` added to Pipfile
- [ ] `core/sentry.py` created with `init_sentry()` function
- [ ] Sentry is a no-op when `SENTRY_DSN=""` (no crash)
- [ ] Authorization headers are stripped from Sentry events (PII protection)
- [ ] Celery task failures are captured automatically
- [ ] SQLAlchemy integration enabled for query performance tracking
- [ ] User context (id, email) set after successful authentication
- [ ] org_id set as Sentry tag on each request
- [ ] `tests/test_sentry_integration.py` passes
- [ ] README updated with Sentry configuration instructions

## Dependencies

None — standalone integration.

## Work Log

### 2026-02-26 - Todo Created

**By:** Planning Agent

**Actions:**
- Identified complete absence of error tracking in production
- Verified Celery task failures are silent (no alerting)
- Designed PII-safe integration with Authorization header stripping

**Learnings:**
- sentry-sdk supports FastAPI + Celery natively — minimal setup
- Must set SENTRY_DSN="" as default to avoid crashes in local dev
