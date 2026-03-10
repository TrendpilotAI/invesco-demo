# 899 — Fix numpy/pandas Binary Incompatibility in Test Environment

**Repo:** signal-studio-data-provider  
**Priority:** Critical (P0) — blocks ALL tests  
**Effort:** XS (~10 minutes)  
**Dependencies:** None  

---

## Problem

Running `pytest` in the project venv fails immediately with:
```
ValueError: numpy.dtype size changed, may indicate binary incompatibility. Expected 96 from C header, got 88 from PyObject
```
This means numpy was compiled against a different version of Python/C headers than what's installed. All 3 test files fail to collect, so zero tests are running in CI.

## Files to Change

- `/data/workspace/projects/signal-studio-data-provider/pyproject.toml` — add version pins
- `.venv` — upgrade packages

## Coding Prompt

```
Fix the numpy/pandas binary incompatibility in the signal-studio-data-provider project.

Steps:
1. In /data/workspace/projects/signal-studio-data-provider/, run:
   .venv/bin/pip install --upgrade numpy pandas

2. If that fails, try:
   .venv/bin/pip install --force-reinstall numpy pandas

3. Update pyproject.toml to pin compatible versions to prevent regression:
   [project]
   dependencies = [
       "pydantic>=2.0",
       "pandas>=2.1,<3.0",
       "numpy>=1.26,<2.0",
   ]

4. Verify tests pass:
   cd /data/workspace/projects/signal-studio-data-provider
   .venv/bin/pytest tests/ -q 2>&1 | tail -20
```

## Acceptance Criteria

- [ ] `pytest tests/` completes collection without errors
- [ ] All previously-passing tests still pass
- [ ] numpy and pandas version pins added to `pyproject.toml`
