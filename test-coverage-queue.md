# Test Coverage Push — Target 80% Across All Repos

## Priority Order (by current gap)
1. invesco-demo — 7 test files / 96 source → nearly 0% coverage
2. signal-builder-backend — 90 test files / 534 source → ~30-40% estimated
3. forwardlane-backend — 291 test files / 2532 source → ~40-50% estimated
4. signal-studio-backend — 285 test files / 2548 source → ~40-50% estimated
5. signal-studio — needs coverage report to assess
6. NarrativeReactor — 287 existing tests, needs gap analysis
7. signal-studio-auth — needs comprehensive test suite
8. signal-studio-data-provider — has some tests, needs expansion
9. signal-studio-templates — needs template engine tests
10. signal-studio-frontend — component tests needed
11. signal-builder-frontend — component tests needed
12. core-entityextraction — already at 100% (done in overnight)
13. Ultrafone — needs E2E + unit tests
14. Second-Opinion — needs component + integration tests
15. Trendpilot — has 16 auth tests, needs more
16. forwardlane_advisor — has 63 tests, needs more
17. flip-my-era — 507 test files (probably good)
18. signalhaus-website — needs tests

## Agent Template
Each agent gets ONE repo, runs coverage, identifies gaps, writes tests until 80%+.
Command: `pytest --cov=. --cov-report=term-missing` (Python) or `npx vitest --coverage` / `npx jest --coverage` (JS/TS)
