# TODO-878: Fix Bitbucket Pipeline REACT_APP_* → VITE_* Env Vars

**Repo:** signal-builder-frontend  
**Priority:** P1 (Critical)  
**Effort:** XS (1-2 hours)  
**Status:** pending

## Problem

After the Vite migration (TODO-326), `bitbucket-pipelines.yml` still injects environment variables with the `REACT_APP_*` prefix. Vite ignores these — only `VITE_*` prefixed vars are exposed to the browser bundle. This means **all deployed environments (demo, qa) are running with undefined API URLs** — the app cannot connect to any backend.

Evidence: `.env.example` uses `VITE_API_BASE_URL`, `VITE_API_BASE_PATH`, etc. Pipeline uses `REACT_APP_API_BASE_URL`, `REACT_APP_API_BASE_PATH`, etc.

## Files to Change

- `bitbucket-pipelines.yml` — rename all `REACT_APP_*` vars to `VITE_*` in both `demo:` and `qa:` pipeline steps

## Coding Prompt

```
In /data/workspace/projects/signal-builder-frontend/bitbucket-pipelines.yml:

For BOTH the `demo:` and `qa:` pipeline step `.env.local` generation blocks, rename:
  REACT_APP_IS_DEV_AUTH_METHOD  → VITE_IS_DEV_AUTH_METHOD
  REACT_APP_API_BASE_PATH       → VITE_API_BASE_PATH
  REACT_APP_API_BASE_URL        → VITE_API_BASE_URL
  REACT_APP_FORWARDLANE_URL     → VITE_FORWARDLANE_URL
  REACT_APP_AUTH_COOKIE_DOMAIN  → VITE_AUTH_COOKIE_DOMAIN
  REACT_APP_FL_API_URL          → VITE_FL_API_URL

Verify that APP_CONFIG in src/shared/config/ reads from the VITE_* names.
Cross-reference with .env.example to ensure all variable names match exactly.
```

## Acceptance Criteria
- [ ] All `REACT_APP_*` replaced with `VITE_*` in pipeline YAML
- [ ] Variable names match `.env.example` exactly
- [ ] Local dev test: run `yarn build` with a `.env.local` using `VITE_*` names — app connects to API
- [ ] Verify `APP_CONFIG` reads `import.meta.env.VITE_*` not `process.env.REACT_APP_*`
