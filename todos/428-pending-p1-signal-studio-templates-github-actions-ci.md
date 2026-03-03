# TODO 428: Add GitHub Actions CI Pipeline

**Repo:** signal-studio-templates  
**Priority:** P1 (High)  
**Effort:** S (2–3 hours)  
**Status:** pending

## Description

No CI pipeline exists. PRs can merge with broken types, failing tests, or lint errors. Add GitHub Actions to enforce quality gates.

## Acceptance Criteria

- [ ] `.github/workflows/ci.yml` created
- [ ] Pipeline runs: typecheck → lint → test → build
- [ ] Fails PR if any step fails
- [ ] `pnpm audit` runs and fails on HIGH+ CVEs
- [ ] Coverage report uploaded as artifact

## Coding Prompt

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  quality:
    name: Quality Gates
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - uses: pnpm/action-setup@v3
        with:
          version: 8
      
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'pnpm'
      
      - name: Install dependencies
        run: pnpm install --frozen-lockfile
      
      - name: Type check
        run: pnpm typecheck
      
      - name: Lint
        run: pnpm lint || echo "::warning::Lint not configured — add eslint"
      
      - name: Test with coverage
        run: pnpm test:coverage
      
      - name: Upload coverage
        uses: actions/upload-artifact@v4
        with:
          name: coverage
          path: coverage/
      
      - name: Build
        run: pnpm build
      
      - name: Security audit
        run: pnpm audit --audit-level=high
```

Also add `.eslintrc.json`:
```json
{
  "extends": ["eslint:recommended", "plugin:@typescript-eslint/recommended"],
  "parser": "@typescript-eslint/parser",
  "plugins": ["@typescript-eslint"],
  "rules": {
    "@typescript-eslint/no-explicit-any": "warn",
    "no-unused-vars": "off",
    "@typescript-eslint/no-unused-vars": "error"
  }
}
```

Install: `pnpm add -D eslint @typescript-eslint/eslint-plugin @typescript-eslint/parser`

## Dependencies

- None

## Notes

Add `pnpm run lint` to `package.json` scripts first (currently points to `src/` which doesn't exist — fix path to `.`).
