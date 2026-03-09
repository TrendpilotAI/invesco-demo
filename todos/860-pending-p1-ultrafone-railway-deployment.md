# 860 — Deploy Ultrafone Backend to Railway

**Priority:** P1  
**Repo:** Ultrafone  
**Effort:** 4 hours  
**Depends on:** 858, 859 (secrets must be clean first)

## Description
Deploy the FastAPI backend to Railway using the existing `railway.toml` and `nixpacks.toml`. Provision PostgreSQL and Redis add-ons. Wire Twilio webhook to Railway URL.

## Steps
```bash
cd /data/workspace/projects/Ultrafone
railway init
railway add --database postgresql
railway add --database redis
# Set all environment variables via railway CLI or dashboard
railway up

# Configure Twilio webhook
twilio phone-numbers:update +19129129545 \
  --voice-url=https://<app>.railway.app/twilio/voice
```

## Acceptance Criteria
- [ ] Backend healthy at Railway URL
- [ ] `/health` endpoint returns 200
- [ ] Test call flow works end-to-end
- [ ] Sentry error tracking active
