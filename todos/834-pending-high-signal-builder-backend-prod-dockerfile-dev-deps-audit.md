# TODO-834: Verify Dev Packages Excluded from Production Docker Image

**Repo:** signal-builder-backend  
**Priority:** HIGH  
**Effort:** S (2-4 hours)  
**Status:** pending

## Problem

`Dockerfile.railway` may be installing dev dependencies (`ipython`, `ipdb`, `bandit`, `pytest`) into the production image. This:
1. Bloats the image size
2. Increases attack surface (ipython has known CVEs in older versions)
3. Exposes debug tooling in production

## Audit Steps

1. Check `Dockerfile.railway` for `pipenv install` vs `pipenv install --deploy --without dev`
2. Check if `ipython==8.16.1` (with known CVEs) ends up in production image
3. Verify Railway deploy process uses the correct Dockerfile

## Fix

```dockerfile
# Dockerfile.railway — production install:
RUN pipenv install --system --deploy --without dev
# --system: install to system Python (not virtualenv)
# --deploy: fail if Pipfile.lock is out of date
# --without dev: exclude [dev-packages] section
```

Also add `.dockerignore`:
```
.ipython/
__pycache__/
*.pyc
.pytest_cache/
.mypy_cache/
.ruff_cache/
tests/
*.test.py
```

## Coding Prompt

```bash
# 1. Check current Dockerfile.railway:
cat Dockerfile.railway

# 2. If it uses pipenv install without --without dev, fix it

# 3. Build locally and verify:
docker build -f Dockerfile.railway -t signal-builder-test .
docker run --rm signal-builder-test pip list | grep -E "ipython|bandit|pytest|ipdb"
# Should return nothing (dev packages not installed)

# 4. Add .dockerignore if not present
```

## Acceptance Criteria
- `docker build` with `Dockerfile.railway` produces image without ipython, pytest, bandit, ipdb
- Production image size reduced (dev deps are ~50MB)
- `.dockerignore` excludes test files, cache dirs, and `.ipython/`
- CI build step verifies production image doesn't contain dev packages
