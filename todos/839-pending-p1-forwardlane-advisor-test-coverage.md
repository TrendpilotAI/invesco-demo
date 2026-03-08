# TODO-839: Add Test Coverage >40% (forwardlane_advisor)

**Repo:** forwardlane_advisor  
**Priority:** P1  
**Effort:** Large (1 week)  
**Status:** pending

## Description
Current test coverage estimated <10%. A financial advisory platform needs robust testing. Add unit tests for core services: LLM gateway, portfolio recommendations, alert engine, auth.

## Coding Prompt
In `/data/workspace/projects/forwardlane_advisor/`:
1. Install coverage tooling: `npm install --save-dev nyc mocha`
2. Add to package.json scripts: `"test:coverage": "nyc --reporter=text --reporter=lcov mocha test/**/*.js"`
3. Write unit tests for:
   - `app/llm/gateway.js` — mock Anthropic/OpenAI calls, test fallback logic
   - `app/alerts/` — test alert rule evaluation, notification dispatch
   - `app/portfolios/` — test portfolio scoring, position calculation
   - Auth middleware — test passport local strategy, role-based access
4. Add `.nycrc` config targeting 40% coverage gate
5. Integrate coverage into `npm test`

## Acceptance Criteria
- `npm run test:coverage` runs without errors
- Coverage >40% across lines
- CI will fail if coverage drops below threshold

## Dependencies
- TODO-838 (remove dead code first, simplifies coverage baseline)
