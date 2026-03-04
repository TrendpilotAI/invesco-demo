# TODO-471: Add ESLint + Prettier + Husky Pre-commit

**Priority:** P1 (High)
**Effort:** S (2 hours)
**Repo:** signalhaus-website
**Status:** pending

## Problem

No `.eslintrc.json`, no Prettier config, no pre-commit hooks. Code quality gates missing — as more agents/contributors touch the codebase, inconsistencies will accumulate.

## Agent Prompt

```
Set up ESLint + Prettier + Husky for /data/workspace/projects/signalhaus-website/

1. Install dev dependencies:
cd /data/workspace/projects/signalhaus-website
npm install --save-dev eslint @typescript-eslint/eslint-plugin @typescript-eslint/parser eslint-config-next prettier eslint-config-prettier lint-staged husky

2. Create .eslintrc.json:
{
  "extends": ["next/core-web-vitals", "prettier"],
  "rules": {
    "@typescript-eslint/no-unused-vars": ["warn", { "argsIgnorePattern": "^_" }],
    "no-console": ["warn", { "allow": ["error", "warn"] }]
  }
}

3. Create .prettierrc:
{
  "semi": false,
  "singleQuote": false,
  "trailingComma": "es5",
  "printWidth": 100,
  "tabWidth": 2
}

4. Add to package.json scripts:
"lint": "next lint",
"format": "prettier --write src/"

5. Add lint-staged config to package.json:
"lint-staged": {
  "*.{ts,tsx}": ["eslint --fix", "prettier --write"],
  "*.{json,md,css}": ["prettier --write"]
}

6. Initialize husky:
npx husky init
echo "npx lint-staged" > .husky/pre-commit

7. Run lint to verify: npm run lint
8. Fix any lint errors found
9. Run: npx tsc --noEmit
```

## Acceptance Criteria
- [ ] `npm run lint` passes with zero errors
- [ ] `.prettierrc` exists
- [ ] `.eslintrc.json` exists
- [ ] `husky` pre-commit hook installed
- [ ] `lint-staged` runs on commit
- [ ] TypeScript compiles without errors
