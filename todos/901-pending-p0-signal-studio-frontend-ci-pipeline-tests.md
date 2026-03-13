# TODO: Add CI Pipeline with Tests, Coverage Gates, and Dependency Audit

## Priority: P0
## Repo: signal-studio-frontend

### Problem
CI pipeline does not run tests or enforce coverage or security audits. No automated quality gates exist.

### Action Items
- Add GitHub Actions / Bitbucket pipeline with: `npm run test --coverage`, `npm run typecheck`, `npm audit --audit-level=high`
- Set coverage threshold at 70% (Jest/Vitest config)
- Add pre-commit hooks via husky + lint-staged
- Enforce TypeScript strict mode in tsconfig.json
- Block merges on failing checks

### Impact
- Prevents regressions from reaching production
- Surfaces security vulnerabilities in deps early
- Forces developers to maintain test coverage

### References
- AUDIT.md CI section
- Existing test config files
