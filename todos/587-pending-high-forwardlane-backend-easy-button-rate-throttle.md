# TODO-587: Add Rate Throttling to easy_button LLM Endpoints

**Priority:** HIGH  
**Repo:** forwardlane-backend  
**Effort:** S (1h)  
**Status:** pending  

## Description

`EasyButtonPermission` provides HMAC token auth but no rate throttling. Heavy LLM calls (Gemini/Kimi APIs) can be spammed, causing high API costs and potential DoS.

## Task

1. Create `EasyButtonRateThrottle` in `easy_button/views.py`:
   ```python
   from rest_framework.throttling import SimpleRateThrottle
   
   class EasyButtonRateThrottle(SimpleRateThrottle):
       scope = "easy_button"
       
       def get_cache_key(self, request, view):
           # Rate limit by HMAC token identity or IP
           return f"throttle_easy_button_{request.META.get('REMOTE_ADDR', 'unknown')}"
   ```

2. Add to `REST_FRAMEWORK` settings:
   ```python
   "DEFAULT_THROTTLE_RATES": {
       "easy_button": "30/minute",  # 30 LLM calls per minute max
   }
   ```

3. Apply to LLM-heavy views: `NLQueryView`, `MeetingPrepView`, `TalkingPointsView`:
   ```python
   throttle_classes = [EasyButtonRateThrottle]
   ```

4. Add test in `easy_button/tests/` to verify 429 response after rate limit exceeded

## Acceptance Criteria

- [ ] LLM endpoints return 429 after 30 requests/minute from same IP
- [ ] Non-LLM easy_button endpoints are unaffected
- [ ] Test demonstrates throttle behavior
