# 354 · NarrativeReactor — GitHub Actions CI Pipeline

**Priority:** high  
**Effort:** S (< 1 day)  
**Repo:** /data/workspace/projects/NarrativeReactor/

---

## Task Description

Set up a GitHub Actions CI pipeline that runs on every push and pull request to `main`. The pipeline must enforce type-checking, linting, tests with coverage, and a successful build before merge is allowed.

---

## Coding Prompt (agent-executable)

```
In /data/workspace/projects/NarrativeReactor/, create .github/workflows/ci.yml with:

name: CI
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

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
      - run: npx tsc --noEmit           # type-check
      - run: npm run lint               # ESLint (must exist)
      - run: npm test -- --coverage     # vitest with coverage thresholds
      - run: npm run build              # tsc compile

Also verify package.json has:
  "scripts": {
    "lint": "eslint src --ext .ts",
    "build": "tsc",
    "test": "vitest run"
  }

If lint script is missing, add it. If ESLint is not installed, add:
  npm install -D @typescript-eslint/eslint-plugin @typescript-eslint/parser eslint

Create .eslintrc.json:
{
  "parser": "@typescript-eslint/parser",
  "plugins": ["@typescript-eslint"],
  "extends": ["eslint:recommended", "plugin:@typescript-eslint/recommended"],
  "rules": { "@typescript-eslint/no-explicit-any": "warn" }
}

Run: npm run lint && npm test -- --run to verify locally.
```

---

## Dependencies

- ESLint must be installed (may not be — see BRAINSTORM.md §5)
- `vitest` already present (tests exist)
- Repo must be on GitHub

## Acceptance Criteria

- [ ] `.github/workflows/ci.yml` exists and is valid YAML
- [ ] `npm run lint` exits 0
- [ ] `npm test -- --run` exits 0
- [ ] `npm run build` exits 0
- [ ] CI passes on a clean checkout (no local state)
