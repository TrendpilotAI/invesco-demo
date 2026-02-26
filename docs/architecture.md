# Architecture — OpenClaw Infrastructure

## Service Map

| Service | Type | URL | Status |
|---------|------|-----|--------|
| **OpenClaw** | Agent Runtime | localhost | Running |
| **n8n** | Workflow Automation | https://primary-production-4244.up.railway.app | Online (200) |
| **Postiz** | Social Scheduler | https://postiz-production-6189.up.railway.app | Down (502) |
| **FlipMyEra** | Web App | https://flipmyera.com | Deployed (Netlify) |
| **NarrativeReactor** | AI Pipeline | Modal GPU → Firebase | Built (122 tests) |
| **Trendpilot** | Trend Aggregation | — | Built (133 tests) |
| **Second-Opinion** | Medical AI | Firebase | Building |

## Railway Architecture

### Databases

**PostgreSQL**
- Host: `postgres.railway.internal:5432`
- Database: `railway`
- User: `postgres`
- Used by: n8n, Postiz

**Redis**
- Internal: `redis.railway.internal:6379`
- External: `trolley.proxy.rlwy.net:11973`
- Used by: Postiz (queue/cache), n8n (optional)

### Deployed Services (Railway)

1. **n8n** — Workflow automation engine
   - Connected to Postgres for workflow storage
   - Runs automated workflows (viral video pipeline, social posting)
   - Integrates with Blotato API for cross-platform posting

2. **Postiz** — Social media scheduling
   - Connected to Postgres + Redis
   - HTTP 502 as of 2026-02-17 — needs investigation
   - Likely Redis connection or memory issue

### External Deployments

3. **FlipMyEra** — Netlify
   - Static site + serverless functions
   - 183 tests passing
   - Domain: flipmyera.com

4. **NarrativeReactor** — Multi-cloud
   - Modal (GPU inference)
   - Google Cloud Functions (orchestrator)
   - Firestore (real-time status)
   - React frontend (pipeline UI)
   - Flow: `Modal GPU → Cloud Function → Firestore → React Hook → UI`

5. **Second-Opinion** — Firebase
   - Firebase Hosting + Cloud Functions
   - Competition entry — under active development

6. **Trendpilot** — Local/CI
   - Zod models, aggregator sources (News API, RSS, Reddit)
   - Deduplicator, ranker, orchestrator
   - 133 tests, 5-phase TDD plan

## Inter-Service Communication

```
n8n ──→ Blotato API ──→ Social platforms
n8n ──→ Postgres (workflow state)
Postiz ──→ Postgres (scheduling data)
Postiz ──→ Redis (job queue, cache)
NarrativeReactor: Modal ──→ Cloud Function ──→ Firestore ──→ React
OpenClaw ──→ n8n (API triggers)
OpenClaw ──→ Redis (external proxy for debugging)
```

## Deployment Instructions

### n8n (Railway)
Already deployed. Redeploy via Railway dashboard or `railway up` from n8n service directory.

### Postiz (Railway)
Deployed but returning 502. Check Railway logs:
- Possible Redis connection timeout
- Possible OOM (check memory usage)
- Restart via Railway dashboard

### FlipMyEra (Netlify)
```bash
cd projects/flipmyera
npm run build
netlify deploy --prod
```

### NarrativeReactor
```bash
# Deploy Modal functions
modal deploy

# Deploy Cloud Functions
cd functions && firebase deploy --only functions

# Deploy frontend
firebase deploy --only hosting
```

### Second-Opinion (Firebase)
```bash
cd projects/second-opinion
firebase deploy
```
