# TODO 008 — Ultrafone: Google Calendar Integration for Healthcare Calls

**Status:** pending  
**Priority:** medium  
**Project:** Ultrafone  
**Created:** 2026-02-26

---

## Overview

When the AI receptionist handles a healthcare call, it extracts appointment details (office name, appointment type, date/time). Currently those details are just saved as JSON in `extracted_info`. This task connects those extracted details directly to Google Calendar so appointments are auto-created or Nathan gets a "Create Event" action in the app.

---

## Coding Prompt

```
You are an integrations agent for the Ultrafone project at /data/workspace/projects/Ultrafone/

Your task is to add Google Calendar integration for healthcare appointment calls:

1. Review how healthcare calls are handled:
   cat /data/workspace/projects/Ultrafone/backend/services/receptionist.py
   Search for "healthcare" and "extracted_info" to understand what data is captured.

2. Create a Google Calendar service:
   File: /data/workspace/projects/Ultrafone/backend/services/calendar_service.py
   
   Requirements:
   - Use google-api-python-client library (add to requirements.txt)
   - Auth via service account (GOOGLE_SERVICE_ACCOUNT_JSON env var) OR OAuth2 (GOOGLE_OAUTH_CREDENTIALS)
   - Method: create_event(calendar_id, summary, start_time, end_time, description, location=None) -> event_id
   - Method: list_upcoming_events(calendar_id, days_ahead=7) -> list of events
   - Handle timezone correctly (Nathan is in EST/EDT)

3. Integrate into the receptionist's healthcare call handler:
   After a healthcare call completes and extracted_info contains appointment details:
   - If date/time are present: create a calendar event automatically
   - If date/time are missing: add a "Review and schedule" reminder event
   - Store the calendar event_id in extracted_info['calendar_event_id']

4. Add a backend API endpoint:
   POST /api/calls/{call_id}/create-event
   - Manually triggers calendar event creation from call extracted info
   - Returns {event_id, event_url}

5. Add "Create Event" button in the frontend CallHistory.tsx for healthcare calls:
   - Show button if call_type == "healthcare" and no calendar_event_id yet
   - Call POST /api/calls/{call_id}/create-event
   - Show success/error toast

6. Required env vars to document:
   GOOGLE_CALENDAR_ID (default: "primary")
   GOOGLE_SERVICE_ACCOUNT_JSON or GOOGLE_OAUTH_CREDENTIALS
   CALENDAR_TIMEZONE (default: "America/New_York")

7. Write unit tests mocking the Google Calendar API.
```

---

## Dependencies

- TODO 004 (deployment) — can be developed locally first

---

## Effort

**Estimate:** 6-8 hours  
**Type:** Backend Integration + Frontend

---

## Acceptance Criteria

- [ ] `calendar_service.py` created with create/list methods
- [ ] Healthcare calls trigger automatic event creation when date/time extracted
- [ ] Manual "Create Event" endpoint implemented
- [ ] Frontend "Create Event" button added for healthcare calls
- [ ] Unit tests for calendar service
- [ ] Env vars documented
