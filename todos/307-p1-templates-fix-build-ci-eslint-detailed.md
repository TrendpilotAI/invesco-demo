Title: 307 — Signal Studio Templates: Fix build system + CI + ESLint
Repo: signal-studio-templates
Priority: P1 (High)
Owner: Frontend / Packaging engineer
Estimated effort: 6–12 hours

Description:
Fix npm build issues, add ESLint and pre-commit hooks, and add GitHub Actions CI that builds and runs tests for the template library.

Acceptance criteria:
- npm build produces artifacts successfully
- ESLint configured and enforced via pre-commit hooks
- CI pipeline builds and runs tests on PRs

Execution steps / Agent-executable prompt:
1. Inspect package.json build scripts; fix failing steps
2. Add ESLint config and Husky pre-commit hooks
3. Add GitHub Actions workflow to run builds and tests
4. Add integration test to ensure template parameterization safety

Verification tests:
- PR triggers GH Actions, build succeeds
- ESLint runs locally/pre-commit

Notes:
- Ensure templates parameterization prevents SQL injection by design
