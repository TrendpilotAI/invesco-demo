# 380 — NL→SQL Multi-Turn Conversation Memory

**Repo:** forwardlane-backend  
**Priority:** high (revenue/Invesco)  
**Effort:** M (3-5h)  
**Status:** pending

## Description
The NL→SQL endpoint (INVESCO-001) is single-turn. Invesco advisors naturally ask follow-up questions ("Now filter to equity only", "Sort by YTD"). Multi-turn dramatically increases stickiness and demo quality. Store conversation history in Redis, pass last N turns as context to Gemini/Kimi.

## Coding Prompt
```
In /data/workspace/projects/forwardlane-backend/easy_button/ (or analytical/):

1. Add session_id parameter to NLQueryView POST request
2. On each request, fetch conversation history from Redis:
   key = f"nl_sql_history:{session_id}"
   history = cache.get(key, [])
3. Append current question + generated SQL to history (max 5 turns)
4. Store updated history: cache.set(key, history, timeout=3600)
5. Pass history as context to Gemini prompt:
   "Previous questions and SQL: {history}\nNow answer: {current_question}"
6. Add session_id to response so frontend can thread conversations
7. Add unit tests for multi-turn context threading
8. Add endpoint: DELETE /nl-query/session/{session_id}/ to clear history
```

## Acceptance Criteria
- Two sequential NL questions in same session produce coherent follow-up SQL
- History expires after 1 hour of inactivity
- Session can be cleared explicitly
- Tests cover multi-turn context injection
