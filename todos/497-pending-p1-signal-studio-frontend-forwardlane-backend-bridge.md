# TODO-497: ForwardLane Django Backend Bridge / BFF

**Repo:** signal-studio-frontend  
**Priority:** P1  
**Effort:** L (2-3 days)  
**Status:** pending

## Description
Signal Studio needs to interoperate with the ForwardLane Django/Postgres backend (CORE_API env var exists). Per ecosystem analysis, ForwardLane backend holds all existing client/signal data in Postgres. Signal Studio needs to proxy this data through Next.js API routes and sync signals to Oracle for vector indexing.

## Coding Prompt
1. **Create `app/api/bff/signals/route.ts`** — proxy to `${CORE_API}/api/v1/signals/` with JWT forwarding
2. **Create `app/api/bff/clients/route.ts`** — proxy to `${CORE_API}/api/v1/clients/` 
3. **Create `lib/forwardlane-client.ts`** — typed API client for ForwardLane backend:
   - `getSignals()`, `getClients()`, `getSignalById(id)` 
   - Auto-attach JWT from request headers
4. **Create sync job `scripts/sync-to-oracle.ts`**:
   - Fetch signals from ForwardLane backend
   - Vectorize and store in Oracle (using OracleVectorService from TODO-494)
   - Run on demand or as cron
5. **Update middleware.ts** to ensure ForwardLane JWT is extracted and forwarded to BFF routes

## Dependencies
- TODO-494 (Oracle vector service) for sync step
- CORE_API env var configured

## Acceptance Criteria
- [ ] `/api/bff/signals` returns ForwardLane signal data
- [ ] JWT is properly forwarded (no manual token passing needed)
- [ ] `pnpm tsx scripts/sync-to-oracle.ts` syncs signals to Oracle vectors
