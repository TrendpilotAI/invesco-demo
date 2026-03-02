# TODO 418: GitHub Actions CI Pipeline

**Repo:** Ultrafone  
**Priority:** High  
**Effort:** S (2-3 hours)  
**Dependencies:** None

## Description
No CI/CD pipeline exists. Add GitHub Actions for lint, test, and deploy on PR/push.

## Coding Prompt
```
1. Create .github/workflows/ci.yml:
   - Trigger: push to main, pull_request
   - Jobs:
     a. backend-test: Python 3.11, pip install, ruff lint, pytest with coverage
     b. frontend-build: bun install, eslint, bun run build
     c. security-audit: pip-audit on backend requirements
   
2. Create .github/workflows/deploy.yml:
   - Trigger: push to main only
   - Deploy to Railway using RAILWAY_TOKEN secret
   
3. Add ruff.toml config for Python linting
4. Add pre-commit config: .pre-commit-config.yaml with ruff, eslint, trailing-whitespace
5. Add pytest coverage threshold (80%) to fail CI on coverage drop
6. Add status badges to README.md
```

## Acceptance Criteria
- CI passes on clean repo state
- Failed tests block PR merge
- Auto-deploy to Railway on main push
- Coverage report visible in PRs
