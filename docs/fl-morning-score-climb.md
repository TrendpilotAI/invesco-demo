# FL Morning Score Climb — recurring follow-on

## Objective
Each morning, pick up from the latest overnight learnings, observations, test results, commits, documentation, and recommendations, then continue improving the FL repos until their **project scores exceed 8.0** where realistically achievable.

## Score interpretation
The FL repo scoring system is on a 0–10 scale. "80%" here means **8.0+ composite score**.

## Target repos
1. /data/workspace/repos/forwardlane-backend
2. /data/workspace/repos/signal-builder-backend
3. /data/workspace/repos/signal-studio
4. /data/workspace/repos/signal-studio-frontend
5. /data/workspace/repos/signal-studio-templates
6. /data/workspace/repos/signal-studio-auth
7. /data/workspace/repos/signal-studio-data-provider

## Inputs to read first
- /data/workspace/docs/fl-overnight-coverage-batch.md
- latest docs generated overnight under /data/workspace/docs/
- repo-local PLAN.md / AUDIT.md / BRAINSTORM.md updates
- /data/workspace/.orchestrator/project-scores.json
- /data/workspace/TODO-REPO-INTELLIGENCE.md
- any newly created progress notes from the overnight run

## Core behavior
1. Read the latest documentation and overnight outputs.
2. Build a prioritized execution queue from:
   - findings
   - observations
   - failed tests
   - coverage gaps
   - blocker notes
   - recommendations
3. Prefer ACP-style coding workflows where possible for heavier repo work.
4. Execute the highest-leverage fixes first.
5. Run tests / quality checks after meaningful changes.
6. Deploy only when safe and already supported by the repo workflow:
   - prefer staging / non-destructive deployment first
   - do not invent deployment paths
   - do not bypass existing safety checks
7. Update docs as progress is made.
8. Re-check project score implications using the current scoring criteria.
9. Continue until:
   - major FL repos are above 8.0, or
   - time budget is exhausted, or
   - remaining work becomes low-confidence / high-risk.

## Prioritization rules
- First: revenue-critical and Invesco-adjacent repos
- Second: repos with the highest score upside from concrete fixes
- Third: infrastructure/support repos that unblock the above

## Initial priority order
1. forwardlane-backend
2. signal-builder-backend
3. signal-studio / signal-studio-frontend
4. signal-studio-templates
5. signal-studio-data-provider
6. signal-studio-auth

## What to improve
- real test coverage
- high-risk defects
- auth/security gaps
- API contract stability
- deployability
- documentation quality
- obvious score blockers called out in audits and plans

## Hard constraints
- No fake coverage or no-op work to game scores.
- No destructive git history edits unless already explicitly approved elsewhere.
- No unsafe production deploys.
- Prefer branch-safe workflow.
- Document findings, observations, recommendations, and outcomes as you go.

## Reporting
At the end of each run, produce:
- repo-by-repo work completed
- tests / coverage changes
- deploys performed (if any)
- updated recommendations
- estimated score movement or blockers preventing >8.0
