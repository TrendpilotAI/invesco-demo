# 215 · CI PIPELINE — ADD PR TEST GATE AND DEVELOPMENT BRANCH TESTS

**Repo:** forwardlane-backend  
**Priority:** P1 (code can currently merge to development without any test run)  
**Effort:** S (1–2 hours)  
**Status:** pending

---

## Task Description

The current `bitbucket-pipelines.yml` only runs tests on the `master` branch. The `development`
branch triggers a downstream pipeline but does NOT run tests. This means:
- Broken code can merge to `development` undetected
- Only discovered when the next PR hits `master`

**Fix:**
1. Add a `pull-requests: '**':` section to run tests on ALL PRs regardless of target branch
2. Add test step to the `development` branch pipeline
3. Ensure the analytical DB is properly handled in CI (either mocked in tests or added as a CI service)

---

## Coding Prompt (Agent-Executable)

```
You are modifying forwardlane-backend at /data/workspace/projects/forwardlane-backend/.

TASK: Update bitbucket-pipelines.yml to run tests on all PRs and on the development branch.

STEP 1 — Read the current pipeline config:
Run: cat /data/workspace/projects/forwardlane-backend/bitbucket-pipelines.yml

Understand the existing structure: services, caches, step definitions.

STEP 2 — Identify the test step definition:
Find the step that runs tests (likely something like: pip install tox && tox).
Note the service definitions (postgres, redis) it requires.
Note the image it uses.

STEP 3 — Add pull-requests section:
In bitbucket-pipelines.yml, add a pull-requests section that runs the same test step
for all branch patterns.

Example structure to ADD (adapt exact step content from existing master pipeline):

pull-requests:
  '**':
    - step: &test-step
        name: Run Tests (PR Gate)
        image: python:3.9
        services:
          - postgres
          - redis
        caches:
          - pip
        script:
          - pip install tox
          - tox

NOTE: Use YAML anchors (&test-step, *test-step) to avoid duplicating the step definition
if the same step is used in multiple places.

STEP 4 — Add tests to development branch:
Find the development: section. It likely looks like:
  branches:
    development:
      - step:
          name: Trigger downstream
          script: ...

Modify it to run tests BEFORE the downstream trigger:
  branches:
    development:
      - step: *test-step       # Run tests first (reuse anchor from above)
      - step:
          name: Trigger downstream
          script: ...           # Keep existing downstream step

STEP 5 — Handle analytical DB in CI:
The test postgres service in CI only creates the 'forwardlane' database.
Tests that hit the analytical DB need either:
  a) A second postgres service configured for analytical, OR
  b) All analytical DB calls mocked in tests (preferred — see TODO #214)

Check whether any test attempts to connect to 'analytical' DB:
  - If tests from TODO #214 mock all DB calls → no CI change needed
  - If tests need a real analytical DB → add a second postgres service:

services:
  postgres:
    image: postgres
    environment:
      POSTGRES_DB: forwardlane
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: test
  postgres_analytical:
    image: postgres
    environment:
      POSTGRES_DB: analytical
      POSTGRES_USER: analytical
      POSTGRES_PASSWORD: analytical_test
  redis:
    image: redis

And add environment variable in the test step:
  ANALYTICAL_DATABASE_URL: postgresql://analytical:analytical_test@localhost:5433/analytical

STEP 6 — Verify YAML syntax:
Run: python3 -c "import yaml; yaml.safe_load(open('bitbucket-pipelines.yml'))" && echo "Valid YAML"

STEP 7 — Check tox.ini includes easy_button and analytical:
Run: cat /data/workspace/projects/forwardlane-backend/tox.ini | grep -A5 "commands"
If easy_button/analytical are not in the test commands, add them (see also TODO #214).
```

---

## Files to Modify

| File | Change |
|------|--------|
| `bitbucket-pipelines.yml` | Add `pull-requests` section + test step in `development` branch |
| `tox.ini` | Ensure `easy_button` and `analytical` test directories are included |

---

## Acceptance Criteria

- [ ] `bitbucket-pipelines.yml` has a `pull-requests: '**':` section that runs tests
- [ ] The `development` branch pipeline runs tests before any downstream trigger
- [ ] Tests run on PRs targeting any branch (not just master)
- [ ] YAML is valid (`yaml.safe_load()` passes)
- [ ] CI postgres service creates the analytical database (or tests mock it — see TODO #214)
- [ ] Existing master branch pipeline behavior is unchanged
- [ ] No duplicate step definitions (use YAML anchors)

---

## Notes

- This TODO depends on TODO #214 (tests must exist before CI gate has value)
- If TODO #214 mocks all DB calls, no second postgres service is needed in CI
- The existing `development` downstream trigger should be kept — only add tests BEFORE it
- Consider adding `--exit-zero` to bandit in tox.ini so security warnings don't block CI
  (or fix all bandit warnings first — see AUDIT.md section 3.3)
