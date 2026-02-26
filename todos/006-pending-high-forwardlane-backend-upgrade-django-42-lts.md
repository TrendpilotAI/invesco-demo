# 006 — Upgrade Django 3.2 → 4.2 LTS

**Repo:** forwardlane-backend  
**Priority:** high  
**Effort:** L (1-2d)  
**Status:** pending

## Description

Django 3.2 reached End of Life in April 2024. Running EOL Django means no security patches. The codebase must be upgraded to Django 4.2 LTS (supported until April 2026) or ideally Django 5.1.

## Coding Prompt

1. Update `Pipfile`:
   - `django = "==4.2.*"` (or `"==5.1.*"`)
   - `django-cors-headers = "==4.*"` (3.x may not support Django 4.2)
   - `django-rest-auth` is abandoned — replace with `dj-rest-auth = "==6.*"`
   - `djangorestframework = "==3.15.*"`
   - `django-filter = "==24.*"`
   - `django-extensions = "==3.2.*"` (compatible)
   - `django-celery-beat = "==2.6.*"`
   - `django-otp = "==1.5.*"`
   - `sentry-sdk = "==2.*"`

2. Run `pipenv install` and fix any dependency conflicts.

3. Django 4.x breaking changes to address:
   - `DEFAULT_AUTO_FIELD` — ensure set in settings (already using AutoField explicitly in some models)
   - `django.utils.translation.ugettext_lazy` → `gettext_lazy` (4.0 removed ugettext)
   - `request.is_ajax()` removed in 4.0 — search codebase and replace
   - CSRF cookie `SameSite` default changed — verify CORS config still works
   - `django-saml2-auth==2.2` may need upgrade for Django 4 compat

4. Run full test suite: `python -m pytest`

5. Test Railway deployment with upgraded dependencies.

## Dependencies
- 007 (update all outdated deps — do together)

## Acceptance Criteria
- [ ] `django==4.2.*` in Pipfile.lock
- [ ] Full test suite passes
- [ ] Railway deployment boots successfully
- [ ] No deprecation warnings in logs
- [ ] Admin UI accessible
