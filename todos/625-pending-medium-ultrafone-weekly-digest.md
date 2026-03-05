# TODO 625 — Weekly Intelligence Digest via Telegram

**Repo:** Ultrafone  
**Priority:** MEDIUM  
**Effort:** 1 day  
**Depends on:** 623 (Telegram notifications)

## Task
Send Nathan a weekly summary of call patterns every Monday morning.

## Execution Prompt
```python
# backend/services/digest_service.py

async def generate_weekly_digest(user_id: str) -> str:
    # Query call_records for last 7 days
    # Aggregate: total calls, by category, spam blocked, leads forwarded
    # Use Groq to write natural language summary
    # Format: "This week: 23 calls screened. 8 ForwardLane leads (3 forwarded to you), 
    #          12 spam blocked (saving ~40 min), 3 healthcare messages taken."
    pass

# Add to cron: every Monday 9 AM ET
# POST to /api/digest/weekly or use Railway cron job
```

## Acceptance Criteria
- [ ] Accurate weekly stats from Supabase query
- [ ] AI-generated natural language summary (not just numbers)
- [ ] Sent via Telegram on Monday 9 AM ET
- [ ] Includes top spam tactics detected that week
