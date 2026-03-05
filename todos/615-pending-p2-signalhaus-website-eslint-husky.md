# TODO-615: ESLint + Husky Pre-commit Hooks

**Repo:** signalhaus-website  
**Priority:** P2  
**Effort:** S (1-2 hours)  
**Status:** pending

## Description
No linting configured. Next.js ships with ESLint config but it's not enabled. Add ESLint + Husky for pre-commit quality gates.

## Tasks
1. Run `npx next lint --fix` to set up eslint-config-next
2. Add `.eslintrc.json` with next/core-web-vitals rules
3. Install Husky + lint-staged
4. Pre-commit hook: run ESLint on staged files
5. Add `npm run lint` to CI workflow

## Coding Prompt
```bash
npm install -D husky lint-staged
npx husky init
echo "npx lint-staged" > .husky/pre-commit
```

Add to `package.json`:
```json
{
  "scripts": {
    "lint": "next lint"
  },
  "lint-staged": {
    "*.{ts,tsx}": ["eslint --fix", "git add"]
  }
}
```

## Acceptance Criteria
- [ ] ESLint runs without errors on current codebase
- [ ] Pre-commit hook blocks commits with lint errors
- [ ] Lint step in CI workflow
- [ ] No TypeScript errors (`tsc --noEmit` clean)

## Dependencies
- TODO-611 (CI pipeline)
