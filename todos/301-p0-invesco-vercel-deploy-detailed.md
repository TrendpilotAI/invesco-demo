Title: 301 — Invesco demo: Vercel deploy (P0)
Repo: invesco-retention
Priority: P0
Owner: Nathan + Honey
Estimated effort: 1-2 hours

Description:
Deploy the invesco-retention demo to a public Vercel URL. Ensure build passes, environment variables are configured, and demo backend endpoints (if any) are reachable. Produce a 2–3 minute Loom smoke-test recording showing main flows.

Acceptance criteria:
- Public HTTPS URL available and reachable
- Demo pages (Salesforce embed, Dashboard, Signal Creation, Mobile) load without console errors
- Smoke-test Loom uploaded and link added to /data/workspace/projects/invesco-retention/docs/
- CI build passes on Vercel

Dependencies:
- GitHub repo: trendpilotai/invesco-demo (confirm remote)
- Vercel account and project, deployment token or Nathan's confirmation to trigger
- Any required environment variables (LIST in /data/workspace/projects/invesco-retention/.env.example)

Execution steps / Agent-executable prompt:
1. Verify repo builds locally: yarn && yarn build (or npm ci && npm run build)
2. Create Vercel project (if missing) using Vercel CLI or UI; set env vars from .env.example (ask Nathan for secrets)
3. Trigger deployment and wait for build success
4. Run a smoke test (curl the homepage, check console errors via headless browser) and record Loom demo
5. Add public URL and Loom links to /data/workspace/projects/invesco-retention/docs/DEPLOY.md

Verification tests:
- curl -sSf https://<vercel-url>/ returns 200
- No JS console errors in headless Playwright run

Notes:
- Do NOT publish any secrets in repo. Use Vercel environment variables.
- If Nathan prefers Railway or Netlify, adapt steps accordingly.
