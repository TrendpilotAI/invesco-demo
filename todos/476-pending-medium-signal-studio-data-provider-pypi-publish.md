---
id: "476"
status: pending
priority: medium
repo: signal-studio-data-provider
title: "Publish to PyPI via GitHub Actions OIDC Trusted Publisher"
effort: M
dependencies: []
created: "2026-03-04"
---

## Task Description

The package is at `v0.1.0` but not published to PyPI. Signal Studio deployments currently install from source. PyPI publication enables `pip install signal-studio-data-provider[snowflake]` and semantic versioning.

## Coding Prompt

1. Configure PyPI Trusted Publisher at https://pypi.org/manage/account/publishing/:
   - Repository: `signalhaus-ai/signal-studio-data-provider` (or wherever it lives)
   - Workflow: `publish.yml`
   - Environment: `pypi`

2. Create `.github/workflows/publish.yml`:
```yaml
name: Publish to PyPI

on:
  push:
    tags:
      - "v*"

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Install build
        run: pip install build
      - name: Build dist
        run: python -m build
      - uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/

  publish:
    needs: build
    runs-on: ubuntu-latest
    environment: pypi
    permissions:
      id-token: write  # OIDC
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: dist
          path: dist/
      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
```

3. Add `[build-system]` to `pyproject.toml` if missing:
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

4. Add version bump script or use `hatch version patch` in release workflow.

5. Tag first release: `git tag v0.1.0 && git push --tags`

## Acceptance Criteria
- [ ] `.github/workflows/publish.yml` created
- [ ] PyPI Trusted Publisher configured (manual step — document in README)
- [ ] `[build-system]` section in pyproject.toml
- [ ] Tag `v0.1.0` triggers publish
- [ ] Package installable via `pip install signal-studio-data-provider`
