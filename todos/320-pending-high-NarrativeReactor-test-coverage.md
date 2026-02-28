# 320 · NarrativeReactor — Test Coverage Expansion

**Status:** pending  
**Priority:** high  
**Project:** NarrativeReactor  
**Effort:** ~8h  

---

## Task Description

NarrativeReactor has Vitest configured but limited test coverage. Critical services like brandVoice, campaigns, costTracker, and contentPipeline have no unit tests. API routes have no integration tests. This task brings coverage to ≥70% on lines/branches for the core service layer.

## Full Coding Prompt

```
You are working in /data/workspace/projects/NarrativeReactor/.

## Step 0 — Baseline
Run `pnpm test --coverage` and capture current coverage. Note which files are at 0%.

## Step 1 — Unit tests for core services
Create tests for each of the following (use vi.mock for external API calls):

### tests/services/brandVoice.test.ts
- analyzeBrandVoice() returns structured tone/style object
- getBrandVoiceProfile() throws if brand not found
- Mock LLM calls with vi.mock

### tests/services/campaigns.test.ts
- createCampaign() saves and returns campaign with ID
- getCampaignById() returns null for unknown ID
- Campaign status transitions: draft → active → paused → completed
- Edge cases: empty name, missing brandId

### tests/services/costTracker.test.ts
- trackCost() accumulates costs correctly
- getCostSummary() returns totals by service
- Budget alerts fire when threshold exceeded
- Reset costs clears accumulator

### tests/services/contentPipeline.test.ts
- Pipeline runs steps in order
- Pipeline halts on step failure and returns error
- Retry logic retries up to configured max
- Mock all external service calls

### tests/services/blotatoPublisher.test.ts
- publishPost() calls Blotato API with correct payload
- Handles Blotato API errors gracefully
- Returns published post ID on success

### tests/services/competitorTracker.test.ts
- trackCompetitor() stores competitor data
- getCompetitorInsights() returns ranked insights
- Deduplicates competitor URLs

## Step 2 — Route integration tests
Create tests/api/routes.test.ts using supertest:

```typescript
import request from 'supertest';
import app from '../../src/index'; // ensure app is exported

// Auth
describe('API Auth', () => {
  it('rejects requests without X-API-Key', async () => {
    const res = await request(app).get('/api/content');
    expect(res.status).toBe(401);
  });
  it('accepts requests with valid X-API-Key', async () => {
    const res = await request(app)
      .get('/api/content')
      .set('X-API-Key', process.env.API_KEY!);
    expect(res.status).not.toBe(401);
  });
});

// Health
describe('Health', () => {
  it('GET /health returns ok', async () => {
    const res = await request(app).get('/health');
    expect(res.body.status).toBe('ok');
  });
});
```

## Step 3 — Configure coverage thresholds
Update vitest.config.ts:
```typescript
coverage: {
  provider: 'v8',
  thresholds: {
    lines: 70,
    branches: 65,
    functions: 70,
    statements: 70,
  },
  exclude: ['node_modules', 'dist', 'tests', '**/*.config.*', 'src/lib/env.ts'],
}
```

## Step 4 — Export app from src/index.ts
Make the Express app testable:
```typescript
export { app }; // add at bottom of src/index.ts
// Keep: if (require.main === module) { app.listen(...) }
```

## Step 5 — CI test script
Add to package.json:
```json
"test:ci": "vitest run --coverage --reporter=junit --outputFile=test-results.xml"
```
```

## Dependencies
- 317 (health endpoint needed for route tests)

## Acceptance Criteria
- [ ] `pnpm test --coverage` shows ≥70% line coverage overall
- [ ] All 7 service test files exist with ≥5 test cases each
- [ ] Route integration tests pass (auth, health, at least 5 API routes)
- [ ] Coverage thresholds enforced — CI fails below threshold
- [ ] `app` is exported from `src/index.ts` for testability
- [ ] No tests call real external APIs (all mocked)
