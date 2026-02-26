# CI/CD Status Report — 2026-02-18

## Repository Status

| Repository | CI Workflow | Dependabot | Last Run | Status |
|---|---|---|---|---|
| TrendpilotAI/flip-my-era | ✅ ci.yml | ✅ | Dependabot PR | ❌ Failure |
| TrendpilotAI/Second-Opinion | ✅ ci.yml + deploy + modal-deploy + staging | ✅ | CI | ❌ Failure |
| TrendpilotAI/NarrativeReactor | ✅ ci.yml | ✅ | CI | ❌ Failure |
| TrendpilotAI/Trendpilot | ✅ ci.yml | ✅ | CI | ❌ Failure |
| TrendpilotAI/railway-saas-template | ✅ ci.yml (NEW) | ✅ (NEW) | Dependabot PR | ✅ Success |
| TrendpilotAI/forwardlane-website | ✅ ci.yml (NEW) | ✅ (NEW) | — | 🆕 Just added |
| TrendpilotAI/signalhaus-website | ✅ ci.yml (NEW) | ✅ (NEW) | — | 🆕 Just added |

## Actions Taken

- **Added CI workflows** to: `railway-saas-template`, `forwardlane-website`, `signalhaus-website`
- **Added Dependabot config** to: `railway-saas-template`, `forwardlane-website`, `signalhaus-website`
- All 3 repos pushed to `main` — CI will trigger automatically

## Failing Repos (Pre-existing)

The following repos have CI but their last runs failed:
- **flip-my-era** — Dependabot update failure
- **Second-Opinion** — CI failure
- **NarrativeReactor** — CI failure  
- **Trendpilot** — CI failure

These failures predate this work and may need investigation.

## n8n Instance Status

- **URL:** https://primary-production-4244.up.railway.app
- **Status:** ✅ **Online** (HTTP 200, 127ms response)
- **Health endpoint:** `/healthz` returns `{"status":"ok"}`
- **Version:** n8n v2.8.3
- **Environment:** development (per Sentry config)

## Security Notes

- `railway-saas-template` has 3 Dependabot security alerts (2 high, 1 moderate)
  - See: https://github.com/TrendpilotAI/railway-saas-template/security/dependabot
