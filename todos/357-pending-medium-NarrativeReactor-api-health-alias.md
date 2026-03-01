# 357 · NarrativeReactor — Add /api/health Alias for Load Balancer Compatibility

**Priority:** medium  
**Effort:** S (< 1 day)  
**Repo:** /data/workspace/projects/NarrativeReactor/

---

## Task Description

The existing `/health` endpoint is unauthenticated and correct, but load balancers (Railway, AWS ALB, GCP) commonly expect `/api/health`. Add an alias route that returns the same response, and update the Railway healthcheck config.

---

## Coding Prompt (agent-executable)

```
In /data/workspace/projects/NarrativeReactor/src/:

1. Find where GET /health is registered (likely src/index.ts or src/routes/health.ts).

2. Add the alias immediately after:
   app.get('/api/health', healthHandler);   // same handler, no auth

   Or if the handler is inline:
   const healthHandler = (req, res) => res.json({ status: 'ok', ts: new Date().toISOString() });
   app.get('/health', healthHandler);
   app.get('/api/health', healthHandler);

3. Update railway.json (if present):
   { "healthcheckPath": "/api/health" }
   
   Or keep both in docs — some load balancers are configurable.

4. Add to Swagger/OpenAPI spec if one exists:
   /api/health:
     get:
       summary: Health check (load balancer alias)
       security: []
       responses:
         '200':
           description: Service is healthy

5. Verify: curl http://localhost:3000/api/health returns 200 with JSON body.

6. Add test in tests/integration/api.test.ts (or health.test.ts):
   it('GET /api/health returns 200', async () => {
     const res = await request(app).get('/api/health');
     expect(res.status).toBe(200);
     expect(res.body.status).toBe('ok');
   });
```

---

## Dependencies

- None (standalone route addition)

## Acceptance Criteria

- [ ] `GET /api/health` returns `200 { status: 'ok' }` without API key
- [ ] `GET /health` still works (not broken)
- [ ] railway.json or deployment config updated to use `/api/health`
- [ ] Test covers the alias endpoint
