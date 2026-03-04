# TODO-518: spaCy Model Warm-up + Async Startup

**Repo:** core-entityextraction
**Priority:** P2
**Effort:** S (2h)
**Dependencies:** None
**Blocks:** None

## Description
Run a dummy spaCy prediction at startup to pre-JIT the model and prevent first-request latency spike. Also make entity store loading async.

## Coding Prompt
```
In /data/workspace/projects/core-entityextraction/main.py:

1. In startup_event(), after loading spaCy model:
   - Run nlp("warm up prediction for financial entities") to trigger JIT
   - Log startup time for model loading vs warm-up

2. Make entity store loading async:
   - Use asyncio.gather to load all entity types in parallel
   - Log total startup time

3. Add /health endpoint response field: {"startup_time_ms": X}
```

## Acceptance Criteria
- [ ] First request latency matches subsequent requests
- [ ] Startup loads entity types in parallel
- [ ] Health endpoint shows startup time
