# TODO-508: Add Ruff + mypy to CI

**Repo:** core-entityextraction
**Priority:** P1
**Effort:** S (2h)
**Dependencies:** None
**Blocks:** None

## Description
Add linting and type checking to the CI pipeline.

## Coding Prompt
```
In /data/workspace/projects/core-entityextraction/:

1. Add ruff, mypy to requirements.txt (or dev-requirements.txt)
2. Create pyproject.toml with:
   [tool.ruff]
   line-length = 120
   select = ["E", "F", "I", "W"]
   
   [tool.mypy]
   python_version = "3.11"
   warn_return_any = true
   warn_unused_configs = true
   
3. Update bitbucket-pipelines.yml:
   - Add step: ruff check .
   - Add step: mypy main.py persistence.py
   - Add step: pytest --cov --cov-fail-under=70

4. Create .pre-commit-config.yaml with ruff and mypy hooks
5. Fix any immediate ruff/mypy errors in main.py and persistence.py
```

## Acceptance Criteria
- [ ] `ruff check .` passes
- [ ] `mypy main.py persistence.py` passes (or has explicit ignores for third-party)
- [ ] CI pipeline updated with lint + type check steps
- [ ] Pre-commit hooks configured
