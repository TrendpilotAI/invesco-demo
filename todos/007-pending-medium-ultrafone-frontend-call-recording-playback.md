# TODO 007 — Ultrafone: Frontend Call Recording Playback

**Status:** pending  
**Priority:** medium  
**Project:** Ultrafone  
**Created:** 2026-02-26

---

## Overview

The backend stores Twilio recording URLs (`recording_url` in CallRecord model) but the frontend has no way to play them back. The CallHistory and LiveCall pages need an audio player component so Nathan can listen to call recordings.

---

## Coding Prompt

```
You are a frontend agent for the Ultrafone project at /data/workspace/projects/Ultrafone/

Your task is to add call recording playback to the React frontend:

1. Review the current frontend structure:
   ls /data/workspace/projects/Ultrafone/frontend/src/
   cat /data/workspace/projects/Ultrafone/frontend/src/pages/CallHistory.tsx
   cat /data/workspace/projects/Ultrafone/frontend/src/pages/LiveCall.tsx
   cat /data/workspace/projects/Ultrafone/frontend/src/types/index.ts

2. Create a CallRecordingPlayer component:
   File: /data/workspace/projects/Ultrafone/frontend/src/components/CallRecordingPlayer.tsx
   
   Requirements:
   - Accept props: recordingUrl: string | null, duration: number | null
   - Show "No recording" state if recordingUrl is null
   - HTML5 audio element with custom controls styled with Tailwind
   - Controls: play/pause button, seek slider, current time / total time display
   - Download button (download the recording)
   - Handle Twilio recording URL authentication if needed (proxy through backend if CORS issues)
   - Loading state while audio loads

3. Add a recording proxy endpoint to avoid CORS issues with Twilio:
   File: /data/workspace/projects/Ultrafone/backend/api/routes/calls.py
   Add: GET /api/calls/{call_id}/recording → proxies the Twilio recording URL with auth headers

4. Integrate the player into CallHistory.tsx:
   - Show the player in the expanded call detail view
   - Only show if recording_url is present in the call data

5. Integrate into LiveCall.tsx:
   - Show recording player when a live call transitions to "completed" state

6. Update the CallResponse Pydantic model to include recording_url field if missing.

Use Tailwind CSS for styling. Match the existing dark/professional UI aesthetic of the app.
```

---

## Dependencies

- TODO 004 (recording URLs only available from deployed Twilio integration)

---

## Effort

**Estimate:** 4-5 hours  
**Type:** Frontend / React

---

## Acceptance Criteria

- [ ] `CallRecordingPlayer` component created and styled
- [ ] Backend recording proxy endpoint added
- [ ] Player integrated into `CallHistory.tsx`
- [ ] Player integrated into `LiveCall.tsx`
- [ ] Recording downloads work correctly
