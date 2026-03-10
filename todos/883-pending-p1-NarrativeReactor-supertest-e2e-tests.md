# TODO-883: Add True Supertest HTTP Integration Tests

**Repo**: NarrativeReactor  
**Priority**: P1 — Test Quality  
**Effort**: 2 days  
**Status**: Pending  

## Problem

`src/__tests__/e2e/integration.test.ts` (391 lines) uses `vi.mock` to mock the entire Express stack — it's actually a unit test, NOT a true HTTP integration test. We need tests that spin up the real Express app and verify actual HTTP responses.

## Solution

Install `supertest`:
```bash
npm install -D supertest @types/supertest
```

Create `src/__tests__/e2e/http.test.ts`:

```typescript
import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import request from 'supertest';
import { app } from '../../index';  // Export app from index.ts

const ADMIN_KEY = 'test-admin-key';
let testTenantKey: string;

beforeAll(async () => {
  process.env.API_KEY = ADMIN_KEY;
  process.env.NODE_ENV = 'test';
  // Create a test tenant
  const res = await request(app)
    .post('/api/tenants')
    .set('X-API-Key', ADMIN_KEY)
    .send({ name: 'Test Tenant', email: 'test@example.com' });
  testTenantKey = res.body.api_key;
});

describe('Health', () => {
  it('GET /health returns 200', async () => {
    const res = await request(app).get('/health');
    expect(res.status).toBe(200);
    expect(res.body.status).toBe('ok');
  });
});

describe('Auth', () => {
  it('GET /api/content returns 401 without API key', async () => {
    const res = await request(app).get('/api/content');
    expect(res.status).toBe(401);
  });

  it('GET /api/content returns 200 with valid admin key', async () => {
    const res = await request(app)
      .get('/api/content')
      .set('X-API-Key', ADMIN_KEY);
    expect(res.status).toBe(200);
  });
});

describe('Billing Plans', () => {
  it('GET /api/billing/plans returns plan list', async () => {
    const res = await request(app).get('/api/billing/plans');
    expect(res.status).toBe(200);
    expect(res.body.plans).toHaveLength(4); // free, starter, pro, enterprise
  });
});

describe('Rate Limiting', () => {
  it('enforces 100 req/15min limit', async () => {
    const requests = Array.from({ length: 101 }, () =>
      request(app).get('/api/content').set('X-API-Key', ADMIN_KEY)
    );
    const results = await Promise.all(requests);
    const tooMany = results.filter(r => r.status === 429);
    expect(tooMany.length).toBeGreaterThan(0);
  });
});

describe('Quota Enforcement', () => {
  it('returns 429 when tenant quota exceeded', async () => {
    // Create tenant with 0 token quota
    const adminRes = await request(app)
      .post('/api/tenants')
      .set('X-API-Key', ADMIN_KEY)
      .send({ name: 'Zero Quota Tenant', quota_override: 0 });
    
    const res = await request(app)
      .post('/api/pipeline/generate')
      .set('X-API-Key', adminRes.body.api_key)
      .send({ prompt: 'test' });
    
    expect(res.status).toBe(429);
    expect(res.body.code).toBe('QUOTA_EXCEEDED');
  });
});
```

## Files to Change

- `package.json` — add `supertest` and `@types/supertest` to devDependencies
- `src/index.ts` — export `app` (in addition to starting server): `export { app }`
- `src/__tests__/e2e/http.test.ts` — new file with true HTTP tests
- `vitest.config.ts` — ensure test database path uses in-memory or temp path for E2E

## Dependencies

- TODO-880 (DB singleton fix) should be done first for clean test DB isolation

## Acceptance Criteria

- [ ] `npm test` runs supertest E2E tests against real Express app
- [ ] Tests do NOT use vi.mock for Express/route handlers
- [ ] Health endpoint test passes
- [ ] Auth (401 without key) test passes
- [ ] Rate limiting (429 on 101st request) test passes
- [ ] Quota enforcement (429 when 0 tokens) test passes
- [ ] Billing plans list test passes
- [ ] Tests use isolated test SQLite DB (not production data)
