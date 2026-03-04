# TODO 570 — iOS Push Notifications via APNs

**Priority:** HIGH  
**Repo:** Ultrafone  
**Effort:** 1-2 days  
**Status:** pending

## Description
Real-time call approval requires the user to get an iOS push notification when a call comes in and is awaiting decision. Without this, Ultrafone is not usable as a real product.

## Coding Prompt
```python
# Backend: notification_service.py — add APNs support
# Use httpx-based APNs provider or aioapns library

# 1. Install: pip install aioapns
# 2. Add to settings.py:
#    APNS_CERT_PATH, APNS_KEY_PATH, APNS_TOPIC (bundle ID)
#    Or use Firebase FCM as alternative (simpler for Flutter)

# 3. Update NotificationService.notify_incoming_call():
async def send_push_notification(self, device_token: str, call_data: dict):
    payload = {
        "aps": {
            "alert": {
                "title": f"Call from {call_data['caller_name'] or call_data['phone']}",
                "body": "Tap to approve or block"
            },
            "sound": "default",
            "badge": 1,
            "category": "CALL_DECISION"
        },
        "call_id": call_data["call_id"]
    }
    # Send via aioapns or FCM

# Flutter: Register device token
# firebase_messaging package in pubspec.yaml
# On app launch: FirebaseMessaging.instance.getToken() → POST /api/devices/register
```

## Acceptance Criteria
- [ ] Device token registration endpoint (`POST /api/devices/register`)
- [ ] Push sent on incoming call awaiting approval
- [ ] Push includes caller name + approve/reject action buttons
- [ ] Deep link from notification opens live call screen

## Dependencies
- TODO 569 (Flutter API wiring)
