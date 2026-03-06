# DONE-589: Add compliance audit_log table

**Status:** ✅ Complete
**Completed:** 2026-03-06

## What Was Done

1. **`lib/db.ts`** — Added `audit_log` table creation to `ensureSchema()`:
   - UUID primary key, actor_id, action, resource_type, resource_id, metadata (JSONB), ip_addr, created_at
   - Indexes on actor_id and created_at DESC

2. **`lib/audit.ts`** (new) — `auditLog()` helper:
   - Accepts `{ actorId, action, resourceType?, resourceId?, metadata?, ipAddr? }`
   - Fire-and-forget: failures log but never crash app flow
   - `getIpFromRequest()` helper extracts IP from `x-forwarded-for` / `x-real-ip`

3. **`app/api/signals/run/route.ts`** — Wired `auditLog({ action: 'signal.run', ... })` on success

4. **`app/api/oracle/query/route.ts`** — Wired `auditLog({ action: 'oracle.query', ... })` on success

5. **`app/api/signals/[id]/route.ts`** — Wired `auditLog({ action: 'signal.delete', ... })` on both local DB and proxy DELETE paths

6. **`next.config.mjs`** — Added `pino`, `pino-pretty` to `serverExternalPackages` to prevent Turbopack from bundling them (pre-existing issue from upstream `lib/logger.ts` addition)

## Notes

- TypeScript: `pnpm exec tsc --noEmit` passes with 0 errors
- Build: The Turbopack build still fails due to `pino-pretty` bundling internal test files (thread-stream). This is a pre-existing issue from the upstream commit that added `lib/logger.ts` — not caused by audit changes. The `serverExternalPackages` fix was added; may need further investigation on CI.
- Commits pushed to `main` on Bitbucket

## Commits
- `feat: add audit_log compliance table + lib/audit.ts wired to signal/oracle routes`
- `fix: add pino/pino-pretty to serverExternalPackages to prevent Turbopack bundling`
