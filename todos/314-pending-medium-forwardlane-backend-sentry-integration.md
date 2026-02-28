# TODO-314: Sentry Error Tracking Integration — forwardlane-backend

**Priority:** MEDIUM  
**Effort:** S  
**Repo:** forwardlane-backend  
**Status:** pending

## Description
No error tracking is configured. For an active enterprise demo (Invesco), silent failures in NL→SQL or LLM fallback chains are invisible. Sentry provides real-time error visibility.

## Autonomous Coding Prompt
```
In /data/workspace/projects/forwardlane-backend/:
1. Add to Pipfile: sentry-sdk = {extras = ["django"], version = ">=1.40"}
2. In forwardlane/settings/base.py, add:
   import sentry_sdk
   from sentry_sdk.integrations.django import DjangoIntegration
   from sentry_sdk.integrations.celery import CeleryIntegration
   SENTRY_DSN = env("SENTRY_DSN", default="")
   if SENTRY_DSN:
       sentry_sdk.init(
           dsn=SENTRY_DSN,
           integrations=[DjangoIntegration(), CeleryIntegration()],
           traces_sample_rate=0.1,
           send_default_pii=False,
       )
3. Add SENTRY_DSN to .env.example with a comment
4. Create a Sentry project at sentry.io for forwardlane-backend, get DSN
5. Add SENTRY_DSN to Railway production environment
6. Test: trigger a deliberate 500 error locally, verify it appears in Sentry
```

## Acceptance Criteria
- [ ] sentry-sdk in Pipfile
- [ ] Sentry init in settings (only when SENTRY_DSN set)
- [ ] Celery tasks also reporting to Sentry
- [ ] SENTRY_DSN in .env.example
- [ ] Confirmed working in staging/production
