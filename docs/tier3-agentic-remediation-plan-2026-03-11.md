---
date: 2026-03-11
topic: tier3-agentic-remediation
status: ready-for-execution
owner: Honey
---

# Tier 3 Agentic Remediation Plan

## Executive Summary
This plan remediates all material issues raised in the Tier 3 scoring report across these seven repos:

1. `Trendpilot`
2. `flip-my-era`
3. `signal-studio-auth`
4. `signalhaus-website`
5. `Second-Opinion`
6. `signal-studio-data-provider`
7. `core-entityextraction`

However, the current Tier 3 report is **not fully trustworthy as a snapshot of present reality**. Overnight agent work already fixed some issues on branches, while other findings are likely still valid on main. Therefore, the first phase is **reconciliation**, not blind remediation.

---

# North Star
Produce a Tier 3 board that is:
- **current**
- **evidence-backed**
- **branch-aware**
- **actionable**

And leave each repo with:
- validated current-state docs
- reduced P0 risk
- updated tests where needed
- updated scorecards
- explicit human-only blockers separated from code blockers

---

# Operating Principles

## 1. Main vs Branch Reality
Every finding must be tagged as exactly one of:
- `valid-on-main`
- `fixed-on-branch`
- `stale`
- `blocked-noncode`

## 2. Security Before Cosmetics
If a repo has both a styling/test debt issue and an auth/data exposure issue, the auth/data issue wins.

## 3. Merge Discipline
A fix that exists only on a feature branch does **not** count as resolved in final scoring.

## 4. Human/Legal Separation
If something is not fixable in code — like BAA, policy, vendor agreement — mark it as `blocked-noncode` and stop pretending it’s an engineering task.

## 5. Evidence Required
Every claim in the updated scorecards must cite one of:
- file path + line or grep result
- passing test evidence
- runtime verification
- explicit human confirmation for non-code items

---

# Scope by Repo

## Trendpilot
### Reported Issues
- zero authentication on API routes
- hardcoded SSO user returns
- synchronous file I/O bottlenecks
- in-memory storage / restart risk
- broken rate limit reset

### Desired End State
- all protected routes require auth
- SSO callback is real or disabled
- critical persistence is durable or explicitly admin-only
- rate limiting works and resets correctly

---

## flip-my-era
### Reported Issues
- client-side AI keys exposed
- Stripe billing stubbed
- duplicate `creator/` vs `creators/`

### Desired End State
- no paid-provider secrets in browser bundle
- real billing flow works end-to-end
- duplicate creator modules consolidated

---

## signal-studio-auth
### Reported Issues
- duplicate middleware
- X-Frame-Options weakened DENY → SAMEORIGIN
- missing comprehensive README

### Desired End State
- single canonical header middleware
- no security-policy conflicts
- clear integration/deployment docs

---

## signalhaus-website
### Reported Issues
- in-memory rate limiter vulnerable on serverless cold starts
- contact form lacks durable bot protection
- missing logo asset
- weak test coverage

### Desired End State
- durable rate limiting
- bot protection on contact form
- assets/metadata valid
- materially improved route/component coverage

---

## Second-Opinion
### Reported Issues
- no Google/Firebase BAA
- PHI leak risk via logs
- low test coverage
- no rate limiting on expensive AI endpoints

### Desired End State
- code safe enough for PHI *once legal blocker is removed*
- legal blocker clearly documented as non-code
- expensive endpoints rate-limited
- risky logs removed

---

## signal-studio-data-provider
### Reported Issues
- broken test runner
- mock-only tests
- missing SecretStr
- dependency conflicts

### Desired End State
- reproducible green test runner
- integration tests exist
- credentials redacted by type
- dependency environment stable

---

## core-entityextraction
### Reported Issues
- monolithic `main.py`
- persistence cleanup concerns
- dead code / DRY violations

### Desired End State
- app split into clean modules
- connection cleanup guaranteed on failure paths
- dead code removed without regressions

---

# Phase 0 — Reconciliation (Mandatory)

## Purpose
Prevent agents from fixing stale findings or duplicating overnight branch work.

## Deliverables
- `/data/workspace/reports/tier3-reconciliation-security.md`
- `/data/workspace/reports/tier3-reconciliation-infra.md`
- `/data/workspace/reports/tier3-reconciliation-matrix.csv`

## Reconciliation Matrix Format
| Repo | Finding | Report Claim | Main State | Branch State | Status | Evidence | Action Needed |
|------|---------|--------------|------------|--------------|--------|----------|---------------|

## Agent R0-A — Security Reconciliation
**Repos:** Trendpilot, flip-my-era, signal-studio-auth, signalhaus-website, Second-Opinion

### Checklist
- inspect main/default branch
- inspect known overnight fix branches
- verify reported critical claims
- grep for security middleware/auth usage
- run lightweight tests where possible
- produce status labels

### Definition of Done
- every reported critical security claim is classified
- no ambiguous “maybe fixed” items remain

## Agent R0-B — Infra/Test Reconciliation
**Repos:** signal-studio-data-provider, core-entityextraction

### Checklist
- run test suite / coverage command
- inspect architecture hotspots
- verify whether overnight fixes landed on branch only
- check current pain is code, env, or both

### Definition of Done
- test runner state known
- coverage state known
- architecture debt separated from active breakage

---

# Phase 1 — P0 Security & Legal Blockers

## Trendpilot Remediation

### Workstream T1 — Route Authentication Lockdown
**Owner type:** security/full-stack agent

#### Tasks
- inventory every API/admin route
- classify routes: public vs authenticated vs admin-only
- apply middleware guardrails consistently
- switch to deny-by-default routing pattern where feasible
- add tests:
  - no token → 401
  - wrong tenant → 403
  - viewer vs admin role boundaries
  - malformed token → 401

#### Acceptance Criteria
- unauthenticated requests cannot reach protected business data
- test suite proves protected-route coverage

### Workstream T2 — SSO Hardening
#### Tasks
- inspect SAML/OAuth callback implementation
- remove hardcoded users or fake success paths
- implement real assertion validation or disable route behind feature flag
- add tests for invalid callback payloads

#### Acceptance Criteria
- no auth callback returns a hardcoded user
- auth failure path behaves safely

### Workstream T3 — Persistence/Risk Cleanup
#### Tasks
- identify critical JSON/file-backed stores
- move to durable backend or restrict to authenticated admin-only tooling
- fix rate-limit reset logic

#### Acceptance Criteria
- no production-critical data depends on restart-unsafe memory/file hacks

---

## flip-my-era Remediation

### Workstream F1 — Browser Secret Eradication
#### Tasks
- scan for `VITE_*` and other client-exposed paid-provider keys
- verify bundle/runtime path, not just docs
- move any live AI calls to edge/server functions
- add build guard that fails on forbidden client env vars

#### Acceptance Criteria
- browser bundle contains no paid-provider secrets
- CI/build fails if forbidden keys reappear

### Workstream F2 — Billing Completion
#### Tasks
- trace checkout flow from UI → edge/server → Stripe
- replace all stubbed URLs and fake session flows
- handle success, cancel, webhook sync, subscription state
- write tests for checkout creation and state transitions

#### Acceptance Criteria
- a real checkout session can be created
- subscription state persists correctly

### Workstream F3 — Module Consolidation
#### Tasks
- compare `creator/` and `creators/`
- choose canonical module
- migrate imports
- delete deprecated duplicate after tests pass

#### Acceptance Criteria
- one canonical creator module remains
- no duplicate behavior paths remain

---

## signal-studio-auth Remediation

### Workstream A1 — Middleware / Header Conflict Removal
#### Tasks
- inventory all middleware touching headers
- remove duplicate/competing header writers
- centralize security header policy
- add header snapshot tests for key endpoints

#### Acceptance Criteria
- one source of truth for security headers
- X-Frame-Options and related headers stable across all routes

### Workstream A2 — Auth Service Documentation
#### Tasks
- document env vars
- document login/refresh/revoke/session flows
- document Redis, rate limiting, token family logic
- document deployment and health checks

#### Acceptance Criteria
- README allows a new engineer to run and integrate the service without tribal knowledge

---

## signalhaus-website Remediation

### Workstream H1 — Contact Route Hardening
#### Tasks
- replace in-memory limiter with durable limiter
- add Turnstile/CAPTCHA/honeypot
- verify behavior under serverless cold starts
- add tests for abuse cases

#### Acceptance Criteria
- contact route remains protected across stateless invocations

### Workstream H2 — Site Reliability / Coverage
#### Tasks
- fix missing assets
- test contact API, landing pages, metadata, forms
- improve confidence in production deploy

#### Acceptance Criteria
- no broken structured-data assets
- route/component test coverage materially improved

---

## Second-Opinion Remediation

### Workstream S1 — Code Hardening
#### Tasks
- remove PHI-risky logs
- add throttling on AI analysis endpoints
- test rules and analysis entrypoints
- document legal blocker clearly in repo

#### Acceptance Criteria
- code no longer casually leaks PHI in logs
- expensive endpoints protected from abuse

### Human Workstream S2 — Legal BAA
#### Nathan Action
- sign/confirm BAA with Google Cloud/Firebase before production PHI usage

#### Acceptance Criteria
- repo status becomes either:
  - `code-ready-legal-blocked`
  - or `production-eligible` once BAA confirmed

---

# Phase 2 — Infra Reliability

## signal-studio-data-provider

### Workstream D1 — Test Runner Recovery
#### Tasks
- run clean env install
- fix failing/pinned dependencies
- make pytest command reproducible in CI and local
- document known platform-specific quirks

### Workstream D2 — SecretStr and Config Hygiene
#### Tasks
- convert credential-bearing fields to `SecretStr`
- ensure repr/log output redacts secrets
- add tests for safe serialization/repr

### Workstream D3 — Integration Coverage
#### Tasks
- add testcontainers or equivalent integration tests
- cover one live-ish happy path per provider backend
- keep mocks for unit tests, add integration lane separately

#### Acceptance Criteria
- repo no longer depends only on mocks for critical confidence

---

## core-entityextraction

### Workstream C1 — Decompose main.py
#### Tasks
- split routes, services, extraction logic, app bootstrap
- reduce main.py to wiring
- preserve public API

### Workstream C2 — Persistence Safety
#### Tasks
- audit all DB/session/connection paths
- replace leak-prone branches with guaranteed cleanup
- add exception-path tests

### Workstream C3 — Dead Code & DRY Cleanup
#### Tasks
- remove unused models/functions
- consolidate duplicate logic
- verify no API regressions

#### Acceptance Criteria
- architecture debt reduced without destabilizing service

---

# Phase 3 — Re-scoring

## Purpose
Generate a score report that reflects current truth instead of stale snapshots.

## Agent R3 — Fresh Tier 3 Judge
### Inputs
- reconciliation reports
- merged fixes
- still-open blockers

### Outputs
- refreshed `TIER3-SCORE-SUMMARY.md` for each repo
- updated blackboard scores
- stale findings explicitly retired

### Rules
- no score note may cite a finding marked `stale`
- branch-only fixes must be labeled as such until merged
- legal blockers must not be misrepresented as code defects

---

# Execution Matrix

| Wave | Agents | Focus | Duration | Exit Condition |
|------|--------|-------|----------|----------------|
| 0 | 2 | Reconciliation | 20-40 min | all findings classified |
| 1 | 5 | P0 security/legal | 45-90 min | critical path fixes landed on branches |
| 2 | 5 | revenue/completion | 45-90 min | billing/auth/docs/site hardening done |
| 3 | 5 | infra reliability | 45-90 min | tests + config + architecture fixes landed |
| 4 | 1-2 | re-score | 15-30 min | new board published |

---

# Suggested Agent Prompts

## Prompt: Reconciliation Agent
"Review the Tier 3 report claims against current main/default branch and any known fix branches. For each finding, classify it as valid-on-main, fixed-on-branch, stale, or blocked-noncode. Produce evidence-backed markdown and CSV outputs. Do not fix code unless needed to verify a claim."

## Prompt: Security Fix Agent
"Fix only validated P0 security issues. Add tests proving the vulnerability is closed. Commit on focused branches. Avoid scope creep into cleanup unless it directly supports the P0 fix."

## Prompt: Infra/Test Agent
"Repair test reliability first, then improve coverage and integration confidence. Distinguish env/setup breakage from actual code failures. Add reproducible commands and CI-compatible fixes."

## Prompt: Re-score Agent
"Use only reconciled, evidence-backed findings. Do not repeat stale claims. If a fix exists only on branch, label it branch-fixed and do not count it as resolved on main."

---

# Risk Register

| Risk | Why it matters | Mitigation |
|------|----------------|------------|
| stale findings get re-fixed | wasted agent cycles | mandatory reconciliation phase |
| branch fixes not merged | judge keeps rediscovering issues | merge gate before final scoring |
| legal blockers treated as code | endless fake engineering work | label blocked-noncode |
| broad prompts cause shallow fixes | lots of partial work | use repo-specific focused prompts |
| security fixes break production | auth/header/rate-limit regressions | add targeted tests before/after |

---

# Review Gates

## Gate A — After Reconciliation
Proceed only if:
- all 7 repos classified
- all critical claims tagged
- no unresolved ambiguity around main vs branch

## Gate B — After P0 Remediation
Proceed only if:
- Trendpilot auth state proven
- flip-my-era secret/billing state proven
- signal-studio-auth header conflict proven fixed or still open
- signalhaus contact surface hardened or clearly blocked
- Second-Opinion legal blocker documented

## Gate C — Before Re-score
Proceed only if:
- fixes are merged or explicitly labeled branch-only
- no stale findings remain in active score notes

---

# Final Deliverables
- `reports/tier3-reconciliation-security.md`
- `reports/tier3-reconciliation-infra.md`
- `reports/tier3-reconciliation-matrix.csv`
- updated score summaries for all 7 repos
- updated `.orchestrator/blackboard.json`
- repo-specific PRs/branches for validated fixes
- concise executive summary for Nathan

---

# Final Recommendation
This should be executed as a **branch-aware remediation program**, not a one-shot bugfix swarm.

The right sequence is:

**reconcile → validate → remediate → merge → re-score**

Anything else risks turning the Tier 3 board into expensive fiction.
