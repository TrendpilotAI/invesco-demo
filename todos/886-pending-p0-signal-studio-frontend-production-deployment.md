# TODO-886: Production Deployment — Vercel/GCP Cloud Run

**Repo:** signal-studio-frontend  
**Priority:** P0  
**Effort:** M (3-5 hours)  
**Status:** pending  
**Identified:** 2026-03-10 by Judge Agent v2

## Description

Signal Studio is functionally complete (completeness=7) but has NO production deployment.
Zero revenue is possible without a live URL. The app has `railway.json` and `Dockerfile` present,
suggesting Railway deployment was explored. Vercel is the recommended target for Next.js.

## Deployment Checklist

### Pre-requisites
- [ ] Fix auth API bypass (TODO-885) before going live
- [ ] Set up all environment variables in deployment platform
- [ ] Add `/api/health` endpoint for uptime monitoring

### Environment Variables Required
```
# Supabase
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=

# Oracle 23ai
ORACLE_USER=
ORACLE_PASSWORD=
ORACLE_CONNECTION_STRING=
ORACLE_WALLET_PATH=  # if using Oracle Wallet auth

# AI Providers
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
GOOGLE_AI_API_KEY=
OPENROUTER_API_KEY=

# App Config
NEXTAUTH_SECRET=
NEXTAUTH_URL=https://signalstudio.signalhaus.ai
NODE_ENV=production
```

## Coding Prompt

```
In /data/workspace/projects/signal-studio-frontend/:

STEP 1: Add health check endpoint
Create app/api/health/route.ts:
  import { NextResponse } from 'next/server'
  export async function GET() {
    return NextResponse.json({
      status: 'ok',
      timestamp: new Date().toISOString(),
      version: process.env.npm_package_version || '0.1.0'
    })
  }

STEP 2: Verify next.config.mjs is production-ready
- Ensure no localhost URLs hardcoded
- Add output: 'standalone' for Docker deployments (already present?)
- Add security headers in headers() config

STEP 3: Set up Vercel project
- Link Bitbucket repo to Vercel project
- Configure environment variables in Vercel dashboard
- Set Node.js version to 22.x
- Configure custom domain: signalstudio.signalhaus.ai

STEP 4: Add deploy step to bitbucket-pipelines.yml
Add after test step (main branch only):
  - step:
      name: Deploy to Production (Vercel)
      condition:
        changesets:
          includePaths:
            - "**"
      script:
        - npx vercel --prod --token $VERCEL_TOKEN

STEP 5: Verify Oracle connectivity from Vercel
Oracle 23ai with Wallet auth requires the wallet files to be accessible.
Options:
  - Upload wallet to Vercel (via secret file or env var base64)
  - Use Oracle connection string directly (no wallet) if network allows
  - Consider Railway instead (Docker-native, wallet files easier to include)

STEP 6: Set up monitoring
- Connect Sentry (TODO-887) post-deploy
- Set up Vercel Analytics
- Add uptime monitoring via Better Uptime or UptimeRobot pointing to /api/health
```

## Acceptance Criteria
- [ ] Live URL accessible at signalstudio.signalhaus.ai (or staging subdomain)
- [ ] All environment variables configured in production
- [ ] `/api/health` returns `{ "status": "ok" }`
- [ ] Supabase auth flow works in production
- [ ] Oracle DB connection works in production
- [ ] AI chat (at least one model) works in production
- [ ] Bitbucket pipeline auto-deploys on push to main

## Notes
- `railway.json` exists suggesting Railway was explored — it's a valid alternative to Vercel
- Oracle Wallet auth is the main deployment complexity; document the wallet setup
- Consider deploying to staging first with a separate Supabase project
