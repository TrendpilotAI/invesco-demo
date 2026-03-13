# FL Score Climb Progress — 2026-03-10

## Prioritized queue used for this run
1. `signal-studio` — fast score lift from audit-called unified DB health endpoint + test coverage
2. `signal-builder-backend` — verify low-risk reliability fixes already landed; only touch if current code still missing them
3. `forwardlane-backend` — leave for heavier branch-safe coverage/auth work after confirming overnight branch state

## Findings during this run
- `signal-studio-frontend`, `signal-studio-templates`, `signal-studio-auth`, and `signal-studio-data-provider` are **not present** at the expected target paths under `/data/workspace/repos/`; morning run could not directly execute repo-local work there.
- `signal-studio` already has route-level health endpoints for Oracle / semantic / vectorization, but did **not** yet have the unified `/api/health/db` endpoint called out in the audit/plan.
- `signal-builder-backend` already has the previously-audited delete-signal exception logging improvement in place, so that specific item no longer needed fresh code changes.
- `forwardlane-backend` is currently on `upgrade/python311-django42` with an existing unstaged deletion (`easy_button/views_old.py.bak`), so higher-risk edits there should stay branch-safe and deliberate.

## Work completed
### signal-studio
- Added `app/api/health/db/route.ts`
  - checks Postgres via `lib/db.ts`
  - checks Oracle via `lib/oracle-service`
  - reports rate limiter backend status
  - returns `503` when a core dependency is unhealthy or unconfigured
- Added unit coverage at `__tests__/api/health/db.route.test.ts`
- Extended Playwright health coverage in `tests/e2e/health-endpoints.spec.ts`

## Recommendations queued next
### forwardlane-backend
- Highest leverage next: targeted `easy_button` / `analytical` tests around auth + SQL safety, not broad sweeps.

### signal-builder-backend
- Next concrete lift: add tests around `BaseServiceAPI.request()` retry/error semantics and review `retry_max_count` naming/behavior.

### signal-studio
- Next wins after this run: CSRF coverage audit/fixes, `signal_runs` persistence, and reactflow dedup.

---

## Follow-on run — 2026-03-13 12:27 UTC

## Prioritized queue used for this run
1. `signal-studio` — finish and validate the high-risk CSRF/header-centralization work already in progress
2. `signal-studio-auth` — validate and harden explicit CORS allowlisting + password complexity work already in progress
3. `signal-builder-backend` — attempt to validate webhook/rate-limit/auth-bypass test work already in progress
4. `forwardlane-backend` — inspect branch state and leave for a dedicated Python/Django upgrade-safe pass unless there was an obvious low-risk win

## Work completed
### signal-studio
- Validated the in-progress CSRF/header-centralization changes already on branch:
  - `lib/api-client.ts` now injects CSRF headers for same-origin state-changing `/api/*` calls
  - `lib/auth-context.tsx`, `components/ai-chat-template.tsx`, and `components/visual-editor/visual-builder-chat.tsx` now use CSRF-aware fetch helpers on high-risk POST flows
- Ran targeted Jest validation:
  - `pnpm test -- --runInBand __tests__/lib/api-client.test.ts`
  - Result: **3/3 tests passing**
- Net effect: closes a concrete audit gap with low regression risk and improves confidence on auth/session-sensitive routes

### signal-studio-auth
- Validated the in-progress branch changes for:
  - explicit `CORS_ALLOWED_ORIGINS` allowlisting in `main.py`
  - signup password complexity enforcement in `routes/auth_routes.py`
- Added missing test/dependency support:
  - `tests/test_cors_and_signup_validation.py`
  - `requirements.txt` now includes `fakeredis==2.34.1` because the existing redis integration tests depend on it
- Ran full pytest suite after the additions:
  - Result: **109 passed, 1 warning**
- Net effect: this repo moved from “security hardening in progress” to “security hardening implemented and validated” for the CORS/password-complexity slice

### signal-builder-backend
- Reviewed the in-progress branch focused on webhook auth bypass correctness, rate-limiter resilience, and targeted test repairs
- Attempted to run targeted pytest validation for:
  - `tests/test_health.py`
  - `tests/test_webhooks.py`
  - `tests/test_signal_preview.py`
  - `tests/test_audit_log.py`
- Blocker found: the repo currently expects a project-specific dependency/runtime stack (notably Pydantic v1-compatible auth dependencies such as `fastapi-jwt-auth`), while the shared validation environment here is Pydantic v2-oriented. This causes import-time failures before the tests themselves execute.
- Net effect: branch changes look directionally right, but this repo still needs validation inside its native pinned environment before I’d count the score lift as real

### forwardlane-backend
- Re-read plan/audit context and checked branch state
- Current repo is already scored above 8.0 in the orchestrator snapshot and is mid-flight on `upgrade/python311-django42`
- Left it untouched this run because the highest-leverage remaining work there is not “tiny safe tweak” territory — it is targeted `easy_button` / `analytical` test + auth + SQL-safety work that deserves a dedicated branch-safe pass in the repo’s own environment

## Updated recommendations / next queue
1. `signal-builder-backend`
   - run the current branch’s targeted tests inside the repo’s native pinned environment (Pydantic v1 / Pipfile-driven stack)
   - if green, commit the webhook auth-bypass + limiter-resilience test bundle
2. `signal-studio`
   - land `signal_runs` persistence next for compliance/audit-score lift
   - then remove legacy `reactflow` after import migration and bundle verification
3. `signal-studio-auth`
   - add one small deployment note documenting `CORS_ALLOWED_ORIGINS` examples for staging/prod
   - optional next hardening: login/signup/invite E2E smoke tests
4. `forwardlane-backend`
   - next dedicated pass should focus on real `easy_button` / `analytical` safety tests, not broad coverage-chasing
