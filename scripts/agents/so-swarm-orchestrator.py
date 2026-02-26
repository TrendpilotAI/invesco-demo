#!/usr/bin/env python3
"""
Second Opinion TDD Swarm Orchestrator

Architecture:
  Phase N:
    1. Opus 4.6 (Planner) → TDD plan already generated in TDD_SWARM_PLAN.md
    2. Sonnet 4-6 (Developer) → Implements code + tests for phase
    3. Opus 4.6 (Evaluator) → Scores work, gives feedback
    4. Loop: Dev applies fixes → Eval re-scores → until 9/10 or max iterations
    5. → Next Phase

Runs sequentially through phases, spawning sub-agents via OpenClaw.
"""

import json
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

PROJECT_DIR = "/data/workspace/projects/Second-Opinion"
PLAN_FILE = f"{PROJECT_DIR}/TDD_SWARM_PLAN.md"
LOG_DIR = Path("/data/workspace/projects/Second-Opinion/swarm-logs")
LOG_DIR.mkdir(exist_ok=True)

# Models
DEV_MODEL = "anthropic/claude-sonnet-4-6"  # Codex 5.3 not available via gateway
EVAL_MODEL = "anthropic/claude-opus-4-6"
MAX_ITERATIONS = 3
TARGET_SCORE = 9

PHASES = [
    {
        "id": 1,
        "name": "Test Infrastructure & Foundation",
        "focus": "Fix vitest config, create test utilities, get all existing tests passing",
    },
    {
        "id": 2,
        "name": "Service Layer TDD",
        "focus": "Write tests for all 25+ services, implement/fix to pass",
    },
    {
        "id": 3,
        "name": "Hook Layer TDD",
        "focus": "Write tests for all 5 hooks with state transitions and error handling",
    },
    {
        "id": 4,
        "name": "Component Layer TDD",
        "focus": "Write tests for all 40+ components with rendering and interaction",
    },
    {
        "id": 5,
        "name": "Analysis Pipeline Integration",
        "focus": "End-to-end pipeline tests: upload → triage → analysis → consensus → display",
    },
    {
        "id": 6,
        "name": "Security & HIPAA",
        "focus": "Encryption, auth flows, data retention, firestore rules tests",
    },
    {
        "id": 7,
        "name": "Error Handling & Edge Cases",
        "focus": "Network failures, invalid inputs, rate limiting, concurrent uploads",
    },
    {
        "id": 8,
        "name": "Performance & Polish",
        "focus": "Lazy loading, bundle size, render perf, i18n, a11y audit",
    },
]


def log(msg: str):
    ts = datetime.utcnow().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}")
    with open(LOG_DIR / "orchestrator.log", "a") as f:
        f.write(f"[{ts}] {msg}\n")


def spawn_agent(label: str, model: str, task: str, thinking: str = "high") -> dict:
    """Spawn a sub-agent via OpenClaw sessions_spawn."""
    log(f"  Spawning agent: {label} (model={model.split('/')[-1]})")

    # Write task to a temp file to avoid shell escaping issues
    task_file = LOG_DIR / f"{label}-task.md"
    with open(task_file, "w") as f:
        f.write(task)

    # Use openclaw CLI or direct API
    # For now, we'll write the spawn command for the main agent to execute
    spawn_info = {
        "label": label,
        "model": model,
        "task": task,
        "thinking": thinking,
        "spawned_at": datetime.utcnow().isoformat(),
    }

    with open(LOG_DIR / f"{label}-spawn.json", "w") as f:
        json.dump(spawn_info, f, indent=2)

    return spawn_info


def generate_dev_task(phase: dict, plan_content: str, iteration: int = 1, feedback: str = "") -> str:
    """Generate the developer agent's task prompt."""
    phase_section = f"Phase {phase['id']}: {phase['name']}"

    feedback_block = ""
    if feedback:
        feedback_block = f"""
### EVALUATOR FEEDBACK FROM ITERATION {iteration - 1}
The Opus evaluator scored your previous work and provided this feedback. Address ALL items:

{feedback}

Fix every issue mentioned. The evaluator will re-score after your changes.
"""

    return f"""## DEVELOPER AGENT — Second Opinion TDD Phase {phase['id']}: {phase['name']}
**Iteration:** {iteration}/{MAX_ITERATIONS}
**Model:** {DEV_MODEL}
**Project:** {PROJECT_DIR}

You are a senior developer implementing TDD for the Second Opinion medical AI app.

### YOUR MISSION
Implement Phase {phase['id']}: **{phase['name']}**
Focus: {phase['focus']}

### INSTRUCTIONS
1. Read the TDD plan at `{PLAN_FILE}` — find the section for "{phase_section}"
2. Follow the plan EXACTLY — write tests first, then make them pass
3. Run `cd {PROJECT_DIR} && npx vitest run` after each change to verify
4. Run `cd {PROJECT_DIR} && npx vitest run --coverage` at the end
5. Commit your changes with descriptive messages

{feedback_block}

### RULES
- Write tests BEFORE implementation (true TDD)
- Every test must have clear assertions
- Mock external dependencies (Firebase, Gemini API, fetch)
- No skipped tests — everything must pass
- Type-safe — no `any` types
- Follow existing test patterns in `tests/`

### DELIVERABLE
When done, write a summary to `{LOG_DIR}/phase{phase['id']}-dev-iter{iteration}.md` with:
1. Files created/modified
2. Tests written (count)
3. Tests passing (count)
4. Coverage percentage
5. Any issues or blockers

Then run `cd {PROJECT_DIR} && npx vitest run 2>&1 | tail -30` and include the output.
"""


def generate_eval_task(phase: dict, iteration: int) -> str:
    """Generate the evaluator agent's task prompt."""
    return f"""## EVALUATOR AGENT — Second Opinion TDD Phase {phase['id']}: {phase['name']}
**Iteration:** {iteration}/{MAX_ITERATIONS}
**Model:** {EVAL_MODEL}

You are a senior QA engineer and code reviewer evaluating the developer's TDD work.

### YOUR MISSION
Review and score the developer's implementation of Phase {phase['id']}: **{phase['name']}**

### EVALUATION PROCESS
1. Read the TDD plan at `{PLAN_FILE}` — find Phase {phase['id']} requirements
2. Read the dev's summary at `{LOG_DIR}/phase{phase['id']}-dev-iter{iteration}.md`
3. Review ALL modified/created files in `{PROJECT_DIR}`
4. Run `cd {PROJECT_DIR} && npx vitest run` — verify all tests pass
5. Run `cd {PROJECT_DIR} && npx vitest run --coverage` — check coverage
6. Review code quality, test quality, architecture

### SCORING RUBRIC (each /10)
1. **Test Quality** — Are tests meaningful? Do they test real behavior? Edge cases?
2. **Code Quality** — Clean, typed, no hacks, follows patterns?
3. **Coverage** — Does coverage meet the phase target?
4. **Architecture** — Proper module structure, separation of concerns?
5. **Completeness** — Are ALL items from the TDD plan addressed?
6. **Overall** — Holistic score

### DELIVERABLE
Write your evaluation to `{LOG_DIR}/phase{phase['id']}-eval-iter{iteration}.md` with:

```
## Phase {phase['id']} Evaluation — Iteration {iteration}

### Scores
- Test Quality: X/10
- Code Quality: X/10
- Coverage: X/10
- Architecture: X/10
- Completeness: X/10
- **Overall: X/10**

### What's Good
- ...

### Issues Found
1. [CRITICAL] ...
2. [HIGH] ...
3. [MEDIUM] ...

### Specific Fixes Required
1. File: path/to/file.ts — Line X: [what to fix]
2. ...

### Test Output
[paste vitest output]

### Coverage Report
[paste coverage summary]

### VERDICT
PASS (score >= 9) or FAIL (needs another iteration)
```

If Overall score is >= {TARGET_SCORE}/10, write VERDICT: PASS
If Overall score is < {TARGET_SCORE}/10, write VERDICT: FAIL and provide detailed fix instructions.
"""


def run_phase(phase: dict, plan_content: str):
    """Run a single phase through the dev→eval→feedback loop."""
    log(f"\n{'='*60}")
    log(f"PHASE {phase['id']}: {phase['name']}")
    log(f"{'='*60}")

    for iteration in range(1, MAX_ITERATIONS + 1):
        log(f"\n--- Iteration {iteration}/{MAX_ITERATIONS} ---")

        # Read previous eval feedback if exists
        feedback = ""
        if iteration > 1:
            eval_file = LOG_DIR / f"phase{phase['id']}-eval-iter{iteration-1}.md"
            if eval_file.exists():
                feedback = eval_file.read_text()

        # Step 1: Developer implements
        dev_task = generate_dev_task(phase, plan_content, iteration, feedback)
        dev_label = f"so-dev-p{phase['id']}-i{iteration}"
        spawn_agent(dev_label, DEV_MODEL, dev_task)

        log(f"  → Developer agent spawned: {dev_label}")
        log(f"  → Waiting for developer to complete...")

        # Step 2: Evaluator reviews
        eval_task = generate_eval_task(phase, iteration)
        eval_label = f"so-eval-p{phase['id']}-i{iteration}"
        spawn_agent(eval_label, EVAL_MODEL, eval_task)

        log(f"  → Evaluator agent spawned: {eval_label}")

        # Record phase state
        state = {
            "phase": phase["id"],
            "iteration": iteration,
            "dev_label": dev_label,
            "eval_label": eval_label,
            "timestamp": datetime.utcnow().isoformat(),
        }
        with open(LOG_DIR / f"phase{phase['id']}-state.json", "w") as f:
            json.dump(state, f, indent=2)

        log(f"  → Phase {phase['id']} iteration {iteration} agents prepared")

    return True


def main():
    """Main orchestration loop."""
    log("=" * 60)
    log("SECOND OPINION TDD SWARM ORCHESTRATOR")
    log(f"Started: {datetime.utcnow().isoformat()}")
    log(f"Phases: {len(PHASES)}")
    log(f"Dev model: {DEV_MODEL}")
    log(f"Eval model: {EVAL_MODEL}")
    log(f"Max iterations per phase: {MAX_ITERATIONS}")
    log(f"Target score: {TARGET_SCORE}/10")
    log("=" * 60)

    # Check if plan exists
    if not Path(PLAN_FILE).exists():
        log(f"ERROR: TDD plan not found at {PLAN_FILE}")
        log("Run the planner agent first (so-planner-phase0)")
        sys.exit(1)

    plan_content = Path(PLAN_FILE).read_text()
    log(f"TDD plan loaded ({len(plan_content)} chars)")

    # Determine which phase to start from
    start_phase = int(sys.argv[1]) if len(sys.argv) > 1 else 1

    for phase in PHASES:
        if phase["id"] < start_phase:
            continue
        run_phase(phase, plan_content)

    log("\n" + "=" * 60)
    log("ALL PHASES PREPARED — Check swarm-logs/ for agent tasks")
    log("=" * 60)


if __name__ == "__main__":
    main()
