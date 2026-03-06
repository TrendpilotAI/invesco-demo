# TODO-588: Integration Tests for Gemini→Kimi LLM Fallback Chain

**Priority:** HIGH  
**Repo:** forwardlane-backend  
**Effort:** M (4h)  
**Status:** pending  

## Description

Unit tests exist for the LLM client but no integration tests verify:
1. Gemini succeeds → Kimi is NOT called
2. Gemini fails (network error) → Kimi is called automatically
3. Both fail → proper error raised with meaningful message
4. Retry backoff works correctly (3 retries before fallback)
5. Streaming fallback works (SSE stream switches provider mid-stream? Or at start only?)

## Task

Create `easy_button/tests/test_llm_integration.py`:

```python
class TestLLMFallbackChain(TestCase):
    def test_gemini_success_no_kimi_call(self):
        """When Gemini succeeds, Kimi should never be called."""
        ...
    
    def test_gemini_500_falls_back_to_kimi(self):
        """When Gemini returns 500, should retry then fall back to Kimi."""
        ...
    
    def test_gemini_timeout_falls_back_to_kimi(self):
        """When Gemini times out, should fall back to Kimi."""
        ...
    
    def test_both_fail_raises_service_unavailable(self):
        """When both Gemini and Kimi fail, should raise appropriate error."""
        ...
    
    def test_streaming_fallback(self):
        """SSE streaming falls back correctly when Gemini stream fails."""
        ...
    
    def test_retry_count_before_fallback(self):
        """Should retry Gemini exactly N times before falling back."""
        ...
```

Use `unittest.mock.patch` and `responses` library for HTTP mocking.

## Acceptance Criteria

- [ ] All 6 test scenarios pass
- [ ] Tests are deterministic (no real API calls)
- [ ] Fallback behavior verified at integration level, not just unit level
- [ ] Tests added to `tox.ini` test suite

## Dependencies

- Best done after: TODO-586 (LLMClient class makes testing easier)
