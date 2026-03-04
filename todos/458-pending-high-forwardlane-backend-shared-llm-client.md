# TODO-458: Extract Shared LLM Client Module

**Priority:** HIGH  
**Repo:** forwardlane-backend  
**Effort:** S (2-4 hours)  
**Dependencies:** None

## Description
Gemini and Kimi LLM client code is duplicated across `MeetingPrepView` and `NLQueryView`. Extract to a shared `ai/llm_client.py` with unified retry/fallback logic. Makes adding future LLM providers (GPT-4o, Claude) trivial.

## Coding Prompt
```
In /data/workspace/projects/forwardlane-backend/ai/:

1. Create ai/llm_client.py with:
   - LLMClient class with providers: ["gemini", "kimi", "openai"]
   - Method: complete(prompt, model_preference=None) -> str
   - Fallback chain: try providers in order, catch exceptions, try next
   - Redis caching decorator (cache key = hash of prompt + model)
   - Structured logging on each attempt/failure
   - Configurable via env vars: LLM_PRIMARY_PROVIDER, LLM_FALLBACK_PROVIDERS

2. Refactor MeetingPrepView to use LLMClient
3. Refactor NLQueryView to use LLMClient
4. Add unit tests in ai/tests/test_llm_client.py:
   - Test fallback chain when primary fails
   - Test cache hit/miss
   - Mock all external API calls

5. Commit: "refactor: extract shared LLM client with fallback chain and caching"
```

## Acceptance Criteria
- [ ] Single LLM client module used by all views
- [ ] Fallback chain tested with mocks
- [ ] Cache integration tested
- [ ] No duplicate LLM call code in views
