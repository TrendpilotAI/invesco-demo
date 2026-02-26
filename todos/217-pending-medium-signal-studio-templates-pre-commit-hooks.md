# 217 — Pre-commit Hooks: husky + lint-staged Setup

**Priority:** medium  
**Project:** signal-studio-templates  
**Repo:** /data/workspace/projects/signal-studio-templates/  
**Status:** pending  
**Estimated Effort:** 1h  

---

## Context

Without pre-commit hooks, developers can commit code that breaks the build, fails linting, or introduces type errors. `husky` + `lint-staged` enforce quality gates at commit time, catching issues before they reach CI.

---

## Task Description

1. Install husky and lint-staged:
   ```bash
   npm install --save-dev husky lint-staged
   npx husky install
   ```
2. Add `"prepare": "husky install"` to `package.json` scripts.
3. Create `.husky/pre-commit` hook that runs lint-staged.
4. Configure lint-staged in `package.json`:
   ```json
   "lint-staged": {
     "src/**/*.ts": [
       "eslint --fix",
       "prettier --write"
     ]
   }
   ```
5. Optionally add prettier:
   ```bash
   npm install --save-dev prettier
   ```
   Create `.prettierrc.js` with consistent formatting rules.
6. Test: make a change with a lint error, try to commit, verify the commit is blocked.

---

## Coding Prompt (Autonomous Agent)

```
You are adding pre-commit hooks to signal-studio-templates.

REPO: /data/workspace/projects/signal-studio-templates/

Steps:
1. Run: npm install --save-dev husky lint-staged prettier
2. Run: npx husky install
3. Add to package.json scripts: "prepare": "husky install"
4. Add to package.json:
   "lint-staged": {
     "src/**/*.ts": ["eslint --fix", "prettier --write"]
   }
5. Run: npx husky add .husky/pre-commit "npx lint-staged"
6. Create .prettierrc.js:
   module.exports = {
     semi: true,
     trailingComma: 'es5',
     singleQuote: true,
     printWidth: 100,
     tabWidth: 2,
   };
7. Create .prettierignore: dist/, node_modules/, coverage/
8. Test: introduce a deliberate lint error, try `git commit`, verify it's blocked
9. Fix the test error and verify commit succeeds
10. Report: hook installed, test result
```

---

## Dependencies

- **212** (ESLint must be configured first)

---

## Acceptance Criteria

- [ ] `.husky/pre-commit` hook exists and runs lint-staged
- [ ] `npm run prepare` installs husky hooks
- [ ] Committing a file with lint errors is blocked
- [ ] Committing clean files succeeds
- [ ] `.prettierrc.js` exists with consistent formatting rules
- [ ] `"prepare": "husky install"` in package.json scripts
