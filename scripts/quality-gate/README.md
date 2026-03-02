# Quality Gate — Minimal, Practical, Effective

## The Problem

We had 350+ TODO files, zero CI, zero git hooks, agents pushing to main. Quality was theater.

## The Solution

Four scripts, one template. No frameworks. No MCP.

## Files

| File | Purpose |
|------|---------|
| `quality-check.sh` | Run before every commit. Secrets → Lint → Tests. JSON metrics output. |
| `agent-pr.sh` | Create branch, commit, push, PR. UUID branches, idempotent, retry-safe. |
| `auto-review.sh` | Automated heuristic PR review (NOT LLM - just pattern matching). |
| `agent-template.md` | Template to inject into ALL coding agent prompts. |
| `ci-template.yml` | GitHub Actions workflow using quality-check.sh. |

## Usage

### For Agents

```bash
# Before committing
bash /data/workspace/scripts/quality-gate/quality-check.sh .

# After code works, to create PR
bash /data/workspace/scripts/quality-gate/agent-pr.sh "feat: description" "PR body"

# Automated review (heuristic only - NOT AI)
bash /data/workspace/scripts/quality-gate/auto-review.sh owner/repo 123
```

### For CI

```bash
# Add to any repo
cp ci-template.yml .github/workflows/ci.yml
```

### Quality Gate Flow

```
Code written
    ↓
quality-check.sh (local) → JSON metrics to /tmp/quality-metrics.json
    ↓ fail? → fix → re-run
    ↓ pass
agent-pr.sh → branch → commit → push → PR
    ↓
auto-review.sh → automated heuristic checks
    ↓ fail? → fix → re-run
    ↓ pass
human review → merge
```

## Metrics

quality-check.sh outputs JSON to `/tmp/quality-metrics.json`:
```json
{
  "repo": "signal-builder-backend",
  "timestamp": "2026-03-01T12:55:00Z",
  "result": "pass",
  "pass": 3,
  "fail": 0,
  "checks": {
    "secrets": "pass",
    "lint": "pass",
    "tests": "pass"
  }
}
```

## Principles

1. **Fast-fail** — cheapest checks first (lint), expensive last (tests)
2. **No theater** — every check catches real issues
3. **Metrics** — JSON output for observability
4. **Honest** — auto-review is pattern-matching, NOT AI
5. **Idempotent** — can run 100 times, same result
6. **CI-first** — if it's not in CI, it doesn't exist

## Integration

Add to your agent prompt template:

```
## Quality Gate

Before committing:
  bash /data/workspace/scripts/quality-gate/quality-check.sh .

If it fails, fix and re-run. Do not commit failing code.

To create a PR:
  bash /data/workspace/scripts/quality-gate/agent-pr.sh "type: description" "body"
```

## Dependencies

- `gh` — GitHub CLI (for agent-pr.sh, auto-review.sh)
- `ruff` — Python linting (pip install ruff)
- `pytest` — Python tests
- `eslint` + `tsc` — TypeScript (project-local)

Everything else is bash built-ins.
