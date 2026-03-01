# TODO-354: CI Security Pipeline (pip-audit + bandit + mypy)
**Project:** signal-builder-backend  
**Priority:** P0  
**Effort:** S (0.5–1 day)  
**Status:** pending  
**Created:** 2026-03-01

---

## Description

The Bitbucket pipeline lacks security scanning and type checking. `pip-audit`, `bandit`, and `mypy` are already in dev dependencies — they just need to be wired into the CI pipeline. This is a high-leverage change: one PR to add a `security-checks` step that runs on every future PR, preventing CVE regressions and type drift.

---

## Full Autonomous Coding Prompt

```
You are working on the signal-builder-backend FastAPI service at /data/workspace/projects/signal-builder-backend/.

TASK: Add security-checks step to Bitbucket Pipelines CI.

STEP 1 — Read the current pipeline config:
```
cat /data/workspace/projects/signal-builder-backend/bitbucket-pipelines.yml
```

STEP 2 — Verify dev tools are available:
```
grep -E "pip-audit|bandit|mypy" /data/workspace/projects/signal-builder-backend/Pipfile
```
If any are missing, add them:
```
pipenv install --dev pip-audit bandit mypy
```
Add to Pipfile [dev-packages]:
```
pip-audit = "*"
bandit = ">=1.7"
mypy = ">=1.0"
```

STEP 3 — Add a security-checks step to bitbucket-pipelines.yml.

The new step should be added to the `pull-requests` section (or create one if absent) and also to the default pipeline. Insert this step:

```yaml
- step:
    name: Security & Type Checks
    image: python:3.11
    caches:
      - pip
    script:
      - pip install pipenv
      - pipenv install --dev
      # Dependency vulnerability scan
      - pipenv run pip-audit --strict
      # Security static analysis (medium+ severity)
      - pipenv run bandit -r apps/ core/ -ll -x apps/*/tests/,apps/*/test_*
      # Type checking
      - pipenv run mypy apps/ core/ --ignore-missing-imports --no-error-summary
```

STEP 4 — If bitbucket-pipelines.yml has a `pull-requests` section, add the step there:
```yaml
pull-requests:
  '**':
    - step:
        name: Tests
        ...  # existing test step
    - step:
        name: Security & Type Checks
        ...  # new step above
```

If only a `default` pipeline exists, add it there and add a `pull-requests` section.

STEP 5 — Create a local script for running security checks manually:
File: `scripts/security_check.sh`
```bash
#!/bin/bash
set -e

echo "=== pip-audit: Dependency CVE Scan ==="
pipenv run pip-audit

echo "=== bandit: Security Static Analysis ==="
pipenv run bandit -r apps/ core/ -ll -x "apps/*/tests/,apps/*/test_*"

echo "=== mypy: Type Checking ==="
pipenv run mypy apps/ core/ --ignore-missing-imports

echo "=== All security checks passed! ==="
```
```
chmod +x scripts/security_check.sh
```

STEP 6 — Create mypy configuration in pyproject.toml or mypy.ini:
File: `mypy.ini` (or add `[mypy]` section to existing config):
```ini
[mypy]
python_version = 3.11
ignore_missing_imports = True
warn_return_any = False
warn_unused_configs = True
exclude = (migrations/|scripts/one_time_scripts/)

[mypy-celery.*]
ignore_missing_imports = True

[mypy-dependency_injector.*]
ignore_missing_imports = True
```

STEP 7 — Run checks locally to establish baseline:
```
cd /data/workspace/projects/signal-builder-backend
bash scripts/security_check.sh 2>&1 | tee security-baseline.txt
cat security-baseline.txt
```
Document any pre-existing issues found — these are technical debt to address separately.

STEP 8 — If pip-audit finds CVEs, create a separate issue list:
```
pipenv run pip-audit --format=json > security-audit-results.json
cat security-audit-results.json
```
Add a `## Known CVE Debt` section to AUDIT.md with the findings and plan to fix.

STEP 9 — If bandit finds issues, assess and either fix or add to `.bandit` ignore file for false positives:
```
pipenv run bandit -r apps/ core/ -ll -f json > bandit-results.json
```
Review findings and either fix them or create a `.bandit` file with legitimate exceptions.

STEP 10 — Commit everything:
```
git add bitbucket-pipelines.yml mypy.ini scripts/security_check.sh
git commit -m "ci: add security checks step (pip-audit, bandit, mypy)"
```
```

---

## Dependencies

- None — can run independently
- Complements TODO-352 (Pydantic migration) — mypy will catch type issues introduced during migration

---

## Effort Estimate

**0.5–1 day** — Tools already in dev deps. Main work is YAML editing and handling baseline findings. If there are many mypy errors, this could extend to 2 days to fix them.

---

## Acceptance Criteria

- [ ] `bitbucket-pipelines.yml` has a `Security & Type Checks` step
- [ ] Step runs on every pull request (not just default branch)
- [ ] `pip-audit` runs and exits non-zero on new CVEs
- [ ] `bandit -r apps/ core/ -ll` runs — medium+ severity findings fail the build
- [ ] `mypy apps/ core/ --ignore-missing-imports` runs
- [ ] `scripts/security_check.sh` exists and is executable
- [ ] `mypy.ini` configured with appropriate ignores for third-party libs
- [ ] Pipeline passes on a test PR with no new security issues
