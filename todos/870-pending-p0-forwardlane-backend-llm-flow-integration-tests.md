# FL-016: LLM Flow Integration Tests

**Repo:** forwardlane-backend  
**Priority:** P0  
**Effort:** M (2-3 days)  
**Status:** pending

## Task Description
Write integration tests for LLM flows: mock Gemini and Kimi API responses, test SSE streaming endpoint, test Gemini→Kimi fallback chain, and test observability data capture. Currently these flows are untested — a critical gap given Invesco actively uses them.

## Problem
The LLM meeting prep and recommendation flows are core product features with zero integration test coverage. If Gemini response format changes, or the fallback chain breaks, we won't know until Invesco reports an issue. The SSE streaming endpoint is particularly hard to test and likely has no test coverage at all.

## Coding Prompt
```
In /data/workspace/projects/forwardlane-backend/:

1. Create ai/tests/test_llm_flows.py:

   a) Test Gemini happy path:
   ```python
   @patch('libs.llm_client.LLMClient._call_gemini')
   def test_gemini_success_captures_observability(mock_gemini, api_client, tenant_user):
       mock_gemini.return_value = {
           'text': 'Meeting summary here',
           'usage': {'prompt_token_count': 100, 'candidates_token_count': 50}
       }
       response = api_client.post('/api/v1/meeting-prep/', {...}, format='json')
       assert response.status_code == 200
       # Verify observability record created
       obs = LLMObservabilityLog.objects.last()
       assert obs.latency_ms > 0
       assert obs.prompt_chars > 0
       assert obs.provider == 'gemini'
   ```

   b) Test Gemini→Kimi fallback:
   ```python
   @patch('libs.llm_client.LLMClient._call_gemini')
   @patch('libs.llm_client.LLMClient._call_kimi')
   def test_kimi_fallback_on_gemini_failure(mock_kimi, mock_gemini, api_client, tenant_user):
       mock_gemini.side_effect = Exception('Gemini 503')
       mock_kimi.return_value = {'text': 'Kimi response', 'usage': {...}}
       response = api_client.post('/api/v1/meeting-prep/', {...}, format='json')
       assert response.status_code == 200
       assert mock_kimi.called
       obs = LLMObservabilityLog.objects.last()
       assert obs.provider == 'kimi'
   ```

   c) Test SSE streaming:
   ```python
   def test_sse_streaming_response(api_client, tenant_user):
       with patch('libs.llm_client.LLMClient._call_gemini_stream') as mock_stream:
           mock_stream.return_value = iter(['chunk1', ' chunk2', ' done'])
           response = api_client.get('/api/v1/meeting-prep/stream/', HTTP_ACCEPT='text/event-stream')
           assert response.status_code == 200
           assert response['Content-Type'] == 'text/event-stream'
           # Collect SSE events
           content = b''.join(response.streaming_content)
           assert b'chunk1' in content
           assert b'done' in content
   ```

   d) Test rate limiting on LLM endpoints:
   ```python
   def test_llm_endpoint_rate_limited(api_client, tenant_user):
       for _ in range(20):  # exceed throttle limit
           api_client.post('/api/v1/meeting-prep/', {...})
       response = api_client.post('/api/v1/meeting-prep/', {...})
       assert response.status_code == 429
   ```

2. Create factories/llm_factories.py (if not exists):
   - LLMObservabilityLogFactory using factory_boy
   - TenantFactory (if not in core factories)

3. Add pytest fixture for LLM mocking in conftest.py:
   ```python
   @pytest.fixture
   def mock_gemini_response():
       return {
           'text': 'Test LLM response for meeting prep',
           'usage': {'prompt_token_count': 100, 'candidates_token_count': 75}
       }
   ```

4. Ensure all tests use @pytest.mark.django_db decorator

Files to create/modify:
- ai/tests/test_llm_flows.py (new — primary file)
- conftest.py (update — add LLM fixtures)
- ai/tests/factories.py (new or update)
```

## Acceptance Criteria
- [ ] Gemini happy path test passes with mocked response
- [ ] Gemini→Kimi fallback test verifies Kimi is called on Gemini failure
- [ ] SSE streaming endpoint has test that validates `text/event-stream` content type
- [ ] Rate limiting test verifies 429 after threshold
- [ ] Observability data (latency_ms, provider, tokens) verified in tests
- [ ] All tests pass in CI (tox + pytest)

## Dependencies
- FL-010 (LLM cost fields) — add cost fields to test assertions if done first, but not required.
