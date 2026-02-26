# 212 — Add ESLint: Install eslint + @typescript-eslint, Create .eslintrc.js, Fix lint script

**Priority:** critical  
**Project:** signal-studio-templates  
**Repo:** /data/workspace/projects/signal-studio-templates/  
**Status:** pending  
**Estimated Effort:** 1.5h  

---

## Context

The signal-studio-templates repo has no ESLint configuration. Without linting, the codebase has no automated quality gate — type-unsafe patterns, unused imports, and style inconsistencies accumulate silently. This is especially risky given the SQL injection vulnerability already found in `generateSQL()`. ESLint with TypeScript-aware rules is a first-line defense.

---

## Task Description

1. Install ESLint and TypeScript ESLint plugins:
   ```bash
   npm install --save-dev eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin eslint-plugin-import
   ```
2. Create `.eslintrc.js` at repo root with:
   - Parser: `@typescript-eslint/parser`
   - Plugins: `@typescript-eslint`, `import`
   - Extends: `eslint:recommended`, `plugin:@typescript-eslint/recommended`
   - Rules: no-explicit-any (warn), no-unused-vars (error), @typescript-eslint/no-floating-promises (error)
3. Update `package.json` scripts:
   - `"lint": "eslint 'src/**/*.ts'"`
   - `"lint:fix": "eslint 'src/**/*.ts' --fix"`
4. Run `npm run lint` and fix all errors (auto-fix where possible, manual fix for the rest).
5. Ensure lint passes cleanly (exit code 0).

---

## Coding Prompt (Autonomous Agent)

```
You are adding ESLint to the signal-studio-templates TypeScript project.

REPO: /data/workspace/projects/signal-studio-templates/

Steps:
1. Run: npm install --save-dev eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin eslint-plugin-import
2. Create .eslintrc.js with this content:
   module.exports = {
     parser: '@typescript-eslint/parser',
     parserOptions: { project: './tsconfig.json', ecmaVersion: 2020, sourceType: 'module' },
     plugins: ['@typescript-eslint', 'import'],
     extends: ['eslint:recommended', 'plugin:@typescript-eslint/recommended'],
     rules: {
       '@typescript-eslint/no-explicit-any': 'warn',
       '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
       '@typescript-eslint/no-floating-promises': 'error',
       'import/no-duplicates': 'error',
     },
     ignorePatterns: ['dist/', 'node_modules/', '*.js'],
   };
3. Add to package.json scripts:
   "lint": "eslint 'src/**/*.ts'"
   "lint:fix": "eslint 'src/**/*.ts' --fix"
4. Run: npm run lint:fix
5. Run: npm run lint
6. Fix any remaining errors manually
7. Confirm lint exits 0
8. Report: number of issues auto-fixed, number manually fixed, final lint status
```

---

## Dependencies

- **211** (build system must be working first, tsconfig must be valid for parser)

---

## Acceptance Criteria

- [ ] `.eslintrc.js` exists at repo root
- [ ] `eslint`, `@typescript-eslint/parser`, `@typescript-eslint/eslint-plugin` in devDependencies
- [ ] `npm run lint` exits with code 0 (zero errors)
- [ ] `package.json` has `lint` and `lint:fix` scripts
- [ ] No `@typescript-eslint/no-explicit-any` violations (or all intentional ones are commented with justification)
