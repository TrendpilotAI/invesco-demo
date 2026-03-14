# FL Score Climb — 2026-03-14

## Morning queue
1. **forwardlane-backend** — close remaining analytical API hardening gaps blocking >8.0 confidence:
   - stop leaking raw DB exception details
   - bound large advisor-detail queries
   - harden DB connect timeout / ssl options
2. **signal-builder-backend** — validate in-flight webhook/rate-limit/audit test changes and keep pushing security posture above the current 8.0 floor.
3. **signal-studio** — already above 8.0; treat as stabilization only unless a fast, low-risk issue emerges.
4. **signal-studio-templates** — next best score-up candidate after backend cleanup.
5. **signal-studio-data-provider** / **signal-studio-auth** — likely require heavier work than this run’s budget.

## Work completed this run

### forwardlane-backend
- Hardened `analytical/views.py` error handling so 503 responses no longer expose raw database exception details.
- Added bounded limits to the heaviest `AdvisorDetailView` subqueries:
  - holdings → `LIMIT 100`
  - flows-by-fund → `LIMIT 250`
  - signals → `LIMIT 100`
- Hardened DB connection settings in `forwardlane/settings/databases.py`:
  - `connect_timeout`
  - `sslmode`
  - separate analytical overrides supported via env vars
- Extended `analytical/tests/test_views.py` to assert:
  - generic 503 payload for DB failures
  - advisor detail SQL now includes safety limits

### signal-builder-backend
- Reviewed current repo state and latest in-flight changes.
- Verified focused quality/security suite passes against the active working tree:
  - `tests/test_webhooks.py`
  - `tests/test_health.py`
  - `tests/test_audit_log.py`
  - `tests/test_signal_preview.py`
- Result: **26 tests passed** in ~2.75s.

## Notes / blockers
- Several target repo paths in `docs/fl-morning-score-climb.md` are stale under `/data/workspace/repos`; live copies for `signal-studio-frontend`, `signal-studio-templates`, `signal-studio-auth`, and `signal-studio-data-provider` are under `/data/workspace/projects/`.
- `forwardlane-backend` currently lacks an immediately usable local pytest environment in this workspace shell, so validation this run was limited to code + test updates rather than executing the suite.
- `signal-builder-backend` and `signal-studio` both have uncommitted in-flight changes already present; avoid broad refactors there without first consolidating the active branch state.

## Recommended next queue
1. `forwardlane-backend`: run the analytical/easy_button suite in the proper project env, then tackle remaining analytical auth/CSRF cleanup or audit-log coverage gaps.
2. `signal-builder-backend`: finish and consolidate the current webhook/auth/rate-limit branch state, then address next concrete security blocker.
3. `signal-studio-templates`: attack the missing PostgreSQL DataProvider + POST body validation gap.
4. `signal-studio-auth`: resolve security header conflicts and confirm deploy-safe auth flows.
