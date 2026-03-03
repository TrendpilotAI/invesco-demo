# TODO-425: Dependency CVE Audit & Upgrade

**Repo:** forwardlane-backend  
**Priority:** HIGH  
**Effort:** M (half day)  
**Depends on:** None

## Problem
Multiple dependencies are severely outdated with known security issues:
- `sentry-sdk==1.5` → latest 2.x (significant security fixes)
- `boto3==1.23` → latest 1.34+ (3 years behind)
- `django-rest-auth==0.9` → **abandoned 2019**, use `dj-rest-auth >= 5.0`
- `pypdf2==1.28` → deprecated, use `pypdf >= 3.x`
- `six` → Python 2 compat shim, no longer needed in Python 3.9+
- `django-cors-headers==3.10` → latest 4.x

## Task
1. Run `pip-audit` to enumerate CVEs
2. Update Pipfile to current stable versions
3. Run full test suite to catch regressions
4. Remove `six` dependency

## Coding Prompt
```bash
# Step 1: audit
pipenv run pip-audit

# Step 2: update Pipfile
sentry-sdk = ">=2.0,<3.0"
boto3 = ">=1.34,<2.0"
dj-rest-auth = ">=5.0"  # replaces django-rest-auth
pypdf = ">=3.0"          # replaces pypdf2
django-cors-headers = ">=4.0"
# Remove: six, pypdf2, django-rest-auth

# Step 3: fix imports
# grep -r "from rest_auth" → replace with "from dj_rest_auth"
# grep -r "PyPDF2" → replace with "pypdf"
# grep -r "import six" → remove or replace with Python 3 equivalent

# Step 4: test
pipenv run pytest
```

## Acceptance Criteria
- [ ] `pip-audit` reports zero HIGH/CRITICAL CVEs
- [ ] `django-rest-auth` replaced with `dj-rest-auth`
- [ ] `pypdf2` replaced with `pypdf`
- [ ] `six` removed
- [ ] Full test suite passes
- [ ] Add `pip-audit` to `tox.ini` security check step
