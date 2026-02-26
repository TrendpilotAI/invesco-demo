# TODO 006 — Ultrafone: iOS Push Notifications Validation & Completion

**Status:** pending  
**Priority:** high  
**Project:** Ultrafone  
**Created:** 2026-02-26

---

## Overview

`notification_service.py` exists but its push notification delivery to iOS has never been validated in production. Nathan needs real-time alerts when: a call is forwarded, a suspicious caller is blocked, a voicemail is taken. This task validates the full push notification pipeline from call event → APNs → iPhone.

---

## Coding Prompt

```
You are an iOS push notification agent for the Ultrafone project at /data/workspace/projects/Ultrafone/

Your task is to validate and complete the push notification system:

1. Review the existing notification service:
   cat /data/workspace/projects/Ultrafone/backend/services/notification_service.py
   Identify what's implemented vs what's missing.

2. Ensure APNs integration is complete:
   - The service should use the `apns2` or `httpx` library to send to Apple Push Notification service
   - Required env vars: APNS_KEY_ID, APNS_TEAM_ID, APNS_BUNDLE_ID, APNS_AUTH_KEY_PATH
   - If using Firebase (FCM) instead: FIREBASE_SERVER_KEY
   - Add whichever is missing

3. Verify notification triggers are wired in the right places:
   Check /data/workspace/projects/Ultrafone/backend/services/call_handler.py and receptionist.py
   Ensure notify_ios_app() is called for these events:
   - Call forwarded to Nathan (with caller info + transcript snippet)
   - Call blocked (security score >= 7)
   - Voicemail taken (with message summary)
   - Live call started (for real-time monitoring prompt)

4. Add notification payload structure for each event type:
   - Forwarded: title="📞 Call Forwarded", body="{name} from {company}", data={call_id, transcript}
   - Blocked: title="🛡️ Call Blocked", body="Suspicious caller blocked (score: {score})"
   - Voicemail: title="📝 Voicemail", body="{name}: {summary}"

5. Create a test endpoint POST /api/notifications/test that sends a test push to a registered device token

6. Write unit tests in /data/workspace/projects/Ultrafone/backend/tests/unit/ for notification payloads

7. Update /data/workspace/projects/Ultrafone/backend/README_NOTIFICATIONS.md with setup instructions
```

---

## Dependencies

- TODO 004 (deploy first to have a production APNs endpoint)

---

## Effort

**Estimate:** 4-6 hours  
**Type:** Backend / Mobile Integration

---

## Acceptance Criteria

- [ ] `notification_service.py` sends real APNs/FCM pushes (not just logs)
- [ ] All 4 call event types trigger appropriate push notifications
- [ ] Test endpoint `/api/notifications/test` works
- [ ] Unit tests cover notification payload construction
- [ ] Setup documentation written
