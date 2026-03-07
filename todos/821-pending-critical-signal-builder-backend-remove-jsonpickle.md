# TODO-821: Remove jsonpickle — Security Risk (RCE)

**Repo**: signal-builder-backend  
**Priority**: CRITICAL  
**Effort**: Low (2-4 hours)

## Problem
`jsonpickle.decode()` can instantiate arbitrary Python objects from untrusted input. The `# nosec B301` bandit suppression bypasses security scanning.

**File**: `apps/signals/schemas/signal.py:7,112,129`

## Task
1. Audit all `jsonpickle` usages in the codebase (currently only in `signal.py`)
2. Replace `jsonpickle.encode(v)` with `json.dumps(v, default=json_datetime_encoder)` (helper exists in `core/helpers.py`)
3. Replace `jsonpickle.decode(v)` with `json.loads(v)` — the `sql_params` field should only contain JSON-serializable dicts
4. Remove `jsonpickle` from `Pipfile`
5. Run full test suite: `pipenv run pytest`
6. Remove the `# nosec B301` suppression comment

## Acceptance Criteria
- No `jsonpickle` imports anywhere in the codebase
- `sql_params` field serializes/deserializes correctly via stdlib json
- All 134+ unit tests pass
- `pipenv run security` (bandit) passes without suppressions on this file
