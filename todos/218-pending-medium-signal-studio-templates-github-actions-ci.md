# 218 — GitHub Actions CI: Typecheck + Test + Lint on Push

**Priority:** medium  
**Project:** signal-studio-templates  
**Repo:** /data/workspace/projects/signal-studio-templates/  
**Status:** pending  
**Estimated Effort:** 1.5h  

---

## Context

There is no CI pipeline for signal-studio-templates. Without automated checks on every push/PR, regressions go undetected. A GitHub Actions workflow running typecheck + tests + lint on push provides a continuous quality gate and prevents broken code from reaching the main branch.

---

## Task Description

1. Create `.github/workflows/ci.yml`:
   ```yaml
   name: CI
   on:
     push:
       branches: [main, develop]
     pull_request:
       branches: [main, develop]
   jobs:
     ci:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - uses: actions/setup-node@v4
           with:
             node-version: '20'
             cache: 'npm'
         - run: npm ci
         - run: npm run typecheck   # tsc --noEmit
         - run: npm run lint
         - run: npm test -- --coverage
         - run: npm run build
   ```
2. Add `"typecheck": "tsc --noEmit"` script to `package.json`.
3. Optionally: upload coverage to Codecov.
4. Add a CI status badge to `README.md`.

---

## Coding Prompt (Autonomous Agent)

```
You are adding GitHub Actions CI to signal-studio-templates.

REPO: /data/workspace/projects/signal-studio-templates/

Steps:
1. Add "typecheck": "tsc --noEmit" to package.json scripts
2. Create .github/workflows/ci.yml with:
   name: CI
   on:
     push:
       branches: [main, develop]
     pull_request:
       branches: [main, develop]
   jobs:
     ci:
       runs-on: ubuntu-latest
       strategy:
         matrix:
           node-version: ['18', '20']
       steps:
         - uses: actions/checkout@v4
         - uses: actions/setup-node@v4
           with:
             node-version: ${{ matrix.node-version }}
             cache: 'npm'
         - name: Install dependencies
           run: npm ci
         - name: TypeScript typecheck
           run: npm run typecheck
         - name: Lint
           run: npm run lint
         - name: Test
           run: npm test -- --coverage --passWithNoTests
         - name: Build
           run: npm run build
3. Validate the YAML syntax (no tabs, correct indentation)
4. Update README.md to add CI badge:
   [![CI](https://github.com/forwardlane/signal-studio-templates/actions/workflows/ci.yml/badge.svg)](...)
5. Run typecheck locally: npm run typecheck (fix any errors)
6. Report: workflow file created, typecheck result, any issues found
```

---

## Dependencies

- **211** (build must work)
- **212** (lint must work)
- **214** (tests must exist)

---

## Acceptance Criteria

- [ ] `.github/workflows/ci.yml` exists with correct YAML syntax
- [ ] Workflow runs: typecheck → lint → test → build in sequence
- [ ] `"typecheck": "tsc --noEmit"` script in package.json
- [ ] CI badge added to README.md
- [ ] Workflow tests on Node 18 + 20 matrix
- [ ] All steps pass when run locally with `act` or equivalent
