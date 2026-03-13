# INV-014: GitHub Actions Auto-Deploy — DONE ✅

**Completed:** 2026-03-13
**Priority:** P1/Small
**Commit:** 4751f68 on main branch

## What Was Built

### `.github/workflows/deploy.yml`
- **Trigger:** Push to `main` branch + manual `workflow_dispatch`
- **Build steps:**
  1. Checkout repository
  2. Setup Node.js 20 with npm cache
  3. `npm install` (in `projects/invesco-retention/demo-app/`)
  4. `npm run build` (Next.js static export → `out/` directory)
  5. Deploy `out/` to `gh-pages` branch via `peaceiris/actions-gh-pages@v4`
- **Concurrency:** Cancels in-progress deploys on new push
- **Commit message:** Includes SHA and commit message for traceability

### Workflow Location
`.github/workflows/deploy.yml`

### How It Works
Any push to `main` automatically:
1. Installs dependencies
2. Builds the Next.js app with `output: 'export'` + `basePath: '/invesco-demo'`
3. Deploys built files to `gh-pages` branch
4. GitHub Pages serves from `gh-pages` branch at https://trendpilotai.github.io/invesco-demo/

### Also Added (Required for Build)
- `projects/invesco-retention/demo-app/next.config.ts` — `output: 'export'`, basePath, trailingSlash
- `projects/invesco-retention/demo-app/tsconfig.json` — TypeScript config with `@/*` path alias
- `projects/invesco-retention/demo-app/postcss.config.js` — Tailwind v4 PostCSS config

## First Manual Deploy
Built and deployed manually via git push to `gh-pages` branch (commit 93a30a8).
Future deploys will be automatic via GitHub Actions.

## Live Site
https://trendpilotai.github.io/invesco-demo/
