# TODO-395: Upgrade Dev Dependency CVEs

**Repo:** signal-builder-backend  
**Priority:** Low  
**Status:** Pending  
**Created:** 2026-03-02  

## Description

pip-audit found CVEs in dev/build dependencies. All are dev-only (not production risk),
but should be pinned to fixed versions to keep audit clean:

| Package | Current | Fix Version | CVE |
|---------|---------|-------------|-----|
| filelock | 3.12.4 | 3.20.3 | CVE-2025-68146, CVE-2026-22701 |
| gitpython | 3.1.40 | 3.1.41 | PYSEC-2024-4 |
| setuptools | 68.2.2 | 78.1.1 | PYSEC-2025-49, CVE-2024-6345 |
| virtualenv | 20.24.5 | 20.36.1 | PYSEC-2024-187, CVE-2026-22702 |

## Execution Prompt

```
You are upgrading dev dependency CVEs in signal-builder-backend at 
/data/workspace/projects/signal-builder-backend/.

Steps:
1. Update Pipfile dev-packages section to pin fixed versions:
   - filelock = ">=3.20.3"  (indirect dep — may need constraint via pipenv)
   - gitpython = ">=3.1.41"
   - setuptools = ">=78.1.1"
   - virtualenv = ">=20.36.1"
2. Run: `pipenv update --dev` to update lockfile
3. Run: `pip-audit` to confirm no HIGH/MEDIUM CVEs remain
4. Run: `pytest` to confirm nothing broke
5. Update AUDIT.md security baseline section with new clean status

Note: These are indirect/build deps. If direct pinning isn't possible in Pipfile,
add constraints to Pipfile.lock via `pipenv lock --clear`.
```

## Effort Estimate
- XS (30 min)

## Acceptance Criteria
- [ ] `pip-audit` returns 0 HIGH severity CVEs
- [ ] All tests pass
- [ ] AUDIT.md updated with new clean baseline
