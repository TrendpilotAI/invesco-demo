# 435 — Wire Flutter iOS App to Backend API

**Priority:** HIGH  
**Repo:** Ultrafone  
**Effort:** M (1-2 days)  

## Description

The Flutter iOS app (`ios-app/`) has all UI screens built but `api_service.dart` is a stub with no real API calls. The app is non-functional until wired to the FastAPI backend.

## Coding Prompt

Wire the following Flutter service methods to real backend endpoints:

```dart
// ios-app/lib/services/api_service.dart

class ApiService {
  final String baseUrl;
  final Dio _dio;

  // Dashboard / stats
  Future<DashboardStats> getStats() => 
    _dio.get('$baseUrl/api/stats').then((r) => DashboardStats.fromJson(r.data));

  // Call history
  Future<List<CallRecord>> getCallHistory({int limit = 50, int offset = 0}) =>
    _dio.get('$baseUrl/api/calls', queryParameters: {'limit': limit, 'offset': offset})
        .then((r) => (r.data as List).map(CallRecord.fromJson).toList());

  // Contacts
  Future<List<Contact>> getContacts() =>
    _dio.get('$baseUrl/api/contacts').then((r) => ...);

  // Settings
  Future<UserSettings> getSettings() =>
    _dio.get('$baseUrl/api/settings').then((r) => UserSettings.fromJson(r.data));
  Future<void> updateSettings(UserSettings settings) =>
    _dio.patch('$baseUrl/api/settings', data: settings.toJson());

  // Live call WebSocket
  Stream<CallEvent> liveCallStream(String callId) { ... }
  
  // Auth
  Future<String> login(String email, String password) { ... }
}
```

Also add:
- APNs push notification registration in `AppDelegate.swift`
- Supabase auth token storage in flutter_secure_storage
- Deep link handling for call approval

## Files to Modify
- `ios-app/lib/services/api_service.dart` — main wiring
- `ios-app/lib/providers/` — update providers to use real data
- `ios-app/ios/Runner/AppDelegate.swift` — APNs registration
- `ios-app/pubspec.yaml` — add `dio`, `flutter_secure_storage`

## Acceptance Criteria
- [ ] Dashboard loads real stats from backend
- [ ] Call history list populates from API
- [ ] Settings load/save persist to backend
- [ ] Auth flow uses Supabase JWT
- [ ] Live call view connects to WebSocket
- [ ] Push notifications register device token
