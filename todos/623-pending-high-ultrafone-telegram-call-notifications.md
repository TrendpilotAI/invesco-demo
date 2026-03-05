# TODO 623 — Telegram Real-Time Call Notifications

**Repo:** Ultrafone  
**Priority:** HIGH  
**Effort:** 4 hours  
**Depends on:** None (Telegram bot exists in workspace)

## Problem
Nathan uses Telegram as primary comms. When a call comes in for screening, there's no real-time notification. Push notifications require iOS app wiring (TODO 569).

## Task
Add Telegram notification service to send call events with inline action buttons.

## Execution Prompt
```python
# In backend/services/telegram_notification_service.py
# Use python-telegram-bot or direct Bot API

import httpx
from config.settings import settings

TELEGRAM_BOT_TOKEN = settings.TELEGRAM_BOT_TOKEN  # add to settings
TELEGRAM_CHAT_ID = settings.TELEGRAM_CHAT_ID      # Nathan's chat ID

async def notify_incoming_call(caller_info: dict, call_sid: str):
    message = f"""📞 Incoming Call
    
From: {caller_info.get('name', 'Unknown')} ({caller_info.get('phone')})
Type: {caller_info.get('category', 'Unknown')}
Suspicion: {caller_info.get('suspicion_score', 0)}/10

AI is screening now..."""
    
    keyboard = {
        "inline_keyboard": [[
            {"text": "✅ Connect Me", "callback_data": f"connect:{call_sid}"},
            {"text": "📩 Take Message", "callback_data": f"message:{call_sid}"},
            {"text": "🚫 Block", "callback_data": f"block:{call_sid}"}
        ]]
    }
    
    await send_telegram_message(message, reply_markup=keyboard)

# Add webhook endpoint for callback_data responses
# Wire into call_handler.py after AI screening completes
```

## Acceptance Criteria
- [ ] Telegram message sent when call enters screening
- [ ] Inline buttons trigger Redis pub/sub (connect/message/block)
- [ ] Follow-up message sent when call ends with transcript summary
- [ ] TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID added to Railway env vars
