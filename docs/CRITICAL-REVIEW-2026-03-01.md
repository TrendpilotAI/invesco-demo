# Critical Review: Judge Swarms, Agent Architecture & CI/CD Pipeline
**Date:** 2026-03-01 | **Reviewer:** Honey (Opus 4.6) | **Scope:** Last 7 days of agent work

---

## Executive Summary

The compound intelligence system has accomplished impressive breadth — 350+ TODO files, 15+ BRAINSTORM/AUDIT/PLAN docs, 9 cron jobs, 17-repo judge swarms, self-healing monitors, and a multi-tier orchestrator. **But it's a mile wide and an inch deep.** The system generates plans obsessively but executes shallowly. It scores projects but doesn't close loops. It spawns agents but doesn't verify their work. This review identifies **23 specific improvements** across 9 categories.

---

## 1. JUDGE SCORING — Currently Shallow & Inconsistent

### Problems

**1.1 Scoring is subjective with no calibration.**
The 5-dimension scoring (revenue_potential, strategic_value, completeness, urgency, effort_remaining) uses 0-10 scales with no rubric. Different judge models (Kimi K2.5 vs Sonnet) produce wildly different scores for the same repo. Evidence: `signal-studio-auth` jumped from 4.6→7.5 in one run — that's not the code changing, that's model variance.

**1.2 Composite formula weights are arbitrary.**
```python
composite = (
    revenue_potential * 2 +
    strategic_value * 2 +
    completeness * 1.5 +
    urgency * 2.5 +
    effort_remaining * 1
) / 9
```
Why is urgency weighted 2.5x but effort_remaining only 1x? A nearly-done project with low urgency should still rank high because it's cheap to ship. The weights should be data-driven, not gut-feel.

**1.3 No inter-rater reliability check.**
We never run the same repo through 2+ judges and compare. Without this, score variance is invisible.

**1.4 No delta tracking.**
Judges re-score from scratch each run. There's no mechanism to say "what changed since last score?" — leading to score drift that reflects model mood, not code reality.

### Recommendations

| # | Improvement | Effort | Impact |
|---|-------------|--------|--------|
| R1 | **Create scoring rubric** — define what a 7 vs 9 means for each dimension with concrete examples | S | High |
| R2 | **Dual-judge calibration** — run 2 judges per repo, flag >1.5pt divergence for human review | M | High |
| R3 | **Delta-based scoring** — judges receive last score + git diff since last run, score the delta | S | High |
| R4 | **Effort_remaining should be inverse-weighted higher** — nearly-done projects are the highest ROI | XS | Medium |
| R5 | **Add "test_coverage" and "security_posture" as scoring dimensions** — these are load-bearing and currently invisible | S | High |

---

## 2. HOOKS — Almost Entirely Unused

### Problems

**2.1 No git hooks on any project.**
All 15+ repos have only sample hooks (`.git/hooks/*.sample`). No pre-commit, no pre-push, no commit-msg validation. This means:
- No linting before commit
- No test execution before push
- No conventional commit enforcement
- No secret scanning

**2.2 No webhook hooks for CI triggers.**
Projects push to GitHub but there are no GitHub webhooks configured to trigger builds, tests, or deployments. Everything relies on Railway's auto-deploy (which only does "did it build?" not "did tests pass?").

**2.3 The judge swarm has no post-execution hooks.**
When a judge finishes scoring, nothing happens automatically. No notification, no TODO creation pipeline, no priority queue update. The consolidation cron runs separately on a timer — meaning there's a lag of up to 1 hour between judge completion and any action.

### Recommendations

| # | Improvement | Effort | Impact |
|---|-------------|--------|--------|
| R6 | **Install pre-commit framework** across all repos (ruff, mypy, bandit for Python; eslint, tsc for TS) | M | High |
| R7 | **Add commit-msg hook** enforcing conventional commits (feat/fix/chore/docs prefix) | S | Medium |
| R8 | **Create post-judge webhook** — when a judge completes, immediately trigger TODO creation + priority recalculation instead of waiting for hourly cron | M | High |
| R9 | **Secret scanning hook** — use `detect-secrets` or `gitleaks` as pre-commit to prevent API key leakage | S | Critical |

---

## 3. CI/CD PIPELINE — Essentially Non-Existent

### Problems

**3.1 Zero GitHub Actions workflows in ForwardLane projects.**
None of the core repos (signal-studio, signal-builder-backend, forwardlane-backend, NarrativeReactor, Ultrafone, core-entityextraction) have CI/CD pipelines. The only repos with workflows are `Second-Opinion` (inherited from a template) and `railway-saas-template`.

**3.2 Railway auto-deploy is not CI.**
Railway deploys on push if it builds. That's it. No test gate, no lint gate, no security scan, no coverage threshold. A push with failing tests deploys to production.

**3.3 No environment promotion.**
There's no staging → production pipeline. Every push to main goes directly to prod. For a $300K Invesco demo, this is reckless.

**3.4 No build matrix or cross-version testing.**
Python projects don't test against multiple Python versions. Node projects don't test against multiple Node versions.

### Recommendations

| # | Improvement | Effort | Impact |
|---|-------------|--------|--------|
| R10 | **Create a reusable GitHub Actions CI template** for Python (ruff + pytest + coverage gate + bandit) and TypeScript (eslint + vitest + tsc --noEmit) | M | Critical |
| R11 | **Add Railway deploy gate** — use Railway's deployment hooks to require CI green before deploy | S | Critical |
| R12 | **Implement staging environment** — at minimum for invesco-retention and signal-studio | M | High |
| R13 | **Coverage gates** — 70% minimum, fail CI below threshold. Currently no project measures coverage in CI. | S | High |

---

## 4. PR CREATION & REVIEW — Manual & Inconsistent

### Problems

**4.1 No automated PR creation.**
Agents push directly to main. There's no PR-based workflow. The only PRs ever created were manual (Bitbucket PRs #18 and #2056 on 2026-02-24). Sub-agents should create PRs, not push to main.

**4.2 No automated code review.**
When PRs do exist, there's no automated reviewer. No bot comments on code quality, test coverage delta, security issues, or dependency changes.

**4.3 No branch protection.**
Main branches are unprotected. Anyone (or any agent) can force-push.

### Recommendations

| # | Improvement | Effort | Impact |
|---|-------------|--------|--------|
| R14 | **Agents create PRs, not push to main** — every fix/feature goes through a PR with description, test results, and coverage delta | M | Critical |
| R15 | **Automated PR review agent** — spawn a review agent (Opus) when PR is created. It reads the diff, checks for: security issues, test coverage, style violations, architecture drift. Posts review comments. | L | High |
| R16 | **Enable branch protection** on main for all repos — require PR, require CI green, require 1 review (agent counts) | S | High |

---

## 5. BUG TRIAGE & SECURITY — Reactive Not Proactive

### Problems

**5.1 Bug triage is ad-hoc.**
The judge swarm finds bugs, creates TODOs, but there's no systematic triage process. 350 TODO files sit in `/todos/` with no clear workflow for which gets picked next. The `todo-progress` cron picks "next unblocked task" but the selection algorithm is opaque.

**5.2 Security review is post-hoc, not by-design.**
Security issues are found after code is written (e.g., Ultrafone's 7 API keys in git, no Twilio webhook validation, IDOR in signal-builder). The architecture doesn't enforce security patterns — each agent independently decides whether to add auth, CORS, rate limiting.

**5.3 No threat modeling.**
None of the PLAN.md files include threat models. For financial software handling advisor data, this is a compliance gap.

**5.4 No dependency vulnerability scanning in the loop.**
`pip-audit` was added to signal-builder-backend's Pipfile but never runs automatically. No equivalent for npm/pnpm projects.

### Recommendations

| # | Improvement | Effort | Impact |
|---|-------------|--------|--------|
| R17 | **Security-by-design template** — every agent prompt for new features MUST include: "Add authentication, input validation, rate limiting, and CORS. Write security tests first." | S | Critical |
| R18 | **Threat model in PLAN.md** — judges should generate a threat model section for each repo (attack surfaces, data classification, auth boundaries) | M | High |
| R19 | **Automated dependency scanning** — add `pip-audit` and `npm audit` to CI, run weekly via cron as well | S | High |
| R20 | **Bug triage scoring** — add severity/impact/exploitability scores to bugs, auto-sort by risk, security bugs always P0 | S | High |

---

## 6. TEST-DRIVEN DESIGN — Aspirational, Not Practiced

### Problems

**6.1 Tests are written after code, not before.**
Every sub-agent result shows "wrote code, then added tests." TDD means tests FIRST. The agent prompts don't enforce this.

**6.2 Test quality is shallow.**
Most tests are happy-path only. The signal-builder-backend has 533 test functions but I see no evidence of:
- Fuzz testing
- Property-based testing
- Negative test cases (what happens with malformed input?)
- Load/stress tests
- Integration tests that hit real databases

**6.3 No test infrastructure standardization.**
Python projects use a mix of pytest configurations. TypeScript projects use a mix of Vitest and Jest. No shared test utilities, no test data factories, no fixture libraries.

### Recommendations

| # | Improvement | Effort | Impact |
|---|-------------|--------|--------|
| R21 | **TDD-first agent prompt** — modify all coding agent prompts: "1. Write failing test. 2. Implement minimum code to pass. 3. Refactor. Show test output at each step." | S | High |
| R22 | **Test taxonomy requirement** — every PR must include: unit tests, edge case tests, error handling tests, and at least one integration test | M | High |

---

## 7. FRONTEND DESIGN SKILL — Never Used By Agents

### Problems

**7.1 The `frontend-design` skill exists but is never referenced in agent prompts.**
Sub-agents building frontend features (signal-studio-frontend, invesco-demo, Ultrafone iOS) don't load or follow the frontend-design skill. They produce generic, cookie-cutter UI.

**7.2 No design system enforcement.**
Each project uses different UI libraries (Ant Design, Radix, Tailwind, custom CSS). There's no shared design system or component library.

### Recommendation

| # | Improvement | Effort | Impact |
|---|-------------|--------|--------|
| R23 | **Auto-inject frontend-design skill** — when a task is classified as `frontend-development`, the agent prompt should include: "Read and follow /data/workspace/skills/compound-engineering/skills/frontend-design/SKILL.md" | S | High |

---

## 8. AGENT ARCHITECTURE — Spawn-Happy, Close-Loop-Shy

### Problems

**8.1 Agents spawn but don't verify.**
The self-healing monitor spawns Debug + Ops + QA agents. But QA runs after a fixed 3-minute delay, not after Debug/Ops actually finish. There's no dependency chain.

**8.2 Subagent timeouts are too aggressive.**
Multiple agents timed out today (fix-flipmyera, fix-ultrafone, fix-signal-builder-security). 10-minute timeouts for complex multi-file refactors are insufficient. But increasing timeouts wastes money on stuck agents.

**8.3 No iterative refinement loops.**
Agents run once and report. There's no "run tests → fix failures → run tests again" loop. The fix-narrative-reactor agent succeeded because it happened to get everything right in one pass. That's luck, not architecture.

**8.4 No agent specialization.**
Every agent gets the same generic prompt template. There's no "security specialist agent" or "test specialist agent" with domain-specific knowledge and tools.

**8.5 No shared context between agents.**
The blackboard exists but agents don't read it. Each agent starts from scratch, often rediscovering context that a previous agent already established.

### What's Missing: Iterative Agent Loops

The current pattern is: `spawn agent → wait → collect result`

It should be:
```
spawn agent → initial work → run tests → 
  if tests fail → fix failures → run tests →
    if tests fail → fix failures → run tests →
      if still failing → escalate to stronger model
  if tests pass → run security scan →
    if issues found → fix → re-scan
  → create PR → trigger review agent → merge if approved
```

---

## 9. MCP SERVER SPRAWL — Prefer CLIs Over Persistent Servers

### Problems

**9.1 MCP servers are heavyweight and wasteful for occasional use.**
Each MCP server is a persistent process consuming memory, requiring health checks, and adding failure surface area. Most tools (GitHub, Railway, file operations, git) have excellent CLI equivalents that are stateless, zero-overhead, and already available.

**9.2 MCP servers add latency and fragility.**
Server startup, JSON-RPC serialization, connection management — all overhead that a simple `gh pr create` or `railway logs` doesn't have. When an MCP server crashes mid-session, the entire tool becomes unavailable until restart.

**9.3 Agents should call CLIs directly or invoke MCP tools via CLI wrappers.**
Instead of `mcp_github.create_pr()`, use `exec("gh pr create --title ... --body ...")`. Instead of persistent Playwright MCP, use the `agent-browser` skill's CLI. Reserve MCP servers ONLY for tools that genuinely require persistent state (e.g., a database connection pool that would be expensive to re-establish per call).

### Recommendations

| # | Improvement | Effort | Impact |
|---|-------------|--------|--------|
| R24 | **Audit all MCP servers** — list which are running, kill any that have CLI equivalents | S | Medium |
| R25 | **CLI-first policy** — agent prompts should prefer `gh`, `railway`, `git`, `curl` over MCP servers | S | Medium |
| R26 | **MCP-via-CLI pattern** — for tools that only exist as MCP, invoke via `npx @modelcontextprotocol/tool-name` one-shot rather than persistent server | M | Medium |
| R27 | **Whitelist MCP servers** — only allow MCP servers that meet ALL criteria: (a) no CLI equivalent, (b) requires persistent state, (c) called >10x/session | S | High |

---

## 10. PROMPT CACHING & BATCH API — Not Used At All

### Problems

**9.1 No Anthropic Batch API usage.**
The judge swarm spawns 15+ agents sequentially through OpenClaw's subagent system. Anthropic's Batch API offers 50% cost reduction for non-time-sensitive work (like overnight judge swarms). This is free money left on the table.

**9.2 Prompt caching is accidental, not designed.**
The session_status shows 47% cache hit — but this is just OpenClaw's built-in caching, not deliberate prompt design. Judge prompts should be structured with static system instructions (cacheable) and dynamic repo content (variable), maximizing cache hits.

**9.3 No `/simplify` usage.**
Claude Code's `/simplify` command reduces complex code to its essence before analysis. Judges analyzing 150-model Django backends should simplify first to reduce token usage.

**9.4 No cost tracking per agent run.**
The learner module records outcomes in Postgres but doesn't track token usage or cost per agent. We can't optimize what we don't measure.

### Recommendations

For batch scoring jobs that run at 3 AM:
- Structure prompts with long, stable system prefix (cacheable across all 15 repos)
- Repo-specific content as the variable suffix
- Use Anthropic Batch API for the full swarm (50% cost savings)
- Track tokens_in/tokens_out per agent in Postgres

---

## Implementation Priority

### Wave 1 — This Week (Critical)
1. **R10** — CI template for Python + TypeScript
2. **R14** — Agents create PRs, not push to main  
3. **R17** — Security-by-design in all agent prompts
4. **R9** — Secret scanning hook
5. **R6** — Pre-commit framework

### Wave 2 — Next Week (High Impact)
6. **R1** — Scoring rubric
7. **R3** — Delta-based scoring  
8. **R21** — TDD-first agent prompts
9. **R8** — Post-judge webhook
10. **R23** — Auto-inject frontend-design skill

### Wave 3 — Following Week (Architecture)
11. **R15** — Automated PR review agent
12. **R2** — Dual-judge calibration
13. **R12** — Staging environment
14. **R18** — Threat models
15. Iterative agent loops with test verification

### Wave 4 — Optimization
16. Batch API for overnight swarms
17. Prompt caching optimization
18. Cost tracking per agent
19. Agent specialization (security, test, frontend)

---

## Cost Impact Estimate

| Improvement | Savings/Value |
|------------|---------------|
| Batch API for judge swarms | ~50% on overnight runs (~$X/day) |
| Prompt caching optimization | ~30% fewer tokens on repeated judge calls |
| PR gates preventing broken deploys | Prevents $300K Invesco demo failures |
| Security-by-design | Prevents credential leaks, IDOR exploits |
| TDD-first | Catches bugs before deploy, not after |
| Iterative loops | Higher first-pass success rate → fewer retries |

---

## Conclusion

The system has the right *ambition* — compound intelligence, self-healing, multi-agent orchestration. But execution is stuck in "generate plans" mode. The gap between where we are (350 TODO files, no CI, no PRs, no hooks, agents pushing to main) and where we need to be (automated CI/CD, PR-based workflow, security-by-design, TDD, iterative agent loops) is significant but closeable in 3-4 weeks of focused work.

**The north star should shift from "score more repos and generate more TODOs" to "close loops on existing TODOs with verified, tested, secure code through automated pipelines."**

More plans won't make the Invesco demo more secure. More tests will.
