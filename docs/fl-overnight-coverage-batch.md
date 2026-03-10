# FL Overnight Coverage Batch — 2026-03-10

## Objective
Run an overnight batch mode across the FL repos and iteratively improve real test coverage toward **80%**.

## Target repos
1. /data/workspace/repos/forwardlane-backend
2. /data/workspace/repos/signal-builder-backend
3. /data/workspace/repos/signal-studio
4. /data/workspace/repos/signal-studio-frontend
5. /data/workspace/repos/signal-studio-templates
6. /data/workspace/repos/signal-studio-auth
7. /data/workspace/repos/signal-studio-data-provider

## Success condition
Stop when **80% coverage is reached** on the active repo being worked, then move to the next highest-leverage repo.
If a repo cannot be measured cleanly, document the blocker and move on.

## Hard constraints
- No fake or trivial tests written only to game coverage.
- No disabling tests, linters, auth, or security controls just to raise numbers.
- No destructive branch/history operations.
- Prefer incremental commits with clean diffs.
- Preserve prod behavior; avoid speculative rewrites.
- Use branch-safe workflow: create or reuse repo-specific feature branches; avoid direct pushes to main/master unless explicitly required by existing repo workflow.

## Work loop
For each repo, repeat:
1. Detect test runner and current coverage using native tooling (`tox`, `pytest --cov`, `npm test -- --coverage`, etc.).
2. Identify the highest-risk, highest-leverage untested module tied to business-critical paths.
3. Add or improve tests first.
4. If tests expose design friction, make the minimal implementation refactor needed to make the code testable.
5. Re-run targeted tests and coverage.
6. Commit meaningful progress.
7. Continue until:
   - repo reaches >=80% measured coverage, or
   - the next coverage gains look low-confidence / unsafe, or
   - runtime budget is exhausted.

## Priority order
1. forwardlane-backend
2. signal-builder-backend
3. signal-studio / signal-studio-frontend
4. signal-studio-templates
5. signal-studio-data-provider
6. signal-studio-auth

## Repo-specific focus
### forwardlane-backend
- Easy Button critical endpoints
- startup/env validation
- high-risk API paths tied to Invesco flows
- avoid broad low-value test sweeps

### signal-builder-backend
- tenant isolation
- signal validate/publish/result flows
- API contract stability

### signal-studio / signal-studio-frontend
- route auth
- API handlers
- core UI logic that backs FL/Salesforce integration paths

### signal-studio-templates
- package-level integration tests
- template engine and API behavior

### signal-studio-data-provider
- safe query construction
- provider abstraction tests
- SQL injection regression tests

### signal-studio-auth
- deployment-critical auth flows
- token / session / revocation / security-path coverage

## Documentation while running
As progress is made, continuously update lightweight docs with:
- findings
- observations
- recommendations
- coverage measurements
- blockers / decisions

Prefer appending to existing repo docs when they already exist (`PLAN.md`, `AUDIT.md`, `BRAINSTORM.md`, repo-local notes), otherwise create a concise progress note in the repo root or docs folder.
Keep entries practical and dated — no essay spam.

## Coverage scoreboard
Maintain a simple scoreboard during the run with, at minimum:
- repo name
- baseline coverage
- latest coverage
- delta
- modules targeted
- commits created
- blockers / next recommendation

Prefer storing this in a single dated markdown note under `/data/workspace/docs/` so the morning review is fast.

## Reporting
At the end, provide:
- starting and ending coverage per repo worked
- commits created
- blockers for repos that could not reach 80%
- recommended next queue for the following day
- links/paths to updated documentation produced during the run
