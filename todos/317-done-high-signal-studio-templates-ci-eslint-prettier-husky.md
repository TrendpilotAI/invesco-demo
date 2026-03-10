# 317 — CI Pipeline + ESLint + Prettier + Husky

**Priority:** HIGH  
**Effort:** S  
**Status:** pending

---

## Task Description

The repo has no CI pipeline, no linter config, and no pre-commit hooks. This means broken code can be merged, SQL injection fixes can be reverted accidentally, and type errors ship silently. Set up the full developer quality baseline: ESLint, Prettier, Husky pre-commit, and a Bitbucket Pipelines CI config.

---

## Autonomous Coding Prompt

```
REPO: /data/workspace/projects/signal-studio-templates

TASK: Add ESLint, Prettier, Husky pre-commit hooks, and Bitbucket CI pipeline.

STEPS:

1. ESLint setup:
   pnpm add -D eslint @typescript-eslint/eslint-plugin @typescript-eslint/parser \
     eslint-plugin-import eslint-plugin-jest

   Create .eslintrc.json:
   {
     "root": true,
     "parser": "@typescript-eslint/parser",
     "plugins": ["@typescript-eslint", "import", "jest"],
     "extends": [
       "eslint:recommended",
       "plugin:@typescript-eslint/recommended",
       "plugin:jest/recommended"
     ],
     "rules": {
       "@typescript-eslint/no-explicit-any": "error",
       "@typescript-eslint/no-unused-vars": "error",
       "no-console": "warn",
       "import/no-duplicates": "error"
     },
     "env": { "node": true, "jest": true }
   }

   Add to package.json scripts:
   "lint": "eslint src --ext .ts",
   "lint:fix": "eslint src --ext .ts --fix"

2. Prettier setup:
   pnpm add -D prettier

   Create .prettierrc:
   {
     "semi": true,
     "singleQuote": true,
     "trailingComma": "all",
     "printWidth": 100,
     "tabWidth": 2
   }

   Create .prettierignore: node_modules, dist, coverage

   Add to package.json scripts:
   "format": "prettier --write 'src/**/*.ts'",
   "format:check": "prettier --check 'src/**/*.ts'"

3. .editorconfig:
   root = true
   [*]
   indent_style = space
   indent_size = 2
   end_of_line = lf
   charset = utf-8
   trim_trailing_whitespace = true
   insert_final_newline = true

4. Husky + lint-staged:
   pnpm add -D husky lint-staged
   npx husky init

   .husky/pre-commit:
   #!/bin/sh
   npx lint-staged

   .husky/pre-push:
   #!/bin/sh
   pnpm typecheck && pnpm test --passWithNoTests

   package.json lint-staged config:
   "lint-staged": {
     "src/**/*.ts": ["eslint --fix", "prettier --write"]
   }

5. Bitbucket Pipelines:
   Create bitbucket-pipelines.yml at repo root:

   image: node:20

   pipelines:
     default:
       - step:
           name: Install
           caches: [node]
           script:
             - npm i -g pnpm
             - pnpm install --frozen-lockfile
       - step:
           name: Type Check
           script:
             - pnpm typecheck
       - step:
           name: Lint
           script:
             - pnpm lint
       - step:
           name: Test
           script:
             - pnpm test --coverage
       - step:
           name: Build
           script:
             - pnpm build
     tags:
       'v*':
         - step:
             name: Publish
             script:
               - npm i -g pnpm
               - pnpm install --frozen-lockfile
               - pnpm build
               - echo "//registry.npmjs.org/:_authToken=${NPM_TOKEN}" > ~/.npmrc
               - pnpm publish --no-git-checks

6. Run lint on existing code and fix all violations:
   pnpm lint:fix
   pnpm format

7. Update README.md to document: lint, format, test, build scripts.

ACCEPTANCE: pnpm lint, pnpm format:check, pnpm typecheck all pass with zero errors.
Husky hooks installed. bitbucket-pipelines.yml present and valid.
```

---

## Dependencies

- None (can run in parallel with 315, 316)

---

## Acceptance Criteria

- [ ] `.eslintrc.json` present, `pnpm lint` passes with zero errors
- [ ] `.prettierrc` present, `pnpm format:check` passes
- [ ] Husky pre-commit runs lint-staged; pre-push runs typecheck + tests
- [ ] `bitbucket-pipelines.yml` present with install → typecheck → lint → test → build steps
- [ ] Tag pipeline publishes to npm registry
- [ ] All existing source files pass lint (violations fixed)
