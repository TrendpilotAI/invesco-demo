# 211 — Invesco Retention: Deploy to Vercel (P0)

**Priority:** 🔴 P0 — BLOCKS EVERYTHING  
**Project:** invesco-retention  
**Effort:** XS (15 min)  
**Owner:** Honey  
**Dependencies:** None — this is the root task

---

## Task Description

Deploy the invesco-retention demo-app to Vercel production. The app is a Next.js 16 application with all static mock data — no environment variables required. The deploy path is confirmed clean.

A public HTTPS URL must be live before any other work (branding patches, outreach, recordings) can begin. This is the single most critical action in the entire Invesco retention effort.

---

## Coding Prompt (Agent-Executable)

```
You are deploying the invesco-retention demo app to Vercel production.

REPO: /data/workspace/projects/invesco-retention/demo-app

Steps:
1. cd /data/workspace/projects/invesco-retention/demo-app
2. Run: npm run build
   - Confirm build succeeds with 0 errors
   - If TypeScript errors appear, fix them (likely type mismatches in mock data)
3. Run: npx vercel --prod
   - Follow prompts: project name = "signal-studio-invesco" (or similar)
   - Scope: ForwardLane team account if available, else personal
   - No environment variables needed
4. Copy the production URL from Vercel output
5. Write the URL to /data/workspace/projects/invesco-retention/DEPLOY_URL.md
6. Test the URL: curl -I <url> should return 200
7. Open each route and confirm it loads:
   - / (home/landing)
   - /salesforce (Salesforce embed view)
   - /signals (signal creation)
   - /territory (territory dashboard)
   - /mobile (mobile PWA view, or check /mobile-pwa separately)

If Vercel CLI isn't installed: npm i -g vercel
If login required: vercel login (will open browser)

Report: The production URL, build output summary, and any errors encountered.
```

---

## Acceptance Criteria
- [ ] `npm run build` exits 0
- [ ] `npx vercel --prod` completes successfully
- [ ] Production URL is live and returns HTTP 200
- [ ] All 4 demo routes are accessible
- [ ] URL written to `/data/workspace/projects/invesco-retention/DEPLOY_URL.md`
- [ ] Mobile PWA accessible via HTTPS (required for service worker)
