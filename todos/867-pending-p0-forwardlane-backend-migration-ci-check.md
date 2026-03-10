# FL-025: Migration CI Check — Add to Bitbucket Pipelines

**Repo:** forwardlane-backend  
**Priority:** P0  
**Effort:** S (2 hours)  
**Status:** pending

## Task Description
Add `python manage.py migrate --check` to CI pipeline to detect unapplied migrations before they reach production. Prevents production deployment incidents caused by missing migrations.

## Problem
Currently no CI step verifies that all migrations have been applied. A developer could push a new migration file, and if the deploy step runs `migrate` during deploy but CI doesn't catch conflicts, a broken migration could halt production.

## Coding Prompt
```
In /data/workspace/projects/forwardlane-backend/bitbucket-pipelines.yml:

1. Add a "migration check" step to the test stage that runs:
   - python manage.py migrate --check
   - python manage.py showmigrations | grep '\[ \]' (detect unapplied)

2. This should run BEFORE the deploy step in both `development` and `master` branches.

3. Also add to tox.ini as a separate testenv:
   [testenv:migrations]
   commands = python manage.py migrate --check

4. Use a minimal Django settings that connects to a test database (same as pytest uses).

File to modify: bitbucket-pipelines.yml, tox.ini
```

## Acceptance Criteria
- [ ] `bitbucket-pipelines.yml` has migration check step before deploy
- [ ] CI fails if any migration is missing or conflicted
- [ ] tox has `migrations` testenv
- [ ] README documents the migration check

## Dependencies
None — fully independent.
