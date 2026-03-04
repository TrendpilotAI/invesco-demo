# TODO-463: Daily Briefing Aggregate Endpoint

**Priority:** MEDIUM  
**Repo:** forwardlane-backend  
**Effort:** L (1-2 days)  
**Dependencies:** TODO-458 (shared LLM client)

## Description
Build a "Daily Briefing" endpoint that aggregates portfolio signals, upcoming meetings, and AI-generated talking points for advisors. High demo value for enterprise prospects (Invesco-style).

## Coding Prompt
```
In /data/workspace/projects/forwardlane-backend/api/v1/:

1. Create views/daily_briefing.py:
   - GET /api/v1/daily-briefing/
   - Authenticated: requires JWT
   - Aggregates for the requesting advisor:
     a. Today's meetings (from calendar/meeting data)
     b. Top 5 clients with portfolio changes > 5% this week
     c. New content recommendations (from content_ingestion)
     d. AI-generated "focus of the day" from LLM client
   - Cache result per user for 30 minutes (Redis)
   - Returns structured JSON: { meetings: [...], alerts: [...], recommendations: [...], ai_summary: "..." }

2. Wire to urls.py

3. Add Celery task: pre-generate daily briefings at 7AM ET for all active users
   - Task: briefing_engine/tasks.py::generate_daily_briefings
   - Schedule in django-celery-beat

4. Add tests:
   - Test endpoint returns correct structure
   - Test cache hit behavior
   - Test Celery task creates briefings

5. Commit: "feat: daily briefing aggregate endpoint with LLM summary + Celery pre-generation"
```

## Acceptance Criteria
- [ ] Endpoint returns aggregated data in < 500ms (from cache)
- [ ] Celery task pre-generates at 7AM ET
- [ ] LLM summary included
- [ ] Auth enforced
