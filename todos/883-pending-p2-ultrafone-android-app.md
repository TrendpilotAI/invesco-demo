# 883 · Android App (Cross-Platform Flutter Build)

**Project:** Ultrafone  
**Priority:** P2 (Market Expansion)  
**Status:** pending  
**Effort:** 3 days  
**Created:** 2026-03-10

---

## Problem

Ultrafone has an iOS Flutter app (`ios-app/`) but no Android build. Android = 70% of smartphone market. The Flutter codebase is already cross-platform — Android support is mostly configuration work.

## Task

Configure the existing Flutter codebase to build and run on Android. Submit to Google Play.

## Steps

### 1. Rename `ios-app/` → `mobile-app/`

```bash
mv /data/workspace/projects/Ultrafone/ios-app /data/workspace/projects/Ultrafone/mobile-app
# Update all references in README, DEPLOYMENT.md, etc.
```

### 2. Add Android Configuration

```yaml
# mobile-app/android/app/build.gradle
android {
    compileSdk 34
    
    defaultConfig {
        applicationId "ai.ultrafone.app"
        minSdk 21  # Android 5.0+
        targetSdk 34
        versionCode 1
        versionName "1.0.0"
    }
}
```

### 3. Push Notifications: FCM vs APNs

iOS uses APNs (already planned, TODO 570). Android needs FCM:

```dart
// mobile-app/lib/services/notification_service.dart
// Add FCM token registration alongside APNs
if (Platform.isAndroid) {
  final fcmToken = await FirebaseMessaging.instance.getToken();
  await apiService.registerFcmToken(fcmToken);
}
```

Backend: add `fcm_token` column to user_profiles table, send via Firebase Admin SDK.

### 4. Google Play Submission
- Create Google Play Console account ($25 one-time)
- Generate signed release APK/AAB
- Privacy policy URL required
- Screenshot set (phone + tablet)
- App description: "AI receptionist that screens your calls"

### 5. Deep Link Handling (Android)
```xml
<!-- AndroidManifest.xml -->
<intent-filter android:autoVerify="true">
    <action android:name="android.intent.action.VIEW"/>
    <category android:name="android.intent.category.DEFAULT"/>
    <category android:name="android.intent.category.BROWSABLE"/>
    <data android:scheme="https" android:host="app.ultrafone.ai"/>
</intent-filter>
```

## Acceptance Criteria
- [ ] App builds on Android without errors
- [ ] All 5 screens work (dashboard, calls, contacts, settings, voicemails)
- [ ] Push notifications via FCM
- [ ] Real-time WebSocket transcript works
- [ ] Google Play beta track submission
- [ ] iOS functionality unchanged (regression test)

## Dependencies
- Depends on: iOS backend integration (TODO 569) — same backend
- Depends on: APNs push notifications (TODO 570) — FCM is parallel track
