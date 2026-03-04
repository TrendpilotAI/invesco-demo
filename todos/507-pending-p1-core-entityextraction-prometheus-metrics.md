# TODO-507: Add Prometheus Metrics

**Repo:** core-entityextraction
**Priority:** P1
**Effort:** S (2-3h)
**Dependencies:** None
**Blocks:** None

## Description
Add production observability with Prometheus metrics endpoint.

## Coding Prompt
```
In /data/workspace/projects/core-entityextraction/:

1. Add prometheus-fastapi-instrumentator to requirements.txt
2. In main.py:
   from prometheus_fastapi_instrumentator import Instrumentator
   Instrumentator().instrument(app).expose(app)
3. Add custom metrics:
   - entity_extraction_duration_seconds (histogram, by endpoint type)
   - entity_store_size (gauge, count of entities in store)
   - extraction_entities_found (histogram, entities per request)
4. /metrics endpoint should NOT require API key auth
```

## Acceptance Criteria
- [ ] /metrics returns Prometheus format
- [ ] Request count, latency p50/p95/p99 tracked per endpoint
- [ ] Custom business metrics exposed
- [ ] /metrics accessible without API key
