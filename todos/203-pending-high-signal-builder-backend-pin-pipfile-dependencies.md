# TODO 203 — Pin Pipfile Dependencies (HIGH)

**Project:** signal-builder-backend  
**Priority:** HIGH  
**Estimated Effort:** 2 hours  
**Status:** pending  
**Dependencies:** 200, 201, 202 (run after security fixes so lock file includes any new deps)

---

## Task Description

The `Pipfile` uses wildcard (`*`) versions for critical packages including `fastapi-jwt-auth`, `loguru`, `passlib`, `uvicorn`, `pydantic`, `celery`, `redis`, and `pandas`. Wildcard dependencies are a security and reproducibility timebomb:

- A breaking upstream release can silently corrupt production deployments
- Security advisories may be silently included or excluded
- Build reproducibility is impossible — CI may pass while prod uses a different version

**Fix:**
1. Run `pipenv lock` to generate a fresh `Pipfile.lock` with all resolved versions.
2. Pin all production packages to exact or bounded version ranges in `Pipfile`.
3. Audit for known CVEs using `pip-audit`.
4. Add `pip-audit` to the CI pipeline.
5. Ensure `Pipfile.lock` is committed to version control.

---

## Coding Prompt (Autonomous Agent)

```
TASK: Pin all Pipfile dependencies in signal-builder-backend

REPO: /data/workspace/projects/signal-builder-backend/

STEPS:

1. Read current Pipfile to understand what's wildcard:
   ```bash
   cat Pipfile
   ```

2. In the repo directory, run:
   ```bash
   cd /data/workspace/projects/signal-builder-backend
   pipenv install  # ensure env is up to date
   pipenv lock     # resolve and lock all deps
   ```

3. Read the generated Pipfile.lock and extract pinned versions for each wildcard package.

4. Update `Pipfile` to replace `"*"` with the resolved versions as bounded ranges:
   - Format: `package = ">=X.Y.Z,<(X+1).0.0"` for major-version-safe pinning
   - OR exact pins: `package = "==X.Y.Z"` for maximum reproducibility
   
   Example replacements:
   ```toml
   [packages]
   fastapi = "==0.92.0"           # or whatever pipenv resolved
   fastapi-jwt-auth = "==0.5.0"   # replace * with actual resolved version
   loguru = ">=0.7.0,<1.0.0"
   passlib = ">=1.7.4,<2.0.0"
   uvicorn = ">=0.20.0,<1.0.0"
   pydantic = ">=1.10.0,<2.0.0"   # NOTE: check if codebase is v1 or v2 compatible!
   celery = ">=5.2.0,<6.0.0"
   redis = ">=4.5.0,<6.0.0"
   pandas = ">=1.5.0,<3.0.0"
   ```

5. IMPORTANT: Check pydantic compatibility:
   ```bash
   grep -rn "from pydantic import\|pydantic.v1\|validator\|root_validator" apps/ --include="*.py" | head -20
   ```
   If using v1-style validators, pin `pydantic = ">=1.10.0,<2.0.0"`.
   If already using v2, pin accordingly.

6. Install pip-audit:
   ```bash
   pip install pip-audit
   pip-audit -r <(pipenv run pip freeze)
   ```
   Or add to Pipfile dev dependencies:
   ```toml
   [dev-packages]
   pip-audit = ">=2.6.0"
   ```

7. Run pip-audit and document any CVEs found:
   ```bash
   pipenv run pip-audit
   ```
   For any high/critical CVEs, upgrade the affected package immediately.

8. Update `bitbucket-pipelines.yml` (CI config) to add pip-audit step:
   ```yaml
   - step:
       name: Security Audit
       script:
         - pip install pip-audit
         - pip-audit -r requirements.txt  # or pipenv run pip-audit
   ```

9. Verify `Pipfile.lock` is NOT in `.gitignore`:
   ```bash
   grep "Pipfile.lock" .gitignore
   ```
   If found, remove that line — Pipfile.lock MUST be committed.

10. Commit both `Pipfile` and `Pipfile.lock`:
    "deps: pin all Pipfile dependencies to resolved versions, add pip-audit"

11. Verify fresh install still works:
    ```bash
    pipenv install --ignore-pipfile  # install from lock file only
    pipenv run python -c "import fastapi, celery, pandas, redis; print('OK')"
    ```

NOTES:
- `fastapi-jwt-auth` may be archived/unmaintained. Check and consider migration to
  `python-jose` + manual JWT handling, or `fastapi-users` if a replacement is needed.
  Document this as a follow-up TODO if the library is EOL.
- `sqlalchmy` version: check if using 1.4 vs 2.0 async API — pin to whichever is in use.

VERIFICATION:
- `grep '= "\*"' Pipfile` returns nothing
- `pipenv install --ignore-pipfile` succeeds cleanly
- `pipenv run pip-audit` returns no CRITICAL vulnerabilities
- Tests pass after pinning
```

---

## Dependencies

- **200** (CORS fix) — run after to include any new deps in lock file
- **201** (JWT secrets fix) — same reason
- **202** (SQL injection fix adds `sqlglot`) — run after to lock sqlglot version

## Acceptance Criteria

- [ ] No `"*"` wildcards remain in `Pipfile` for production packages
- [ ] `Pipfile.lock` is committed to version control
- [ ] `pip-audit` runs clean (no CRITICAL CVEs, HIGH CVEs documented)
- [ ] `pip-audit` added to CI pipeline
- [ ] App still starts and all tests pass after pinning
- [ ] Note added to README about updating lock file workflow (`pipenv update`)
