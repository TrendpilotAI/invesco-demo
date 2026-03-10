# TODO-831: Add Alembic Check Step to CI Pipeline

**Repo:** signal-builder-backend  
**Priority:** HIGH  
**Effort:** XS (1 hour)  
**Status:** pending

## Problem

There's no CI check that detects when SQLAlchemy models have changed but no migration was generated. Developers can forget to run `alembic revision --autogenerate` and silently ship model changes without corresponding migrations. This causes production deploy failures.

## Fix

Add `alembic check` step to `bitbucket-pipelines.yml`. This command fails if there are detected model changes without a migration file:

```bash
alembic check
# Exit code 1 if models differ from DB schema (pending migrations)
# Exit code 0 if everything is up to date
```

## Coding Prompt

```yaml
# In bitbucket-pipelines.yml, add after the existing test step:

- step:
    name: Migration Check
    script:
      - pip install pipenv
      - pipenv install --dev
      - alembic check
    # This will fail if any SQLAlchemy model changes lack a migration file
```

Also add to GitHub Actions workflow if one exists (`.github/workflows/`).

Add a comment in `alembic.ini` documenting the check:
```ini
# Run `alembic check` in CI to detect unmigrated model changes
# Run `alembic revision --autogenerate -m "description"` to generate
```

## Acceptance Criteria
- `alembic check` runs in CI pipeline
- CI fails if SQLAlchemy models have changes without migration
- PR that adds model fields without migration fails CI check
- Documented in README.md's "Development" section
