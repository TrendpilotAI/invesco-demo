# TODO 421: Smart Call Summaries via Slack

**Repo:** Ultrafone  
**Priority:** High  
**Effort:** M (1-2 days)  
**Dependencies:** None

## Description
Post AI-generated call summaries to a Slack channel after each call ends. This is high-value for Nathan and any future team users.

## Coding Prompt
```
1. Add Slack webhook integration to notification_service.py:
   - SLACK_WEBHOOK_URL env var
   - Post to #calls channel (or configurable)
   
2. Create services/summary_service.py:
   - After call ends, get full transcript from DB
   - Send to Groq: "Summarize this call in 2-3 sentences. Include: caller name/company, purpose, action items, risk level."
   - Return structured summary: {summary, action_items, risk_level, caller_info}
   
3. Format Slack message as Block Kit attachment:
   - Header: 📞 Incoming Call from {caller_name} ({phone})
   - Body: AI summary
   - Fields: Duration, Type (healthcare/business/unknown), Disposition (forwarded/message/blocked)
   - Action buttons: View Transcript, Add to Contacts
   - Color: green (forwarded), yellow (message), red (blocked)
   
4. Trigger summary generation in call_handler.py on call end
5. Add user setting to toggle Slack notifications on/off
6. Write unit test for summary generation (mock Groq)
```

## Acceptance Criteria
- Slack message posted within 30s of call ending
- Summary is accurate and concise
- Risk level and action items included
- User can toggle off in settings
