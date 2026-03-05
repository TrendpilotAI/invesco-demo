# TODO-577: Expand Test Coverage from <6% to 60%+

**Repo:** signal-builder-frontend  
**Priority:** P1 🔥  
**Effort:** M (3-5 days)  
**Status:** pending

## Task Description
Signal builder frontend has 271 TS/TSX files but only 7 test files (<6% coverage). This is a critical risk for a production application with enterprise clients. Expand coverage to 60%+ starting with highest-risk modules.

## Acceptance Criteria
- [ ] Redux slices (auth, builder) reach 80%+ coverage
- [ ] All API service functions tested with MSW mocks
- [ ] All Zod schemas tested with valid and invalid inputs
- [ ] React Hook Form submission flows tested
- [ ] ReactFlow canvas node operations tested (add, delete, connect)
- [ ] Jest coverage report shows ≥60% overall coverage
- [ ] CI pipeline runs tests and fails on coverage drop

## Coding Prompt (Agent-Executable)
```
Navigate to /data/workspace/projects/signal-builder-frontend/

1. Audit existing tests:
   - Read src/redux/auth/slice.test.ts
   - Read src/redux/builder/slice.test.ts
   - Note patterns used

2. Write tests for missing Redux slices:
   - Find all slice files: find src/redux -name "slice.ts"
   - For each slice, create slice.test.ts following existing pattern
   - Test initial state, all reducers, selectors

3. Write MSW API tests:
   - Read src/shared/lib/getAxiosInstance.ts
   - Find all API call functions: grep -r "axios\." src/ --include="*.ts" -l
   - Create __tests__/ folder in src/shared/lib/
   - Write tests using MSW handlers for each API endpoint

4. Write Zod schema tests:
   - Find all zod schemas: grep -r "z.object\|z.string\|z.number" src/ --include="*.ts" -l
   - For each schema, test valid inputs pass and invalid inputs throw

5. Update jest config to collect coverage:
   - Add "collectCoverage": true to package.json jest config
   - Add "coverageThreshold": {"global": {"lines": 60}}

6. Run: yarn test --coverage and fix failures
```

## Dependencies
- TODO-232 (CI pipeline with typecheck+tests) — do this after tests pass locally

## Notes
- MSW v2 is already installed (msw: 2 in package.json)
- React Testing Library already installed
- @testing-library/user-event v14 available
