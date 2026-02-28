# 223 · NarrativeReactor · Docker Deployment Hardening

**Status:** pending  
**Priority:** high  
**Project:** NarrativeReactor  
**Created:** 2026-02-27

---

## Task Description

NarrativeReactor has no Dockerfile or container strategy. The app runs on Firebase App Hosting / Cloud Run per docs, but there's no containerised local/staging path. Add production-grade Docker support with multi-stage build, health check, and Railway/Cloud Run deployment config.

---

## Coding Prompt (agent-executable)

```
Working in /data/workspace/projects/NarrativeReactor/:

1. Create a multi-stage Dockerfile:
   - Stage 1 (builder): node:20-alpine, copy package*.json, npm ci --omit=dev, copy src/, npm run build
   - Stage 2 (runner): node:20-alpine, copy dist/ and node_modules from builder, expose port 3401
   - Add HEALTHCHECK CMD curl -f http://localhost:3401/health || exit 1
   - Run as non-root user (uid 1001)

2. Create .dockerignore:
   node_modules, dist, .env*, *.log, coverage, site, docs

3. Create railway.toml:
   [build]
   builder = "dockerfile"
   [deploy]
   healthcheckPath = "/health"
   healthcheckTimeout = 30
   restartPolicyType = "on_failure"

4. Update src/index.ts health endpoint to include:
   - uptime
   - memory usage
   - version from package.json
   - timestamp

5. Create scripts/docker-build.sh — convenience wrapper for local image build + run.

6. Add `docker:build` and `docker:run` npm scripts to package.json.
```

---

## Dependencies

- None (foundational)

## Effort Estimate

3–4 hours

## Acceptance Criteria

- [ ] `docker build -t narrativereactor .` succeeds
- [ ] Container starts, `/health` returns 200 with uptime/version
- [ ] Railway deployment config validates (`railway up --dry-run`)
- [ ] Image runs as non-root user
- [ ] .dockerignore keeps image < 500 MB
