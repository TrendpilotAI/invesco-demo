---
id: 637
status: pending
priority: P1
repo: signal-studio-templates
title: Add ESLint config + GitHub Actions CI pipeline
effort: S (1 day)
dependencies: []
---

# ESLint Config + GitHub Actions CI/CD Pipeline

## Problem
- `package.json` scripts reference `eslint` but `.eslintrc` is MISSING → lint script fails
- No `.github/workflows/` → no CI/CD, no automated publish
- `dist/` is committed to git (should be gitignored)

## Task
Add ESLint config, Prettier config, GitHub Actions CI workflow, and publish workflow.

## Coding Prompt
```
In /data/workspace/projects/signal-studio-templates/:

1. Create .eslintrc.json:
{
  "extends": ["eslint:recommended", "@typescript-eslint/recommended"],
  "parser": "@typescript-eslint/parser",
  "plugins": ["@typescript-eslint"],
  "rules": {
    "@typescript-eslint/no-explicit-any": "warn",
    "@typescript-eslint/no-unused-vars": "error",
    "no-console": "warn"
  },
  "ignorePatterns": ["dist/", "node_modules/"]
}

2. Create .prettierrc.json:
{
  "semi": true,
  "singleQuote": false,
  "tabWidth": 2,
  "trailingComma": "es5",
  "printWidth": 100
}

3. Add devDependencies (pnpm add -D):
   @typescript-eslint/eslint-plugin @typescript-eslint/parser eslint prettier

4. Create .github/workflows/ci.yml:
   - Triggers: push to main, all PRs
   - Jobs: checkout, pnpm install --frozen-lockfile, typecheck, lint, test
   - Node 20, ubuntu-latest

5. Create .github/workflows/publish.yml:
   - Triggers: push to tags matching v*
   - Jobs: build + pnpm publish --no-git-checks
   - Uses NPM_TOKEN secret
   - Sets registry-url to https://npm.forwardlane.com

6. Add dist/ to .gitignore

7. Update package.json lint script to: "eslint . --ext .ts,.tsx --ignore-path .gitignore"
```

## Acceptance Criteria
- [ ] `pnpm lint` runs without "eslint config not found" error
- [ ] `.github/workflows/ci.yml` exists and would pass on clean codebase
- [ ] `.github/workflows/publish.yml` exists
- [ ] `dist/` in `.gitignore`
- [ ] No lint errors on existing codebase (or they are documented)
