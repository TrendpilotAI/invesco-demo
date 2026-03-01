# 341 — Add easy_button + analytical to pylint/bandit in tox.ini

**Priority:** HIGH
**Repo:** forwardlane-backend
**Effort:** S (30 min)
**Category:** Workflow / Security

## Description
`tox.ini` runs pylint and bandit across a list of Django apps, but `easy_button` and
`analytical` are missing from the scope. These are the two newest, highest-risk apps in
the codebase (demo layer, security-sensitive, financial data).

## Current tox.ini pylint line
```
pylint --load-plugins pylint_django -f colorized -rn --rcfile={toxinidir}/.pylintrc \
  user pipeline_engine core feedback market_data portfolio user_behavior ranking \
  client_ranking document_ranking ai access_guardian content_ingestion product_update customers
```

## Fix
Add `easy_button analytical` to the pylint and bandit commands:
```ini
commands =
  pipenv install --dev
  pytest --disable-warnings
  pylint --load-plugins pylint_django -f colorized -rn --rcfile={toxinidir}/.pylintrc \
    user pipeline_engine core feedback market_data portfolio user_behavior ranking \
    client_ranking document_ranking ai access_guardian content_ingestion product_update \
    customers easy_button analytical
  bandit -r .
```

## Files to Change
- `tox.ini` — add `easy_button analytical` to pylint scope

## Notes
- `bandit -r .` already covers everything recursively — no change needed there
- May need to add pylint disable comments for known false positives in easy_button
  (e.g., raw SQL with `pylint: disable=W0611` for the UserRateThrottle import)

## Acceptance Criteria
- [ ] `tox.ini` updated with easy_button + analytical in pylint scope
- [ ] `tox` passes locally without new pylint errors (or errors are fixed/suppressed)
- [ ] CI runs this on next PR
