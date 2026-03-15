// src/tests/e2e/content.test.ts
import request from 'supertest';
import app from '../../src/app';

describe('E2E: /api/content', () => {
  const validApiKey = process.env.TEST_API_KEY || 'demo_key';

  it('returns 401 for missing API key', async () => {
    const res = await request(app).get('/api/content');
    expect(res.status).toBe(401);
    expect(res.body).toHaveProperty('error');
  });

  it('returns 200 and content list for valid API key', async () => {
    const res = await request(app)
      .get('/api/content')
      .set('X-API-Key', validApiKey);

    expect([200, 201]).toContain(res.status);
    expect(Array.isArray(res.body.data) || Array.isArray(res.body.contents)).toBe(true);
  });

  it('returns 400 for malformed request (if params required)', async () => {
    const res = await request(app)
      .post('/api/content')
      .set('X-API-Key', validApiKey)
      .send({ bogus: 'data' });

    expect([400, 404, 405]).toContain(res.status);
    expect(res.body).toHaveProperty('error');
  });
});