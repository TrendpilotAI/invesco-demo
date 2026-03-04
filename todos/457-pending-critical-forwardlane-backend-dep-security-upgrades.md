# TODO-457: Upgrade Critically Outdated Dependencies

**Priority:** CRITICAL  
**Repo:** forwardlane-backend  
**Effort:** M (4-8 hours including testing)  
**Dependencies:** TODO-456 (Django 4.2 compat first)

## Description
Several pinned deps are dangerously outdated with potential CVEs:
- `boto3==1.23` → ~18 months old (current ~1.34)
- `sentry-sdk==1.5` → major version behind (current ~2.x)  
- `pypdf2==1.28` → abandoned, superseded by `pypdf`
- `django-rest-auth==0.9` → abandoned, replace with `dj-rest-auth`
- `elastic-apm==6.13` → check advisories
- `django-cors-headers==3.10` → current is 4.x

## Coding Prompt
```
In /data/workspace/projects/forwardlane-backend/Pipfile:

1. Run safety check: pip install safety && safety check -r <(pipenv run pip freeze)
   Document all CVEs found.

2. Upgrade these packages:
   - boto3: "==1.23.*" → "*" (or latest stable pin)
   - sentry-sdk: "==1.5.*" → ">=2.0,<3.0"
   - pypdf2: "==1.28.*" → remove, add pypdf = "*"
   - django-rest-auth: "==0.9.*" → remove, add dj-rest-auth = "*"
   - elastic-apm: "==6.13.*" → "*"
   - django-cors-headers: "==3.10.*" → "==4.*"

3. For pypdf2 → pypdf migration:
   grep -r "PyPDF2\|pypdf2" --include="*.py" -l
   Update imports: from PyPDF2 → from pypdf

4. For django-rest-auth → dj-rest-auth:
   grep -r "rest_auth" --include="*.py" -l
   Update imports accordingly (dj-rest-auth has same API mostly)

5. Run: pipenv install
6. Run: python manage.py check
7. Run: python -m pytest -x
8. Commit: "deps: upgrade outdated/abandoned packages - boto3, sentry-sdk, pypdf, dj-rest-auth"
```

## Acceptance Criteria
- [ ] No abandoned packages in Pipfile
- [ ] safety check passes with 0 critical CVEs
- [ ] All tests pass after upgrades
- [ ] `python manage.py check` passes
