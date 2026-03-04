# TODO 574 — Slack Call Summaries Integration

**Priority:** MEDIUM  
**Repo:** Ultrafone  
**Effort:** 1 day  
**Status:** pending

## Description
After each call, push an AI-generated summary to a Slack channel. High-value for ForwardLane use case where Nathan needs instant awareness of calls.

## Coding Prompt
```python
# backend/services/slack_service.py
import httpx

class SlackService:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
    
    async def post_call_summary(self, call_record: CallRecord, summary: str):
        color = "#ff0000" if call_record.spam_score > 7 else "#36a64f"
        blocks = [
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"*{call_record.caller_name or call_record.phone}*"},
                "fields": [
                    {"type": "mrkdwn", "text": f"*Status:* {call_record.outcome}"},
                    {"type": "mrkdwn", "text": f"*Duration:* {call_record.duration}s"},
                    {"type": "mrkdwn", "text": f"*Spam Score:* {call_record.spam_score}/10"},
                ]
            },
            {"type": "section", "text": {"type": "mrkdwn", "text": summary}},
        ]
        await httpx.AsyncClient().post(self.webhook_url, json={"blocks": blocks})

# Add SLACK_WEBHOOK_URL to settings.py
# Hook into call_record_service.py on call completion
# Generate summary via Groq: summarize transcript in 2 sentences
```

## Acceptance Criteria
- [ ] Slack message posted after each call completes
- [ ] Shows: caller name/number, outcome (forwarded/blocked/voicemail), spam score, AI summary
- [ ] Configurable webhook URL in settings
- [ ] Opt-in per user (not mandatory)

## Dependencies
- TODO 568 (secrets in Railway)
