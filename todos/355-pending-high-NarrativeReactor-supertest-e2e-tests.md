# 355 · NarrativeReactor — Supertest E2E Tests for Express App

**Priority:** high  
**Effort:** M (1–3 days)  
**Repo:** /data/workspace/projects/NarrativeReactor/

---

## Task Description

Add `supertest`-based integration/E2E tests that exercise the full Express app — middleware stack, auth, routing, error handling — without mocking the server layer. Cover at least the 10 highest-value endpoints.

---

## Coding Prompt (agent-executable)

```
In /data/workspace/projects/NarrativeReactor/:

1. Install supertest:
   npm install -D supertest @types/supertest

2. Create tests/integration/api.test.ts:

import request from 'supertest';
import { app } from '../../src/index';   // adjust path if needed

const API_KEY = process.env.API_KEY || 'test-key';
const AUTH = { 'X-API-Key': API_KEY };

describe('Health endpoints', () => {
  it('GET /health returns 200', async () => {
    const res = await request(app).get('/health');
    expect(res.status).toBe(200);
    expect(res.body).toMatchObject({ status: 'ok' });
  });
  it('GET /api/health returns 200 (alias)', async () => {
    const res = await request(app).get('/api/health');
    expect(res.status).toBe(200);
  });
});

describe('Auth middleware', () => {
  it('rejects requests without API key with 401', async () => {
    const res = await request(app).get('/api/content');
    expect(res.status).toBe(401);
  });
  it('accepts valid API key', async () => {
    const res = await request(app).get('/api/content').set(AUTH);
    expect([200, 404]).toContain(res.status);  // 404 ok if no content yet
  });
});

describe('POST /api/pipeline/generate', () => {
  it('returns 400 on missing body', async () => {
    const res = await request(app).post('/api/pipeline/generate').set(AUTH).send({});
    expect([400, 422]).toContain(res.status);
  });
});

describe('Dashboard auth', () => {
  it('GET /dashboard redirects to /login when not authenticated', async () => {
    const res = await request(app).get('/dashboard');
    expect([302, 401]).toContain(res.status);
  });
  it('POST /login with wrong password returns 401', async () => {
    const res = await request(app).post('/login').send({ password: 'wrong' });
    expect(res.status).toBe(401);
  });
});

// Add 5+ more endpoint tests covering: brands, campaigns, webhooks, error shapes

3. Add test environment variables to vitest.config.ts:
   test: { env: { API_KEY: 'test-key', NODE_ENV: 'test' } }

4. Run: npm test -- --run tests/integration/api.test.ts

Fix any import issues (e.g., app not exported — export it from src/index.ts).
```

---

## Dependencies

- #354 (CI pipeline) — tests run in CI
- Express app must export `app` (not just `listen`)

## Acceptance Criteria

- [ ] `supertest` installed
- [ ] `tests/integration/api.test.ts` exists with ≥ 15 test cases
- [ ] All integration tests pass
- [ ] Auth middleware tested (401 without key, 200 with key)
- [ ] Error shape consistency tested
- [ ] Tests run in CI pipeline
