# TODO-396: NarrativeReactor — Production Deployment

**Priority:** critical
**Repo:** NarrativeReactor
**Effort:** S (1 day)

## Description
NarrativeReactor is production-ready (Docker, CI, health checks) but has no CD pipeline or deployment config. Deploy to Railway, Fly.io, or GCP Cloud Run.

## Coding Prompt
```
Deploy NarrativeReactor at /data/workspace/projects/NarrativeReactor/ to production.

1. Create `.github/workflows/deploy.yml` — on push to main, build Docker image and deploy
2. Add Railway/Fly.io config (railway.toml or fly.toml) 
3. Set all required env vars in deployment platform
4. Verify health check at /health responds 200
5. Update README with live URL and deployment instructions
```

## Acceptance Criteria
- [ ] CD pipeline deploys on push to main
- [ ] /health endpoint returns 200 in production
- [ ] All env vars documented and set
- [ ] Live URL in README

## Dependencies
None — app is ready to deploy
