---
status: pending
priority: P1
issue_id: "016"
tags: [flip-my-era, security, secrets, edge-functions, vite, groq, stripe]
dependencies: []
---

# 016 — Move API Secrets from VITE_ Frontend to Supabase Edge Functions

## Overview

FlipMyEra currently exposes API keys in the browser bundle via `VITE_` prefixed environment variables. Any key prefixed with `VITE_` is embedded in the compiled JavaScript bundle and visible to anyone who visits the site and inspects the source. This is a **security vulnerability** for sensitive keys like:
- `VITE_GROQ_API_KEY` — used for AI story generation
- `VITE_RUNWARE_API_KEY` — used for image generation
- Any future payment or AI keys

Supabase Anon Key and Stripe Publishable Key are intentionally public and can remain as `VITE_` variables. All other API keys must move to edge functions.

**Why P1:** Anyone who visits flipmyera.com can extract the Groq API key from the bundle and use it for free AI generation at your expense. This is a live financial risk.

## Coding Prompt

You are working on FlipMyEra, a React 18 + TypeScript + Vite + Supabase SaaS app at `/data/workspace/projects/flip-my-era/`.

**Task:** Audit all `VITE_` env vars and move non-public secrets to Supabase Edge Functions.

### Step 1 — Audit all VITE_ usage

Run:
```bash
grep -r "VITE_" src/ --include="*.ts" --include="*.tsx" | grep -v "node_modules" | grep -v ".test." | sort -u
grep -r "import.meta.env" src/ --include="*.ts" --include="*.tsx" | grep -v ".test." | sort -u
```

Categorize each variable:
- **Safe (public):** `VITE_SUPABASE_URL`, `VITE_SUPABASE_ANON_KEY`, `VITE_STRIPE_PUBLISHABLE_KEY`, `VITE_POSTHOG_KEY`, `VITE_GTM_ID`
- **Unsafe (must move):** `VITE_GROQ_API_KEY`, `VITE_RUNWARE_API_KEY`, `VITE_SENTRY_DSN` (less critical), any other AI or payment processing keys

### Step 2 — Audit existing edge functions

Check whether Groq calls already go through edge functions:
- `supabase/functions/groq-api/index.ts` — does this function use `Deno.env.get('GROQ_API_KEY')`?
- `supabase/functions/runware-proxy/index.ts` — same check

Read both files. If the edge functions already exist and handle the API calls properly, the issue may be that **the frontend ALSO has a direct path** to the API using the VITE_ key. Find and remove the direct frontend paths.

### Step 3 — Remove VITE_GROQ_API_KEY from frontend

In `src/modules/shared/utils/groq.ts`:
- If it currently reads `import.meta.env.VITE_GROQ_API_KEY` and calls Groq directly, REMOVE this code.
- All Groq calls must go through `supabase.functions.invoke('groq-api', ...)` or `supabase.functions.invoke('groq-storyline', ...)`.

Update any component that calls Groq directly to use the edge function instead.

### Step 4 — Remove VITE_RUNWARE_API_KEY from frontend

In `src/modules/shared/utils/runware.ts` and `src/modules/shared/services/runwayApi.ts`:
- If it reads `import.meta.env.VITE_RUNWARE_API_KEY`, REMOVE it.
- All image generation must go through `supabase.functions.invoke('runware-proxy', ...)`.

### Step 5 — Update EnvironmentValidator

In `src/modules/shared/components/EnvironmentValidator.tsx`, remove any validation check for `VITE_GROQ_API_KEY` or `VITE_RUNWARE_API_KEY` — these should no longer be required in the frontend environment.

Update `.env.example` to reflect what is now truly required in the frontend.

### Step 6 — Update Supabase deploy workflow

In `.github/workflows/supabase-deploy.yml`, ensure secrets are passed as edge function environment variables:

```yaml
- name: Set Edge Function Secrets
  run: |
    supabase secrets set GROQ_API_KEY=${{ secrets.GROQ_API_KEY }}
    supabase secrets set RUNWARE_API_KEY=${{ secrets.RUNWARE_API_KEY }}
```

Remove `GROQ_API_KEY: ${{ secrets.VITE_GROQ_API_KEY }}` references — use `GROQ_API_KEY: ${{ secrets.GROQ_API_KEY }}` with a properly named secret.

### Step 7 — Test that AI generation still works

After removing VITE_ keys from frontend:
1. Run locally without VITE_GROQ_API_KEY set
2. Trigger a story generation
3. Verify it still works via the edge function
4. Verify no console errors about missing API keys

## Dependencies

Coordinate with TODO #015 (subscription tiers) — Stripe secret key should also be edge-function-only.

## Effort

M (1-2 days)

## Acceptance Criteria

- [ ] `grep -r "VITE_GROQ" src/` returns zero results
- [ ] `grep -r "VITE_RUNWARE" src/` returns zero results
- [ ] Story generation still works (via edge function)
- [ ] Image generation still works (via edge function)
- [ ] `EnvironmentValidator` updated to not require removed VITE_ vars
- [ ] `.env.example` updated
- [ ] `npm run typecheck` passes
- [ ] `npm run test:ci` passes
- [ ] No API keys visible in browser network inspector during story generation
