# TODO-586: Extract easy_button/llm.py LLM Client Module

**Priority:** CRITICAL  
**Repo:** forwardlane-backend  
**Effort:** M (3h)  
**Status:** pending  
**Depends on:** TODO-585

## Description

LLM client code (`_llm_meeting_brief`, `_gemini_sql`, `_call_gemini`, `_call_kimi`, retry logic) is embedded inside `easy_button/views.py` (67k lines). This violates SRP, makes testing hard, and blocks reuse across apps.

## Task

Create `easy_button/llm.py` with:

```python
class LLMClient:
    def generate(self, prompt: str, system: str | None = None) -> str:
        """Single-shot text generation. Tries Gemini, falls back to Kimi."""
        ...
    
    def stream(self, prompt: str) -> Iterator[str]:
        """Streaming text generation for SSE endpoints."""
        ...
    
    def _call_gemini(self, prompt: str, system: str | None) -> str: ...
    def _call_kimi(self, prompt: str, system: str | None) -> str: ...
```

1. Move all LLM logic from `views.py` into `easy_button/llm.py`
2. Instantiate `llm_client = LLMClient()` (module-level singleton)
3. Wire `NLQueryView._gemini_sql()` → `llm_client.generate(prompt)`
4. Wire `MeetingPrepView._sse_generator()` → `llm_client.stream(prompt)`
5. Wire `_llm_meeting_brief()` → `llm_client.generate(prompt)`
6. Update `test_llm_client.py` to test `LLMClient` directly
7. Add type hints throughout

## Acceptance Criteria

- [ ] `easy_button/llm.py` exists with `LLMClient` class
- [ ] `views.py` has no inline LLM HTTP logic
- [ ] All existing LLM tests pass
- [ ] `LLMClient` can be imported and used independently
- [ ] Streaming works end-to-end for MeetingPrep SSE

## Dependencies

- Requires: TODO-585 (requests.Session migration)
