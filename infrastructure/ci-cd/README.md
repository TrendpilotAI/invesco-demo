# CI/CD Pipeline

Unified CI/CD setup for all projects.

## GitHub Actions

Each project has `.github/workflows/ci.yml` that runs on push/PR to `main`:

| Project | Steps |
|---------|-------|
| **Second-Opinion** | lint (tsc --noEmit) → build (tsc + vite) → test |
| **flip-my-era** | lint (eslint) → typecheck → test:ci → build |
| **NarrativeReactor** | build (tsc) → test:ci |
| **Trendpilot** | build (tsc) → test |

All use **Node 22** with npm caching.

## Dependabot

Each project has `.github/dependabot.yml` — weekly npm dependency updates, max 10 open PRs.

## Scripts

### Deploy

```bash
./infrastructure/ci-cd/deploy.sh <project-name>
```

Builds and deploys:
- **Second-Opinion** → Firebase Hosting
- **NarrativeReactor** → Firebase Functions
- **flip-my-era / Trendpilot** → Railway

### Rollback

```bash
./infrastructure/ci-cd/rollback.sh <project-name> [commit-sha]
```

Reverts the last commit (or to a specific SHA) via `git revert`. Run `deploy.sh` after to redeploy.
