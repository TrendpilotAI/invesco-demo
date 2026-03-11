# TODO-830 ✅ DONE — GitHub Actions CI Pipeline (signal-studio-auth)

## Summary
Added CI pipeline and tooling config to `TrendpilotAI/signal-studio-auth`.

## Files Created

### `.github/workflows/ci.yml`
Four parallel jobs triggered on push/PR to `main`/`master`:

| Job | Tool | Command |
|-----|------|---------|
| Lint | ruff | `ruff check .` |
| Type check | mypy | `mypy .` |
| Test | pytest | `pytest --cov=. --cov-report=xml` |
| Security | bandit + pip-audit | `bandit -r . -x ./tests,./migrations` + `pip-audit -r requirements.txt` |

- Test job spins up a Redis service container
- Coverage uploaded to Codecov (non-blocking)
- All jobs use `python:3.11` + `actions/cache` for pip deps

### `pyproject.toml`
- **ruff**: line-length 100, selects E/W/F/I/B/C4/UP, ignores E501 + B008 (FastAPI DI)
- **mypy**: `strict=false`, `ignore_missing_imports=true`, `disallow_untyped_defs=true`
- **pytest**: `asyncio_mode=auto`, `testpaths=["tests"]`
- **coverage**: omits tests/, migrations/, .venv/

## Branch / PR
`feat/cors-docker-ci` → https://github.com/TrendpilotAI/signal-studio-auth/pull/new/feat/cors-docker-ci

## Completed
2026-03-11
