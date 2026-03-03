# TODO 432 — Add Railway Auto-Deploy to GitHub Actions CI

**Priority:** MEDIUM  
**Repo:** NarrativeReactor  
**Effort:** 2 hours  
**Status:** pending

## Description
GitHub Actions CI is now set up (typecheck, lint, test, docker-build) but doesn't auto-deploy to Railway on main branch pushes.

## Task

1. Add Railway deploy step to `.github/workflows/ci.yml`:
```yaml
- name: Deploy to Railway
  if: github.ref == 'refs/heads/main' && success()
  run: |
    npm install -g @railway/cli
    railway up --service narrative-reactor
  env:
    RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
```

2. Add `RAILWAY_TOKEN` to GitHub repo secrets
3. Add staging deploy on `develop` branch push
4. Add deploy status badge to README.md

## Acceptance Criteria
- [ ] Main branch push auto-deploys to Railway production
- [ ] Develop branch push deploys to Railway staging
- [ ] Deploy failure sends notification
- [ ] README shows deploy status badge

## Dependencies
- Requires Railway service already configured (railway.json exists ✓)
- Requires RAILWAY_TOKEN from Nathan
