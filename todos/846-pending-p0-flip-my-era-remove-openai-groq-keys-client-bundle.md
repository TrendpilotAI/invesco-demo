# TODO-846: Remove VITE_OPENAI_API_KEY and VITE_GROQ_API_KEY from Client Bundle

**Priority:** P0 — Critical Security
**Repo:** flip-my-era
**Effort:** S (1 day)
**Created:** 2026-03-08 by Judge Agent v2

## Problem

`VITE_OPENAI_API_KEY` and `VITE_GROQ_API_KEY` are exposed in the client-side JS bundle. Any browser visitor can extract them via DevTools. These are live billing-enabled API keys.

Note: `groq-api` and `groq-storyline` edge functions already exist server-side — frontend should call those exclusively.

## Task

1. Search for all usages of `VITE_OPENAI_API_KEY` and `VITE_GROQ_API_KEY` in `src/`:
   ```bash
   grep -rn "VITE_OPENAI_API_KEY\|VITE_GROQ_API_KEY" src/
   ```
2. Remove both vars from `src/vite-env.d.ts` and `src/modules/shared/utils/env.ts`
3. Create `supabase/functions/openai-proxy/index.ts` edge function that proxies OpenAI calls using `Deno.env.get('OPENAI_API_KEY')` (server-only)
4. Update all frontend callers to use `supabase.functions.invoke('groq-api', ...)` or `supabase.functions.invoke('openai-proxy', ...)`
5. Remove both vars from `.env.example` (or document as server-only)
6. Run `pnpm build` — verify no `OPENAI_API_KEY` or `GROQ_API_KEY` strings in `dist/`

## Acceptance Criteria
- [ ] `grep -r "VITE_OPENAI_API_KEY\|VITE_GROQ_API_KEY" dist/` returns nothing
- [ ] Story generation still works end-to-end via edge functions
- [ ] No client-side code imports OpenAI or Groq SDK directly
