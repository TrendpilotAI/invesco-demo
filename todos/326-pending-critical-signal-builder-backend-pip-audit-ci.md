# Add pip-audit to CI + Fix CVEs

**Repo:** signal-builder-backend  
**Priority:** critical  
**Effort:** S (2-3 hours)  
**Phase:** 0

## Problem
Several outdated packages with known CVEs: aiohttp 3.8.6, pydantic 1.10.13 (EOL), fastapi 0.92. `pip-audit` is in dev deps but not run in CI.

## Task
1. Run `pip-audit` locally and document all findings
2. Add `pip-audit` step to `bitbucket-pipelines.yml`
3. Upgrade `aiohttp` to 3.11+ (CVE fixes) immediately
4. Document remaining CVEs with upgrade plan

## Acceptance Criteria
- `pip-audit` runs in CI and fails build on HIGH CVEs
- aiohttp upgraded to latest stable
- All HIGH CVEs resolved or documented with timeline
