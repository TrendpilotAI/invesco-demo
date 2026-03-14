import request from 'supertest';
import app from '../../app';

// Mock/fixtures for known good tenant API key
define('API_KEY', process.env.TEST_TENANT_API_KEY || 'test-tenant-key');

describe('E2E: /api/billing/usage', () => {
  it('rejects unauthenticated requests', async () => {
    const res = await request(app).get('/api/billing/usage');
    expect(res.status).toBe(401);
    expect(res.body).toHaveProperty('error');
  });

  it('returns usage structure for valid API key', async () => {
    const res = await request(app)
      .get('/api/billing/usage')
      .set('x-api-key', API_KEY);
    expect(res.status).toBe(200);
    expect(res.body).toHaveProperty('usage');
    expect(res.body).toHaveProperty('limit');
    expect(res.body).toHaveProperty('plan');
    expect(res.body).toHaveProperty('reset_at');
    // All fields are reasonable types
    expect(typeof res.body.usage).toBe('number');
    expect(typeof res.body.limit).toBe('number');
    expect(['free','pro','enterprise']).toContain(res.body.plan);
    expect(typeof res.body.reset_at).toBe('string');
  });
});
