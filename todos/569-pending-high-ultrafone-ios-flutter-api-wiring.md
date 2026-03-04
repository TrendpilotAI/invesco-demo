# TODO 569 — Wire Flutter iOS App to Backend API

**Priority:** HIGH  
**Repo:** Ultrafone  
**Effort:** 2-3 days  
**Status:** pending

## Description
The Flutter iOS app has all UI screens built but zero API calls are connected. This is the #1 gap between demo and usable product.

## Screens to Wire
1. Dashboard — live call status (WebSocket), stats
2. Call History — GET /api/calls, recording playback
3. Settings — GET/PUT /api/settings (DND, voice selection)
4. Contacts — GET /api/contacts, search
5. Live Call Screen — WebSocket for real-time transcript + approve/reject

## Coding Prompt
```dart
// 1. Create API service layer in lib/services/api_service.dart
// Base URL from environment config
// Auth via Supabase JWT token

// 2. Create WebSocket service in lib/services/websocket_service.dart
// Connect to ws://{backend}/ws/calls
// Handle: call_started, call_updated, call_ended, transcript events

// 3. Wire Dashboard page
// - Fetch active calls via WebSocket
// - Show stats from GET /api/dashboard/stats

// 4. Wire Settings page  
// - GET /api/settings → populate form
// - PUT /api/settings → save on change

// 5. Wire Call History page
// - GET /api/calls?limit=50&offset=0
// - Pagination via ListView.builder
// - Audio playback for recordings

// 6. Wire Contacts page
// - GET /api/contacts?search={query}
// - Contact detail view

// 7. Add Supabase auth flow (login screen)
// supabase_flutter package already in pubspec?
```

## Acceptance Criteria
- [ ] Auth flow working (login/logout via Supabase)
- [ ] Dashboard shows real call data
- [ ] Call history loads and plays recordings
- [ ] Settings save/load correctly
- [ ] Contacts searchable
- [ ] WebSocket live updates working on dashboard

## Dependencies
- TODO 568 (keys rotated / backend running)
