# TODO 004 — Ultrafone: E2E Railway Deployment & Twilio Validation

**Status:** pending  
**Priority:** high  
**Project:** Ultrafone  
**Created:** 2026-02-26

---

## Overview

Deploy Ultrafone backend to Railway in production mode and validate the full call flow end-to-end using a real Twilio phone number. Currently Phase 2 is committed but has never been tested in a live production environment. This is the critical blocker before Nathan can actually use the system.

---

## Coding Prompt

```
You are a deployment agent for the Ultrafone project at /data/workspace/projects/Ultrafone/

Your task is to prepare and validate a Railway production deployment:

1. Review the current deployment config:
   - /data/workspace/projects/Ultrafone/railway.toml
   - /data/workspace/projects/Ultrafone/nixpacks.toml
   - /data/workspace/projects/Ultrafone/Dockerfile

2. Check that all required environment variables are documented:
   Review backend/main.py and backend/config/settings.py for all os.getenv() calls.
   Produce a complete .env.production.template file at the repo root with every variable and its purpose.

3. Validate Twilio webhook configuration:
   - The webhook URL should point to https://<railway-domain>/twilio/voice
   - Check that /data/workspace/projects/Ultrafone/backend/api/routes/calls.py and main.py handle Twilio's POST format correctly
   - Add Twilio webhook signature validation using twilio.request_validator.RequestValidator

4. Run the backend test suite to ensure passing state:
   cd /data/workspace/projects/Ultrafone/backend
   pip install -r requirements.txt --quiet
   python -m pytest tests/ -x -q 2>&1 | tail -20

5. Create a deployment runbook at /data/workspace/projects/Ultrafone/DEPLOY_RUNBOOK.md with:
   - Step-by-step Railway deployment instructions
   - Required env vars checklist
   - Twilio webhook configuration steps
   - Health check validation commands
   - Rollback procedure

6. Document any failing tests or missing configurations in the runbook.
```

---

## Dependencies

- None (first task in sequence)

---

## Effort

**Estimate:** 3-4 hours  
**Type:** Infrastructure / DevOps

---

## Acceptance Criteria

- [ ] `.env.production.template` created with all required variables documented
- [ ] Twilio webhook signature validation implemented in `/twilio/voice` endpoint
- [ ] All unit tests pass (`pytest tests/ -x`)
- [ ] `DEPLOY_RUNBOOK.md` created with complete deployment instructions
- [ ] Railway health check endpoint (`/health`) returns 200
