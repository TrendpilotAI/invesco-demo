# TODO-465: N+1 Query Audit (pipeline_engine + ranking)

**Priority:** MEDIUM  
**Repo:** forwardlane-backend  
**Effort:** M (4-8 hours)  
**Dependencies:** None

## Description
`pipeline_engine/` and `ranking/` process large client datasets and likely have N+1 query problems. Use `django-debug-toolbar` and `nplusone` to detect and fix.

## Coding Prompt
```
In /data/workspace/projects/forwardlane-backend/:

1. Add to Pipfile [dev-packages]:
   django-debug-toolbar = "*"
   nplusone = "*"

2. Configure nplusone in test settings to raise on N+1:
   # forwardlane/settings/test.py
   NPLUSONE_RAISE = True
   NPLUSONE_LOGGER = logging.getLogger('nplusone')

3. Run existing tests with nplusone active — capture all N+1 warnings

4. For each N+1 found in pipeline_engine/ and ranking/:
   - Add select_related() or prefetch_related() to QuerySets
   - Document: file, line, fix applied

5. Add EXPLAIN ANALYZE investigation for these common query patterns:
   - Client list with portfolio data
   - Ranking computation per client
   - Document recommendations per advisor

6. Add DB indexes where missing:
   - Check all ForeignKey fields that are filtered on
   - Run: python manage.py inspectdb and compare to migration indexes

7. Write findings to /data/workspace/projects/forwardlane-backend/PERF_AUDIT.md

8. Commit: "perf: fix N+1 queries in pipeline_engine and ranking, add missing DB indexes"
```

## Acceptance Criteria
- [ ] nplusone passes in test suite (no N+1 in test paths)
- [ ] PERF_AUDIT.md documents findings
- [ ] At least 3 N+1 fixes applied
- [ ] New DB indexes added where warranted
