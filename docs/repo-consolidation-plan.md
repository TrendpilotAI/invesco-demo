# ForwardLane Repo Consolidation Plan

**Goal:** All source of truth in Bitbucket (`bitbucket.org/forwardlane/`). GitHub (`TrendpilotAI/`) used only for public demos or deprecated.

---

## Current State (Messy)

| What | Bitbucket (source of truth) | GitHub (TrendpilotAI/) | Status |
|---|---|---|---|
| Core Django Backend | `forwardlane/forwardlane-backend` (branch: `railway-deploy`) | `signal-studio-backend` | **GitHub has newer commits** — easy_button app, NL→SQL, security hardening |
| Signal Studio Frontend | `forwardlane/signal-studio` (branch: `main`) | `signal-studio-platform` + `signal-studio` | **Bitbucket is ahead** — Railway deploys from here |
| Signal Builder Backend | `forwardlane/signal-builder-backend` | `signal-builder-backend` | GitHub is a mirror, needs sync |
| Signal Builder Frontend | `forwardlane/signal-builder-frontend` | — | Bitbucket only ✅ |
| Entity Extraction | `forwardlane/core-entityextraction` (if exists) | `core-entityextraction` | **GitHub only** — needs Bitbucket repo |
| Data Provider | — | `signal-studio-data-provider` | **GitHub only** — needs Bitbucket repo |
| Auth Service | — | `signal-studio-auth` | **GitHub only** — needs Bitbucket repo |
| Signal Templates | — | `signal-studio-templates` | **GitHub only** — needs Bitbucket repo |
| Invesco Demo | — | `invesco-demo` (GH Pages) | GitHub only, OK (public demo site) |
| Docs | — | `honey-docs` (public) | GitHub only, OK (public docs) |

---

## Phase 1: Merge GitHub Changes → Bitbucket Branches (Day 1)

### 1.1 `forwardlane-backend` ← GitHub `signal-studio-backend`

The biggest gap. GitHub has these changes not in Bitbucket:

- `easy_button/` — entire Django app (views, urls, tests, permissions)
- `enrichment/` — data waterfall pipeline
- NL→SQL endpoint with Gemini + Kimi fallback
- Security hardening (rate limiting, SQL injection prevention)
- Celery health endpoint fix (just pushed)
- `Dockerfile.celery-worker` and `Dockerfile.celery-beat` updates
- `scripts/entrypoint.sh` service-aware entrypoint

**Action:**
```bash
cd /data/workspace/repos/forwardlane-backend
git checkout railway-deploy

# Add GitHub repo as remote (already exists as it was pushed from here)
# All easy_button changes are already on railway-deploy branch
# Verify:
git log --oneline -20
```

**Status:** Most changes are ALREADY on `railway-deploy` branch in Bitbucket. The branch just needs to be merged to `development` → `main` via Bitbucket PR.

### 1.2 `forwardlane/signal-studio` ← GitHub changes

GitHub repos `signal-studio-platform` and `signal-studio` have:
- TanStack React Query refactor (TODO-445)
- Rate limiting on Oracle query routes (TODO-385)
- Auth bypass for demo (our recent changes)

**Action:**
```bash
cd /data/workspace/repos/signal-studio
# Our changes are already pushed to Bitbucket main
# Verify with: git log --oneline -10 origin/main
```

**Status:** Changes are already on Bitbucket `main`. ✅

### 1.3 Create New Bitbucket Repos

These repos only exist on GitHub and need Bitbucket homes:

| New Bitbucket Repo | Source | Description |
|---|---|---|
| `forwardlane/signal-studio-data-provider` | `TrendpilotAI/signal-studio-data-provider` | Snowflake + Oracle data providers |
| `forwardlane/signal-studio-auth` | `TrendpilotAI/signal-studio-auth` | Auth service |
| `forwardlane/signal-studio-templates` | `TrendpilotAI/signal-studio-templates` | Signal template definitions |
| `forwardlane/core-entityextraction` | `TrendpilotAI/core-entityextraction` | Entity extraction (asyncpg) |

**Action (per repo):**
```bash
# 1. Create repo in Bitbucket (via UI or API)
# 2. Add Bitbucket as remote and push
cd /data/workspace/projects/<repo>
git remote add bitbucket https://x-token-auth:<BB_TOKEN>@bitbucket.org/forwardlane/<repo>.git
git push bitbucket --all
git push bitbucket --tags
```

**Nathan needs to:** Create these 4 repos in Bitbucket under the `forwardlane` workspace.

---

## Phase 2: Update Railway Service Configs (Day 1-2)

### Railway Project: "ForwardLane Signal Studio"

| Service | Current Source | Branch | Dockerfile | Healthcheck |
|---|---|---|---|---|
| Signal Studio | BB `signal-studio` | `main` | (Next.js default) | `/` ✅ |
| Django Backend | BB `forwardlane-backend` | `railway-deploy` | `Dockerfile.railway` | `/healthz` ✅ |
| Signal Builder API | BB `signal-builder-backend` | ? | ? | ? |
| Entity Extraction | ? (needs BB repo) | `main` | ? | ? |
| Celery Worker | BB `forwardlane-backend` | `railway-deploy` | `Dockerfile.celery-worker` | `/healthz` 🔧 (just fixed) |
| Celery Beat | BB `forwardlane-backend` | `railway-deploy` | `Dockerfile.celery-beat` | `/healthz` 🔧 (just fixed) |
| New Design | ? | ? | ? | ❌ FAILED — investigate |

### Actions:
1. ✅ **Celery Worker/Beat** — Just pushed health endpoint fix to Bitbucket, triggered redeploy
2. ❓ **New Design** — Need to investigate what this service is and why it's failing
3. ⬜ **Entity Extraction** — Once Bitbucket repo exists, update Railway to deploy from BB

---

## Phase 3: Clean Up GitHub Repos (Day 3)

Once all code is in Bitbucket:

1. **Archive** these GitHub repos (don't delete — keep for reference):
   - `TrendpilotAI/signal-studio-backend` → archived
   - `TrendpilotAI/signal-studio-platform` → archived
   - `TrendpilotAI/signal-studio` → archived
   - `TrendpilotAI/signal-builder-backend` → archived

2. **Keep active** on GitHub (public-facing):
   - `TrendpilotAI/invesco-demo` — GH Pages demo site
   - `TrendpilotAI/honey-docs` — public documentation

3. **Move to Bitbucket then archive on GitHub:**
   - `TrendpilotAI/signal-studio-data-provider`
   - `TrendpilotAI/signal-studio-auth`
   - `TrendpilotAI/signal-studio-templates`
   - `TrendpilotAI/core-entityextraction`

---

## Phase 4: Set Up Bitbucket → GitHub Mirroring (Optional)

If you want GitHub to stay in sync for visibility/CI:

```bash
# In each Bitbucket repo, add a post-push webhook or use Bitbucket Pipelines:
# bitbucket-pipelines.yml
pipelines:
  default:
    - step:
        name: Mirror to GitHub
        script:
          - git remote add github https://${GITHUB_TOKEN}@github.com/TrendpilotAI/${BITBUCKET_REPO_SLUG}.git
          - git push github --all --force
          - git push github --tags --force
```

---

## Local Workspace Cleanup

After consolidation, the local clones should be simplified:

| Keep | Path | Remote |
|---|---|---|
| ✅ | `/repos/forwardlane-backend` | BB `forwardlane/forwardlane-backend` |
| ✅ | `/repos/signal-studio` | BB `forwardlane/signal-studio` |
| ✅ | `/repos/signal-builder-backend` | BB `forwardlane/signal-builder-backend` |
| ❌ Remove | `/repos/signal-studio-backend` | Was GitHub mirror of forwardlane-backend |
| ❌ Remove | `/repos/github-signal-builder-backend` | Was GitHub mirror |
| ✅ | `/projects/forwardlane-backend` | BB (same as /repos, consolidate) |

**Duplicates to eliminate:**
- `/repos/forwardlane-backend` and `/projects/forwardlane-backend` are the same repo cloned twice
- `/repos/signal-studio-backend` is a fork of `forwardlane-backend` — merge and delete

---

## Summary of What Nathan Needs To Do

1. **Create 4 Bitbucket repos** under `forwardlane/`:
   - `signal-studio-data-provider`
   - `signal-studio-auth`
   - `signal-studio-templates`
   - `core-entityextraction`

2. **Merge PR** in `forwardlane-backend`: `railway-deploy` → `development` (all the easy_button + celery fixes)

3. **Investigate "New Design"** Railway service — what is it?

4. **Decide** on GitHub: archive mirrors or set up Bitbucket→GitHub mirroring?

Everything else I can do myself once the repos exist. 🍯
