# TODO-515: Update CI Pipeline (Bitbucket Pipelines)

**Repo:** core-entityextraction
**Priority:** P1
**Effort:** S (2h)
**Dependencies:** TODO-503 (tests), TODO-508 (ruff/mypy)
**Blocks:** None

## Description
Current bitbucket-pipelines.yml is likely outdated from Flask era. Update with modern test/lint/build steps.

## Coding Prompt
```
In /data/workspace/projects/core-entityextraction/bitbucket-pipelines.yml:

1. Update pipeline to:
   - Step 1: Install deps (pip install -r requirements.txt)
   - Step 2: Lint (ruff check .)
   - Step 3: Type check (mypy main.py persistence.py)
   - Step 4: Test (pytest --cov --cov-fail-under=70)
   - Step 5: Docker build + push (on main branch only)
   - Step 6: Deploy to Railway (on main branch, after tests pass)

2. Add post-deploy health check: curl $RAILWAY_URL/health
3. Use Python 3.11 image
4. Cache pip packages between builds
```

## Acceptance Criteria
- [ ] Pipeline runs lint, type check, test, build, deploy
- [ ] Fails on lint errors, type errors, or coverage < 70%
- [ ] Docker build succeeds
- [ ] Post-deploy health check passes
