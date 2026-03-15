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

  it('returns 400 for malformed POST request (missing fields)', async () => {
    const res = await request(app)
      .post('/api/content')
      .set('X-API-Key', validApiKey)
      .send({ bogus: 'data' });

    expect([400, 404, 405]).toContain(res.status);
    expect(res.body).toHaveProperty('error');
  });

  it('returns 401 for POST with missing API key', async () => {
    const res = await request(app)
      .post('/api/content')
      .send({ title: 'Test Title', body: 'Hello world' });
    expect(res.status).toBe(401);
    expect(res.body).toHaveProperty('error');
  });

  it('returns 200 for valid POST (create content)', async () => {
    const newContent = { title: 'New Test Title', body: 'Automated test content', type: 'article' };
    const res = await request(app)
      .post('/api/content')
      .set('X-API-Key', validApiKey)
      .send(newContent);
    expect([200, 201]).toContain(res.status);
    expect(typeof res.body).toBe('object');
    expect(res.body).toHaveProperty('title', 'New Test Title');
  });

  it('returns 405 for unsupported HTTP methods (PUT/DELETE)', async () => {
    const putRes = await request(app)
      .put('/api/content')
      .set('X-API-Key', validApiKey);
    expect([404, 405]).toContain(putRes.status);

    const deleteRes = await request(app)
      .delete('/api/content')
      .set('X-API-Key', validApiKey);
    expect([404, 405]).toContain(deleteRes.status);
  });
});
