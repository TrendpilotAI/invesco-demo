Title: 306 — Signal Studio: E2E tests for Invesco flows + bundle optimization
Repo: signal-studio
Priority: P1 (High)
Owner: Frontend engineer
Estimated effort: 1-3 days

Description:
Add Playwright E2E tests covering Invesco demo flows and implement bundle size optimizations (code-splitting, lazy imports, skeleton loaders) for demo pages.

Acceptance criteria:
- Playwright tests run in CI and cover: demo login (if any), dashboard load, signal creation, Salesforce push simulation
- Lighthouse metrics for demo pages improved (target: 20% improvement or equivalent grade)
- Bundle size reduction steps documented and merged

Execution steps / Agent-executable prompt:
1. Add Playwright tests to repo and create GitHub Action to run them
2. Identify largest client-side bundles via webpack/next build analysis
3. Apply code-splitting and lazy-load heavy components (visual builder etc.)
4. Implement skeleton loaders for main pages
5. Run Lighthouse and document metrics before/after

Verification tests:
- Playwright tests pass in CI
- Lighthouse report attached to PR showing improvement

Notes:
- Keep changes backwards compatible; use feature flags if needed
