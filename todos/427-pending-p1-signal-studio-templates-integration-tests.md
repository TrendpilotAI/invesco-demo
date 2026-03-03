# TODO 427: Add Integration Tests — TemplateEngine + API Routes

**Repo:** signal-studio-templates  
**Priority:** P1 (High)  
**Effort:** M (1–2 days)  
**Status:** pending

## Description

Current test suite only validates template schema. The TemplateEngine `execute()` path and all API routes have zero test coverage. Before Invesco demos or production deploy, we need tests that exercise the full execution cycle.

## Acceptance Criteria

- [ ] `__tests__/engine.test.ts` — tests `TemplateEngine.execute()` with MockDataProvider for all 20 templates
- [ ] `__tests__/api.test.ts` — tests all API routes with supertest
- [ ] Parameter validation edge cases covered (missing required params, out-of-range values)
- [ ] Error paths tested (template not found, data source unavailable)
- [ ] Coverage report shows >80% for `engine/` and `api/`

## Coding Prompt

```
In /data/workspace/projects/signal-studio-templates/__tests__/:

### 1. Create MockDataProvider (shared fixture)
// __tests__/fixtures/mock-data-provider.ts
export class MockDataProvider implements DataProvider {
  private rows: Record<string, any>[] = [];
  
  constructor(rows: Record<string, any>[] = []) {
    this.rows = rows;
  }
  
  async executeSQL(sql: string, params?: unknown[]): Promise<Record<string, any>[]> {
    // Return fixture rows, record calls for assertion
    this.lastSql = sql;
    this.lastParams = params;
    return this.rows;
  }
  
  async availableDataSources(): Promise<DataSource[]> {
    return ['crm', 'holdings', 'transactions', 'interactions', 'market-data', 
            'compliance', 'demographics', 'pipeline', 'activity-log', 
            'product-catalog', 'benchmarks'];
  }
  
  lastSql?: string;
  lastParams?: unknown[];
}

### 2. engine.test.ts
import { TemplateEngine } from '../engine/template-engine';
import { ALL_TEMPLATES } from '../templates';
import { MockDataProvider } from './fixtures/mock-data-provider';

describe('TemplateEngine', () => {
  it('executes all 20 templates without throwing', async () => {
    const provider = new MockDataProvider([{ id: 1, name: 'Test Advisor' }]);
    const engine = new TemplateEngine(provider);
    
    for (const template of ALL_TEMPLATES) {
      const defaults = Object.fromEntries(
        template.parameters
          .filter(p => p.default !== undefined)
          .map(p => [p.name, p.default])
      );
      const result = await engine.execute(template.id, defaults);
      expect(result.templateId).toBe(template.id);
      expect(Array.isArray(result.rows)).toBe(true);
    }
  });
  
  it('throws on missing required parameters', async () => {
    const engine = new TemplateEngine(new MockDataProvider());
    await expect(engine.execute('dormant-relationships', {}))
      .rejects.toThrow();
  });
  
  it('throws on unknown template id', async () => {
    const engine = new TemplateEngine(new MockDataProvider());
    await expect(engine.execute('nonexistent-template', {}))
      .rejects.toThrow('Template not found');
  });
});

### 3. api.test.ts
Install: pnpm add -D supertest @types/supertest

import request from 'supertest';
import express from 'express';
import { createTemplateRouter } from '../api/templates';
import { MockDataProvider } from './fixtures/mock-data-provider';

const app = express();
app.use(express.json());
app.use('/', createTemplateRouter(new MockDataProvider([{ advisor: 'Test' }])));

describe('Template API', () => {
  it('GET /templates returns 20 templates', async () => {
    const res = await request(app).get('/templates').expect(200);
    expect(res.body.count).toBe(20);
    expect(res.body.templates).toHaveLength(20);
  });
  
  it('GET /templates?category=meeting-prep returns 4 templates', async () => {
    const res = await request(app).get('/templates?category=meeting-prep').expect(200);
    expect(res.body.count).toBe(4);
  });
  
  it('GET /templates/:id returns full template', async () => {
    const res = await request(app).get('/templates/dormant-relationships').expect(200);
    expect(res.body.id).toBe('dormant-relationships');
    expect(res.body.sqlTemplate).toBeTruthy();
  });
  
  it('GET /templates/nonexistent returns 404', async () => {
    await request(app).get('/templates/does-not-exist').expect(404);
  });
  
  it('POST /templates/:id/execute runs template', async () => {
    const res = await request(app)
      .post('/templates/dormant-relationships/execute')
      .send({ dormant_days: 45, min_aum: 5000000 })
      .expect(200);
    expect(res.body.rows).toBeDefined();
  });
});
```

## Dependencies

- TODO 426 (auth) should be done first OR implement AUTH_DISABLED=true for tests

## Notes

Run with: `pnpm test --coverage`
