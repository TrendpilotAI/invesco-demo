---
id: 642
status: pending
priority: P2
repo: signal-studio-templates
title: Deploy demo environment for Invesco
effort: S (1 day)
dependencies: [634, 635, 636]
---

# Demo Deployment for Invesco

## Problem
No hosted demo environment exists. Craig Lieb / Invesco team need a URL to point at.

## Task
Deploy Signal Studio Templates API + Gallery to Railway with MockDataProvider and real OpenAI for talking points.

## Coding Prompt
```
In /data/workspace/projects/signal-studio-templates/:

1. Create src/demo-server.ts:
   - Express app using createTemplateRouter(mockDataProvider, openaiAIProvider)
   - Serves template-gallery.tsx as a static React app at GET /
   - Uses MockDataProvider (TODO-635) + OpenAIAIProvider (TODO-634)
   - PORT from env, default 3000
   - Add health check: GET /health → { status: "ok", templates: 20 }

2. Create Dockerfile:
   FROM node:20-alpine
   WORKDIR /app
   COPY . .
   RUN pnpm install --frozen-lockfile
   RUN pnpm build
   CMD ["node", "dist/src/demo-server.js"]

3. Create railway.json:
   { "build": { "builder": "DOCKERFILE" }, "deploy": { "healthcheckPath": "/health" } }

4. Create .env.example with:
   OPENAI_API_KEY=
   JWT_SECRET=
   PORT=3000

5. Document deployment in README.md under "Demo Deployment" section

Environment: Railway (railway.app)
Subdomain target: templates-demo.forwardlane.com (CNAME Railway URL)
```

## Acceptance Criteria
- [ ] `src/demo-server.ts` starts a working Express app
- [ ] Dockerfile builds and container starts cleanly
- [ ] `GET /health` returns 200
- [ ] All 20 templates execute with MockDataProvider
- [ ] Talking points generate via OpenAI AIProvider
- [ ] README documents Railway deployment steps
