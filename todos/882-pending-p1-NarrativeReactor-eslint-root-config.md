# TODO-882: Add ESLint Configuration to Project Root

**Repo**: NarrativeReactor  
**Priority**: P1 — Developer Experience  
**Effort**: 1 hour  
**Status**: Pending  

## Problem

ESLint is configured in `/dashboard` but not in the project root `src/`. TypeScript files have no linting, allowing type-unsafe patterns and code quality issues to slip through.

## Solution

```bash
cd /data/workspace/projects/NarrativeReactor
npm install -D eslint @typescript-eslint/eslint-plugin @typescript-eslint/parser eslint-plugin-import
```

Create `eslint.config.js` in project root:
```javascript
import tsPlugin from '@typescript-eslint/eslint-plugin';
import tsParser from '@typescript-eslint/parser';
import importPlugin from 'eslint-plugin-import';

export default [
  {
    ignores: ['dist/**', 'node_modules/**', 'coverage/**', 'dashboard/**', '**/*.js'],
  },
  {
    files: ['src/**/*.ts'],
    languageOptions: {
      parser: tsParser,
      parserOptions: {
        project: './tsconfig.json',
        tsconfigRootDir: '.',
      },
    },
    plugins: {
      '@typescript-eslint': tsPlugin,
      'import': importPlugin,
    },
    rules: {
      '@typescript-eslint/no-explicit-any': 'warn',
      '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
      '@typescript-eslint/explicit-function-return-type': 'off',
      'no-console': ['warn', { allow: ['warn', 'error'] }],
      'import/no-duplicates': 'error',
    },
  },
];
```

Add to `package.json` scripts:
```json
{
  "scripts": {
    "lint": "eslint src/",
    "lint:fix": "eslint src/ --fix"
  }
}
```

Update `.github/workflows/ci.yml` to include lint step:
```yaml
- name: Lint
  run: npm run lint
```

## Files to Change

- `package.json` — add devDeps + scripts
- `eslint.config.js` — new file
- `.github/workflows/ci.yml` — add lint step

## Acceptance Criteria

- [ ] `npm run lint` runs without crashing
- [ ] No-console rule warns on existing console.log calls (doesn't fail CI yet — warn mode)
- [ ] no-explicit-any warns on existing `any` types
- [ ] CI pipeline includes lint step
- [ ] Dashboard ESLint config unchanged
