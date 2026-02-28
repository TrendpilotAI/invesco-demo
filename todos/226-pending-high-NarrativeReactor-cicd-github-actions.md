# 226 · NarrativeReactor · CI/CD Pipeline (GitHub Actions)

**Status:** pending  
**Priority:** high  
**Project:** NarrativeReactor  
**Created:** 2026-02-27

---

## Task Description

NarrativeReactor has no CI/CD pipeline. Tests exist (`vitest`) but run manually. Add GitHub Actions workflows for: PR checks (lint + test), main branch build + deploy to Railway or Cloud Run, and nightly dependency audits.

---

## Coding Prompt (agent-executable)

```
Working in /data/workspace/projects/NarrativeReactor/:

1. Create .github/workflows/ci.yml — PR gate:
   - Trigger: pull_request to main
   - Jobs:
     a. lint: npm ci, npm run typecheck (tsc --noEmit), eslint
     b. test: npm ci, npm run test:ci (vitest --reporter=verbose --coverage)
     c. build: npm ci, npm run build
   - Cache: node_modules via actions/cache with package-lock.json hash
   - Upload coverage to Codecov (optional, add CODECOV_TOKEN secret)

2. Create .github/workflows/deploy.yml — deploy on merge to main:
   - Trigger: push to main
   - Needs: ci workflow pass (via workflow_run or jobs dependency)
   - Job: deploy-railway
     - Uses: railwayapp/github-action@latest OR curl Railway API to trigger deploy
     - Env secrets: RAILWAY_TOKEN, RAILWAY_SERVICE_ID
   - Add Slack/Discord notification on success/failure (webhook secret)

3. Create .github/workflows/security.yml — nightly security scan:
   - Trigger: schedule cron '0 2 * * *'
   - Run: npm audit --audit-level=moderate
   - Run: npx snyk test OR trivy fs (if docker available)
   - Create GitHub issue on failures using gh CLI

4. Add package.json scripts:
   - "typecheck": "tsc --noEmit"
   - "lint": "eslint src --ext .ts"
   Install eslint + @typescript-eslint if not present

5. Create .github/PULL_REQUEST_TEMPLATE.md with checklist

6. Add GitHub Actions badge to README.md
```

---

## Dependencies

- 223 (Docker hardening — for deploy workflow)

## Effort Estimate

4–5 hours

## Acceptance Criteria

- [ ] PR CI runs in < 5 minutes
- [ ] Failed tests block merge
- [ ] Deploy triggers automatically on main merge
- [ ] Security audit runs nightly and creates issues on failures
- [ ] Lint enforced on all .ts files
