# TODO-570: Add Unit Tests for Core Business Logic — forwardlane_advisor

**Repo:** forwardlane_advisor  
**Priority:** P0  
**Status:** pending

## Description
Test coverage is near zero. Add unit tests for all core business logic modules.

## Test Suites to Create
- `test/unit/portfolios/` — portfolio calculation functions
- `test/unit/alerts/` — alert evaluation and rule matching
- `test/unit/hdialog/` — dialog state machine (post-LLM migration)
- `test/unit/instruments/` — instrument utility functions
- `test/integration/routes/` — all REST API endpoints (chai-http)

## Coding Prompt for Agent
```
Add comprehensive unit tests to /data/workspace/projects/forwardlane_advisor/.
Use existing Mocha + Chai setup (already in package.json).
1. Create test/unit/portfolios/portfolio.test.js - test portfolio calculations
2. Create test/unit/alerts/alert_evaluator.test.js - test alert rule evaluation
3. Create test/integration/routes/api.test.js - test key API endpoints with chai-http
Use sequelize-mock to mock DB calls. Target 70% coverage on business logic.
Run: npm test to verify all pass.
```

## Acceptance Criteria
- `npm test` passes with >70% coverage on business logic
- All route tests cover happy path + error cases
- Tests run in CI (GitHub Actions)

## Dependencies
TODO-568 (Sequelize v6) for integration tests
