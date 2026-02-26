# 007 — Update Outdated/Deprecated Dependencies

**Repo:** forwardlane-backend  
**Priority:** high  
**Effort:** M (3-5h)  
**Status:** pending

## Description

Several dependencies in `Pipfile` are severely outdated or deprecated:
- `boto3==1.23.*` — released May 2022, current is 1.35+. Known CVEs in older boto3.
- `sentry-sdk==1.5.*` — Sentry SDK v2 was released; v1 deprecated.
- `pypdf2==1.28.*` — PyPDF2 was deprecated and merged into `pypdf`. Use `pypdf>=4.0`.
- `django-rest-auth==0.9.*` — Abandoned. Replaced by `dj-rest-auth`.
- `backoff==1.11.*` — current 2.x has API improvements.
- `paramiko==3.5.*` — current, ok.
- `elastic-apm==6.13.*` — current is 6.22+.

## Coding Prompt

Update `/data/workspace/projects/forwardlane-backend/Pipfile`:

1. Replace `pypdf2 = "==1.28.*"` with `pypdf = ">=4.0"` 
   - Find all imports: `grep -r "PyPDF2\|PdfFileReader\|PdfFileWriter" /data/workspace/projects/forwardlane-backend --include="*.py"`
   - Update import statements: `from PyPDF2 import PdfReader` → `from pypdf import PdfReader`
   - `PdfFileReader` was renamed `PdfReader` in pypdf

2. Replace `django-rest-auth = "==0.9.*"` with `dj-rest-auth = ">=6.0"` 
   - Update imports: `from rest_auth` → `from dj_rest_auth`
   - Search: `grep -r "rest_auth" /data/workspace/projects/forwardlane-backend --include="*.py"`

3. Update `boto3 = ">=1.34"` (latest stable)

4. Update `sentry-sdk = ">=2.0"` and update init code (v2 has new API)

5. Update `elastic-apm = ">=6.20"`

6. Update `backoff = ">=2.0"`

7. Run `pipenv install` and fix any conflicts.

8. Run `python -m pytest` to verify nothing broke.

## Dependencies
- 006 (do together with Django upgrade)

## Acceptance Criteria
- [ ] No deprecated packages in Pipfile
- [ ] PyPDF2 replaced with pypdf, all imports updated
- [ ] django-rest-auth replaced with dj-rest-auth, all imports updated
- [ ] boto3 >= 1.34 installed
- [ ] sentry-sdk >= 2.0 installed and init code updated
- [ ] Full test suite passes
