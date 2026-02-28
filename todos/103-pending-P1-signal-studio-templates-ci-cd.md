# TODO 103 — Add CI/CD Pipeline (P1)

**Repo:** signal-studio-templates  
**Priority:** P1  
**Effort:** S (2 hours)  
**Status:** pending

---

## Autonomous Coding Prompt

```
Add CI/CD to /data/workspace/projects/signal-studio-templates/

1. Create bitbucket-pipelines.yml:
---
image: node:20-alpine

pipelines:
  default:
    - step:
        name: Install
        caches: [node]
        script:
          - npm install -g pnpm
          - pnpm install --frozen-lockfile
    - step:
        name: Typecheck
        script: pnpm typecheck
    - step:
        name: Test
        script: pnpm test:coverage
        artifacts: [coverage/**]
    - step:
        name: Build
        script: pnpm build
        artifacts: [dist/**]

2. Add pre-commit hook via package.json scripts:
   "scripts": {
     "pre-commit": "pnpm typecheck && pnpm test --passWithNoTests"
   }
   
   Create .husky/pre-commit or use simple package.json prepare + lint-staged.
   OR: just document the manual pre-commit command in README.

3. Add .eslintrc.json with TypeScript rules:
   {
     "extends": ["eslint:recommended"],
     "parser": "@typescript-eslint/parser",
     "rules": {
       "no-unused-vars": "error",
       "@typescript-eslint/no-explicit-any": "warn"
     }
   }
   Add @typescript-eslint/parser and @typescript-eslint/eslint-plugin to devDependencies.

4. Add "lint" to pipeline after typecheck step.
```

## Acceptance Criteria
- [ ] bitbucket-pipelines.yml created
- [ ] Pipeline runs typecheck, test, build in sequence
- [ ] ESLint config added
- [ ] README updated with CI status badge placeholder

## Dependencies
- TODO 102 (tests should exist before CI enforces them)
