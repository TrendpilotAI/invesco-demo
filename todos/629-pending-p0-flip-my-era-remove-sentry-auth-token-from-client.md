# TODO: P0 — Remove VITE_SENTRY_AUTH_TOKEN from Client Bundle

**Repo:** flip-my-era  
**Priority:** P0 (Security Critical)  
**Effort:** 30 min  
**Depends on:** nothing

## Description

`VITE_SENTRY_AUTH_TOKEN` is used in `src/core/integrations/opentelemetry.ts` to set an `Authorization: Bearer` header in the OTLPTraceExporter. Because of the `VITE_` prefix, this auth token is compiled into the client-side JavaScript bundle and exposed to every browser visitor via DevTools.

**This is NOT the Sentry DSN** — it's a privileged auth token that grants write access to your Sentry project.

## Coding Prompt

```
In /data/workspace/projects/flip-my-era/:

1. Open src/core/integrations/opentelemetry.ts
2. Remove all references to import.meta.env.VITE_SENTRY_AUTH_TOKEN
3. Remove the Authorization header from the OTLPTraceExporter configuration
4. If the exporter works without auth (e.g., endpoint doesn't require it), keep it auth-less
5. If auth is required for the OTLP endpoint, remove the exporter entirely and rely on Sentry SDK's DSN-based ingestion (sentry.ts already handles this correctly)
6. Search entire codebase: grep -r "VITE_SENTRY_AUTH_TOKEN" src/
7. Remove any other occurrences found
8. Update env.example: remove VITE_SENTRY_AUTH_TOKEN line, add comment:
   # SENTRY_AUTH_TOKEN — server-side only, never use VITE_ prefix
   # Set in Supabase Edge Function secrets or Netlify build env (not VITE_)
9. Run: pnpm build && pnpm typecheck to verify no errors
```

## Acceptance Criteria
- [ ] No `VITE_SENTRY_AUTH_TOKEN` in any file under `src/`
- [ ] `pnpm build` succeeds
- [ ] Sentry error capture still works via DSN (test by triggering an error)
- [ ] env.example updated with explanation

## Security Action (Do First!)
Rotate the Sentry auth token immediately in:
Sentry → Settings → Auth Tokens → Revoke the exposed token → Create a new one for server-side use only
