# TODO-584: Add CI Test Gate for development Branch

**Priority:** HIGH
**Repo:** forwardlane-backend
**Effort:** S (2h)
**Status:** pending

## Problem
`bitbucket-pipelines.yml` `development` branch has no test gate. Code merges to development without running tests, lint, or security scan. This means broken code can reach staging/Railway without detection.

## Fix

In `bitbucket-pipelines.yml`, add `tox` step to the `development` branch pipeline:

```yaml
branches:
  development:
    - step:
        name: Test & Lint (development)
        image: python:3.11
        caches:
          - pip
        script:
          - pip install tox
          - tox
    - step:
        name: Deploy to Railway (staging)
        ...existing deploy step...
```

Also update `tox.ini` to include `easy_button` and `analytical` in pylint and bandit scope:

```ini
[testenv:lint]
commands =
    pylint forwardlane easy_button analytical core user adapters ...

[testenv:security]
commands =
    bandit -r easy_button analytical core user ...
```

## Files
- `bitbucket-pipelines.yml`
- `tox.ini`

## Acceptance Criteria
- [ ] PRs to `development` cannot merge without green CI
- [ ] `easy_button` and `analytical` included in pylint/bandit
- [ ] CI runs `python manage.py check` (catches Django config errors)
- [ ] CI time under 5 minutes

## Dependencies
- TODO-582 (analytical tests must exist first or CI will skip them)
