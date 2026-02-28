# TODO 102 — Add TemplateEngine Integration Tests (P1)

**Repo:** signal-studio-templates  
**Priority:** P1  
**Effort:** M (1 day)  
**Status:** pending

---

## Autonomous Coding Prompt

```
Add comprehensive engine tests to /data/workspace/projects/signal-studio-templates/__tests__/engine.test.ts

Create a MockDataProvider:
  class MockDataProvider implements DataProvider {
    rows: Record<string, any>[] = [];
    lastSQL = '';
    lastParams: unknown[] = [];
    
    async executeSQL(sql: string, params?: unknown[]) {
      this.lastSQL = sql; this.lastParams = params ?? []; return this.rows;
    }
    async availableDataSources() { return ['crm','holdings','interactions','market-data','compliance','demographics','pipeline','activity-log','product-catalog','benchmarks','transactions'] as DataSource[]; }
  }

TEST CASES:

1. getTemplates() - no filter returns 20 templates
2. getTemplates({ category: 'meeting-prep' }) - returns 4
3. getTemplates({ search: 'dormant' }) - returns dormant-relationships
4. getTemplate('nonexistent') - returns undefined
5. validateParameters() - required field missing returns error
6. validateParameters() - number below min returns error  
7. validateParameters() - defaults applied correctly
8. validateDataSources() - all available returns valid=true
9. validateDataSources() - mock returns subset, missing sources returned
10. generateSQL('dormant-relationships', { dormant_days: 60, min_aum: 1000000 })
    - sql should NOT contain literal '$1' inside quotes
    - params array should contain 1000000 and 60
11. execute('dormant-relationships', { dormant_days: 60, min_aum: 1000000 })
    - mock returns 2 rows, result.rowCount === 2
    - result.sql is a string
    - result.executionTimeMs >= 0
12. execute('nonexistent') - throws "Template not found"
13. execute with missing required param - throws "Validation failed"
14. customize('dormant-relationships', { name: 'My Custom' })
    - returns template with id starting with 'custom-'
    - name is 'My Custom'
    - tags includes 'custom'

Run: pnpm test --coverage
Target: >80% coverage on engine/template-engine.ts
```

## Acceptance Criteria
- [ ] All 14 test cases implemented and passing
- [ ] engine/template-engine.ts coverage > 80%
- [ ] `pnpm test` passes

## Dependencies
- TODO 100 (SQL fix must be in place for generateSQL tests to pass)
