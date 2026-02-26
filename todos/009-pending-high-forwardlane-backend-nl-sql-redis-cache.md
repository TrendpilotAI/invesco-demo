# 009 — Add Redis Caching for NL→SQL Queries

**Repo:** forwardlane-backend  
**Priority:** high  
**Effort:** S (2-3h)  
**Status:** pending

## Description

`NLQueryView` in `easy_button/views.py` calls Gemini or Kimi K2.5 for every NL→SQL request. The same question (e.g. "show at-risk advisors") will call the LLM API repeatedly — wasting money and adding latency. Redis is already in the stack.

Cache strategy: hash(question.lower().strip()) → (sql_string, TTL=3600s). Cache both the SQL text and whether LLM was used.

## Coding Prompt

File: `/data/workspace/projects/forwardlane-backend/easy_button/views.py`

1. Add imports at the top:
```python
import hashlib
from django.core.cache import cache

_NL_QUERY_CACHE_TTL = int(os.environ.get('NL_QUERY_CACHE_TTL', 3600))  # 1 hour default
```

2. In `NLQueryView.post()`, after extracting `question`, add cache lookup before the pattern/LLM chain:
```python
cache_key = 'nl_sql:' + hashlib.md5(question.lower().strip().encode()).hexdigest()
cached = cache.get(cache_key)
if cached:
    sql = cached['sql']
    used_llm = False
    # proceed to execution step
```

3. After successful LLM SQL generation (before execution), store in cache:
```python
if used_llm and sql and sql.upper() != 'UNSUPPORTED':
    cache.set(cache_key, {'sql': sql}, timeout=_NL_QUERY_CACHE_TTL)
```

4. Add `'cache_hit': True/False` to the response JSON.

5. Add `NL_QUERY_CACHE_TTL` to `.env.example` with a comment.

6. Verify `CACHES` is configured in Railway settings to use Redis:
   ```python
   CACHES = {
       'default': {
           'BACKEND': 'django.core.cache.backends.redis.RedisCache',
           'LOCATION': os.environ.get('REDIS_URL', 'redis://localhost:6379/'),
       }
   }
   ```

## Dependencies
- None (but coordinate with 010 which also modifies NLQueryView)

## Acceptance Criteria
- [ ] Second identical NL query uses cache (used_llm=False, cache_hit=True)
- [ ] Cache TTL is configurable via env
- [ ] Cache invalidation works (restart resets cache gracefully)
- [ ] Unit test: mock LLM, send same question twice, assert LLM called only once
- [ ] Response includes `cache_hit` field
