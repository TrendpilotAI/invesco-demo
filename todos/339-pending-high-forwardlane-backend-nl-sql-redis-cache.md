# 339 — Redis Caching for NL→SQL Endpoint

**Priority:** HIGH
**Repo:** forwardlane-backend
**Effort:** S (1 hour)
**Category:** Performance

## Description
`NLQueryView.post()` in `easy_button/views.py` calls the Gemini/Kimi LLM API on every request
regardless of whether the same question was asked before. LLM calls add 1-5 seconds latency
and accrue API costs. Cache results by question hash.

## Implementation

Add to `NLQueryView.post()` before the LLM call:
```python
import hashlib
from django.core.cache import cache

def post(self, request, *args, **kwargs):
    question = request.data.get('question', '').strip()
    if not question:
        return Response({'error': 'question required'}, status=400)
    
    # Cache check
    cache_key = f"nl_sql:{hashlib.md5(question.lower().encode()).hexdigest()}"
    cached_sql = cache.get(cache_key)
    if cached_sql:
        logger.info("NL→SQL cache hit for question hash")
        return Response({'sql': cached_sql, 'cached': True, 'rows': self._execute(cached_sql)})
    
    # ... existing LLM call ...
    
    # Cache result (1 hour TTL)
    cache.set(cache_key, generated_sql, 3600)
    return Response({'sql': generated_sql, 'cached': False, 'rows': rows})
```

## Files to Change
- `easy_button/views.py` — `NLQueryView.post()` method
- `easy_button/tests/test_nl_query_cache.py` — add cache hit/miss tests

## Acceptance Criteria
- [ ] Same question asked twice only calls LLM API once
- [ ] `cached: true` field in response when from cache
- [ ] Cache TTL is 1 hour
- [ ] Cache key based on normalized (lowercased, stripped) question
- [ ] Test: mock LLM, verify second call returns from cache without calling LLM
