# TODO 009 — Add mypy Type Checking to CI Pipeline

**Status:** pending  
**Priority:** high  
**Repo:** signal-builder-backend  
**Effort:** M (1-2 days)

## Problem

The codebase uses Python type hints throughout but mypy is not configured or enforced. This means:
- Type errors silently reach production
- Refactors break type contracts without detection
- IDE support is degraded without proper mypy config

The existing `.pre-commit-config.yaml` and `bitbucket-pipelines.yml` do not include mypy.

## Files Affected

- `mypy.ini` (new)
- `.pre-commit-config.yaml`
- `bitbucket-pipelines.yml`
- `Pipfile` (add mypy to dev-packages)
- Potentially: various `*.py` files where type errors are discovered

## Coding Prompt

```
You are adding mypy type checking to signal-builder-backend.

1. Add mypy to Pipfile [dev-packages]:
   mypy = "*"
   types-redis = "*"
   types-passlib = "*"

2. Create /data/workspace/projects/signal-builder-backend/mypy.ini:
   [mypy]
   python_version = 3.11
   ignore_missing_imports = True
   warn_return_any = False
   warn_unused_configs = True
   exclude = (migrations|scripts/one_time_scripts|tests)
   
   [mypy-dependency_injector.*]
   ignore_missing_imports = True
   
   [mypy-fastapi_jwt_auth.*]
   ignore_missing_imports = True

3. Run mypy on the codebase: mypy apps/ core/ settings/ --config-file mypy.ini
   Fix the most critical type errors (Any returns on core paths, wrong return types)
   For non-critical issues, add # type: ignore[...] comments with explanatory notes
   Goal: get mypy to exit 0 with the above config

4. Add to .pre-commit-config.yaml:
   - repo: https://github.com/pre-commit/mirrors-mypy
     rev: v1.8.0
     hooks:
       - id: mypy
         args: [--config-file=mypy.ini]
         additional_dependencies: [types-redis, types-passlib]

5. Add to bitbucket-pipelines.yml in the test step:
   - pipenv run mypy apps/ core/ settings/ --config-file mypy.ini

Document all type errors found but not immediately fixable in a MYPY_ISSUES.md file.
```

## Acceptance Criteria

- [ ] `mypy apps/ core/ settings/` exits with code 0 (or only known suppressions)
- [ ] mypy runs in pre-commit hooks
- [ ] mypy runs in Bitbucket Pipelines CI
- [ ] No regressions in existing tests

## Dependencies

- TODO 007 (pin deps) — should be done first so mypy type stubs are pinned
