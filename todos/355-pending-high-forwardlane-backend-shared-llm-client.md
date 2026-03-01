# TODO 355: Extract Shared LLM Client Module

**Repo:** forwardlane-backend  
**Priority:** HIGH  
**Effort:** M (2-4 hours)  
**Dependencies:** None

## Description

The LLM API call patterns (Gemini → Kimi fallback) are duplicated in at least two places in `easy_button/views.py`:
1. `_call_gemini_brief()` / `_call_kimi_brief()` in `_llm_meeting_brief()`
2. `NLQueryView._call_gemini()` / `NLQueryView._call_kimi()`

Additionally, all LLM calls use stdlib `urllib` instead of the `requests` library (already installed) — no connection pooling, no retry support, worse error handling.

## Coding Prompt

```
You are working in /data/workspace/projects/forwardlane-backend/.

Task: Create a shared LLM client module and refactor easy_button views to use it.

1. Create file: easy_button/llm_client.py

Content should include:
  - `import requests` (already in Pipfile)
  - `class LLMClient` with methods:
    - `__init__(self)`: set up a requests.Session with timeout defaults
    - `call_gemini(self, prompt: str, *, max_tokens: int = 512, temperature: float = 0) -> str`
      Uses GEMINI_API_KEY and GEMINI_MODEL env vars
      Returns raw text response
      Raises LLMError on failure
    - `call_kimi(self, prompt: str, system: str = None, *, max_tokens: int = 512, temperature: float = 0) -> str`
      Uses KIMI_API_KEY and KIMI_BASE_URL env vars
      Returns raw text response
      Raises LLMError on failure
    - `call_with_fallback(self, prompt: str, system: str = None, **kwargs) -> tuple[str, str]`
      Tries Gemini first, falls back to Kimi
      Returns (response_text, model_used) where model_used is 'gemini' or 'kimi'
      Raises LLMError if both fail
  - `class LLMError(Exception): pass`
  - Module-level singleton: `llm_client = LLMClient()`

2. Update easy_button/views.py:
  - Remove all urllib imports from function bodies
  - Import: from easy_button.llm_client import llm_client, LLMError
  - Refactor `_llm_meeting_brief()` to use `llm_client.call_with_fallback()`
  - Refactor `NLQueryView._gemini_sql()` to use `llm_client.call_with_fallback()`
  - Remove duplicate `_call_gemini_brief`, `_call_kimi_brief`, `_call_gemini`, `_call_kimi` methods

3. Add retry logic in LLMClient using requests' built-in retry adapter:
  from requests.adapters import HTTPAdapter
  from urllib3.util.retry import Retry
  session.mount('https://', HTTPAdapter(max_retries=Retry(total=2, backoff_factor=0.5)))

4. Write unit tests in easy_button/tests/test_llm_client.py:
  - Test Gemini success path (mock requests)
  - Test Kimi fallback when Gemini fails
  - Test LLMError when both fail

Commit: "refactor: extract shared LLM client, use requests lib with retry"
```

## Acceptance Criteria
- [ ] `easy_button/llm_client.py` created with LLMClient class
- [ ] No duplicate LLM call code in views.py
- [ ] No urllib imports in function bodies
- [ ] Retry logic implemented
- [ ] Unit tests for LLM client
- [ ] All existing functionality preserved
