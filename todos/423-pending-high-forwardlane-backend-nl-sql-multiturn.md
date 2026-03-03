# TODO-423: NL→SQL Multi-Turn Conversation Memory

**Repo:** forwardlane-backend  
**Priority:** HIGH  
**Effort:** M (1-2 days)  
**Depends on:** Redis (already configured)

## Problem
Current NL→SQL (`/api/v1/easy-button/nl-query/`) is single-turn. Invesco advisors naturally ask follow-up questions: "Now filter to just equity funds", "Sort by YTD performance". Without session memory, each question is stateless, producing a poor demo experience.

## Task
Add Redis-backed conversation thread support to the NL→SQL endpoint. Each session gets a `thread_id`; last N (3-5) question+SQL pairs are passed as context to Gemini.

## Coding Prompt
```python
# In NLQueryView.post():
import uuid

thread_id = request.data.get('thread_id') or str(uuid.uuid4())
history_key = f"nl_sql_history:{thread_id}"
history = cache.get(history_key, [])

# Build context string from history
context = "\n".join([f"Q: {h['q']}\nSQL: {h['sql']}" for h in history[-3:]])
full_prompt = f"{context}\nQ: {question}\nSQL:" if context else f"Q: {question}\nSQL:"

# After successful query:
history.append({"q": question, "sql": generated_sql})
cache.set(history_key, history[-5:], timeout=3600)  # 1hr session

# Return thread_id in response for client to track
return Response({..., "thread_id": thread_id})
```

## Acceptance Criteria
- [ ] `thread_id` returned in response when not provided
- [ ] Follow-up questions use prior context (test: "now sort by AUM" after advisor query)
- [ ] Thread expires after 1 hour of inactivity
- [ ] Unit test: mock Redis, verify history stored and passed to LLM
- [ ] Load test: 10 concurrent threads don't collide
