# TODO-827: Add Dockerfile + docker-compose to signal-studio-auth

**Repo:** signal-studio-auth  
**Priority:** P0 (Critical)  
**Effort:** 1 hour  
**Status:** pending

## Task
Create Dockerfile (multi-stage), docker-compose.yml with redis service, and .env.example.

## Acceptance Criteria
- [ ] `docker build` succeeds
- [ ] `docker-compose up` starts app + redis
- [ ] `/health` returns 200
- [ ] All env vars documented in `.env.example`
