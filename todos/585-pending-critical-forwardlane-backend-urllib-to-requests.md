# TODO-585: Migrate easy_button urllib.request → requests.Session

**Priority:** CRITICAL  
**Repo:** forwardlane-backend  
**Effort:** M (3h)  
**Status:** pending  

## Description

`easy_button/views.py` uses `urllib.request.urlopen` for all LLM HTTP calls (Gemini and Kimi APIs). This provides no connection pooling, poor timeout control, no retry adapter, and harder error handling. The `requests` library is already in Pipfile.

## Problem

```python
# Current: urllib.request (no pooling, no retry)
req = urllib.request.Request(url, data=body, headers=headers, method="POST")
with urllib.request.urlopen(req, timeout=30) as resp:
    raw = resp.read()
```

33 urllib usages detected across the codebase.

## Task

1. Replace all `urllib.request.urlopen` calls in `easy_button/views.py` and related LLM code with `requests.Session()` with retry adapter:
   ```python
   from requests.adapters import HTTPAdapter, Retry
   session = requests.Session()
   retries = Retry(total=3, backoff_factor=0.3, status_forcelist=[500,502,503])
   session.mount("https://", HTTPAdapter(max_retries=retries))
   ```
2. Update `easy_button/tests/test_llm_client.py` — change mocks from `@patch("urllib.request.urlopen")` to `@patch("requests.Session.post")`
3. Ensure timeout is still enforced (`timeout=30` kwarg on `.post()` call)
4. Remove `import urllib.request` from views.py once migration complete

## Acceptance Criteria

- [ ] No `urllib.request.urlopen` calls remain in easy_button/
- [ ] All existing LLM tests pass with updated mocks
- [ ] Manual test: NL→SQL query returns correct result
- [ ] Manual test: MeetingPrep SSE streams correctly

## Dependencies

- Completes before: TODO-586 (llm.py extraction, easier to extract clean requests-based code)
