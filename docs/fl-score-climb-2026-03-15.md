# FL Score Climb — 2026-03-15

## Prioritized queue used this run
1. **signal-studio** — safest high-leverage target in the current workspace: close remaining auth/CSRF caller gaps and fix any obvious admin-console data wiring bugs.
2. **signal-builder-backend** — validate whether the in-flight router/rate-limit branch still needed intervention beyond the already-added delete logging and focused tests.
3. **forwardlane-backend** — keep prior analytical hardening work intact; defer until the correct project env is available for executable validation.
4. **signal-studio-templates** / **signal-studio-auth** / **signal-studio-data-provider** — reviewed for queueing, but not touched this run because the biggest low-risk score gain was still in `signal-studio`.

## Work completed this run

### signal-studio
- Migrated remaining high-value UI callers from raw `fetch('/api/...')` to shared `authFetch()` in:
  - `app/admin/page.tsx`
  - `app/oracle-ml/page.tsx`
- Fixed an admin dashboard data bug:
  - the signals panel was accidentally fetching `/api/admin/collections` twice
  - it now fetches `/api/signals` for signal data and `/api/admin/collections` for collections
- Updated repo docs to reflect the new state:
  - `AUDIT.md`
  - `PLAN.md`
- Ran focused validation:
  - `pnpm exec jest __tests__/lib/api-client.test.ts --runInBand` ✅
  - `pnpm exec eslint app/admin/page.tsx app/oracle-ml/page.tsx lib/api-client.ts __tests__/lib/api-client.test.ts` ✅

## Findings / repo state notes
- **signal-studio** still has additional lower-risk direct `/api/*` callers (for example in `lib/agent/tools-impl.ts` and some test harnesses), but the biggest remaining admin-facing gap is now closed.
- **signal-builder-backend** already contains the earlier `delete_signal` logging improvement in `apps/signals/routers/signal.py`; no extra code change was required this run without first reconciling the active branch’s broader in-flight edits.
- **forwardlane-backend** still has useful in-flight analytical hardening changes on the current branch, but local execution remains blocked by environment/setup mismatch in this shell.
- Live repo locations are still split:
  - `/data/workspace/repos/...` for `forwardlane-backend`, `signal-builder-backend`, `signal-studio`
  - `/data/workspace/projects/...` for `signal-studio-templates`, `signal-studio-auth`, `signal-studio-data-provider`

## Recommended next queue
1. **signal-studio**
   - sweep remaining lower-risk direct `fetch('/api/...')` callers to `authFetch()` / `csrfFetch()`
   - then tackle one of the next score-lifters: `signal_runs` persistence or ReactFlow package dedupe
2. **signal-builder-backend**
   - consolidate the active webhook/rate-limit branch state
   - then hit the next concrete security/quality issue (likely backoff semantics or dependency audit)
3. **forwardlane-backend**
   - run the analytical test suite in the correct env and confirm the existing connection/query hardening changes pass
4. **signal-studio-templates**
   - attack the PostgreSQL DataProvider gap once the above repos are in a cleaner validated state
