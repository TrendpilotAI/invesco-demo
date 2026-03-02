# TODO-401: NarrativeReactor — E2E Integration Tests

**Priority:** high
**Repo:** NarrativeReactor
**Effort:** M (2-3 days)

## Description
274 unit tests exist but no E2E tests for critical HTTP flows. Add Supertest-based E2E tests.

## Coding Prompt
```
Add E2E tests to /data/workspace/projects/NarrativeReactor/src/__tests__/e2e/

Use Supertest to test full HTTP flow (Express → Service → SQLite → Response).

Required test suites:
1. content-generation.e2e.ts — POST /api/generate returns content
2. campaign-flow.e2e.ts — Create campaign → advance stages → complete
3. brand-compliance.e2e.ts — Create brand → generate content → compliance check
4. social-publish.e2e.ts — Generate content → approve → publish (mock Blotato)
5. auth.e2e.ts — Missing API key returns 401, invalid returns 403

Setup:
- Use in-memory SQLite for test isolation
- Mock external APIs (Fal.ai, Fish Audio, Blotato, Gemini) with nock or msw
- Add X-API-Key: test-key header to all requests

Add to vitest.config.ts: include e2e directory in test run.
```

## Acceptance Criteria
- [ ] 5 E2E test suites passing
- [ ] Tests run in <30 seconds (mocked externals)
- [ ] No real API calls in test suite
- [ ] Coverage increases to >90%

## Dependencies
None
