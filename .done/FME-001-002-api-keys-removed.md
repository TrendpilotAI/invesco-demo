# FME-001 + FME-002 — API Keys Removed from Client Bundle ✅

**Completed:** 2026-03-08  
**Commit:** `2029e9a` pushed to `main`

## What Was Found

Grep of all `*.ts`, `*.tsx`, `*.js`, `*.jsx` files revealed:
- **No active client-side usage** of `VITE_OPENAI_API_KEY` or `VITE_GROQ_API_KEY`
- `src/modules/shared/utils/env.ts` — `getGroqApiKey()` and `getOpenAiApiKey()` already return `undefined` (deprecated with security warnings)
- Only occurrences were in comments/test files warning NOT to use these keys
- **The one real issue:** `.env.example` still listed both as `VITE_` prefixed vars, which would mislead developers into setting them incorrectly

## What Was Changed

### `.env.example`
- **Removed** `VITE_GROQ_API_KEY=your-groq-api-key`
- **Removed** `VITE_OPENAI_API_KEY=your-openai-api-key`
- **Added** commented-out server-side equivalents with clear explanation that they belong in Supabase Edge Function secrets (no `VITE_` prefix)

## Verified

- `pnpm build` ✅ — builds successfully
- `grep -r "VITE_OPENAI_API_KEY\|VITE_GROQ_API_KEY" dist/` → **0 results** ✅
- No tracked `.env` files with secrets (git status clean)
- All Groq/OpenAI calls already route through Edge Functions: `groq-api`, `groq-storyline`, `stream-chapters`

## Architecture (Already Correct)

```
Client → Supabase Edge Functions (groq-api, groq-storyline, stream-chapters)
                    ↓
         GROQ_API_KEY / OPENAI_API_KEY (server-side secrets only)
```

## Note on Dependabot Alerts

GitHub reported 3 vulnerabilities (1 high, 2 moderate) on push — these are pre-existing dependency issues unrelated to this task, tracked separately.
