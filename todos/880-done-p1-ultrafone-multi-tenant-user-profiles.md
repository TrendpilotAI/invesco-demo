# TODO-880 Done: Multi-tenant UserProfile (remove hardcoded `user_id="nathan"`)

**Commit:** `128cbe3`  
**Branch:** `main`  
**Repo:** https://github.com/TrendpilotAI/Ultrafone  
**Date:** 2026-03-11

---

## Summary

Removed all 8 hardcoded `user_id="nathan"` occurrences across service files and replaced them with dynamic tenant resolution via a new `UserProfile` model. Ultrafone is now architecturally multi-tenant.

---

## Changes Made

### New Files

| File | Purpose |
|------|---------|
| `backend/models/user_profile.py` | SQLAlchemy model: maps Twilio number → tenant |
| `backend/services/user_profile_service.py` | `get_profile_by_twilio_number()`, `get_profile_by_id()` |
| `backend/tests/unit/test_user_profile.py` | 11 unit tests covering model, DB, service, and receptionist layers |
| `supabase/migrations/20260311000001_add_user_profiles.sql` | Migration + Nathan seed row for backward compat |

### Modified Files

| File | Change |
|------|--------|
| `backend/models/__init__.py` | Export `UserProfile` |
| `backend/services/receptionist.py` | `AIReceptionist.__init__` accepts `user_profile: UserProfile`; 5× `user_id="nathan"` → `user_profile.id` |
| `backend/services/agent_functions.py` | 3× `user_id="nathan"` → `get_user_id_for_call(call_sid)` (looks up CallRecord) |
| `backend/services/call_record_service.py` | `create_call_record()` now accepts `user_id` param; added `get_user_id_for_call()` |
| `backend/services/call_handler.py` | `handle_incoming_call()` accepts `user_profile`; passes it to `_handle_ai_receptionist()` |
| `backend/main.py` | Twilio webhook extracts `To` number, looks up `UserProfile`, rejects unknown numbers with TwiML |
| `backend/api/routes/settings.py` | Added `GET /api/settings/profile` and `PUT /api/settings/profile` endpoints |

---

## Routing Flow (After This Change)

```
Twilio call arrives
    → main.py extracts To (Twilio number) + From (caller)
    → get_profile_by_twilio_number(To) → UserProfile (or reject)
    → handle_incoming_call(caller_phone, call_sid, user_profile=profile)
    → create_call_record(..., user_id=profile.id)
    → AIReceptionist(call_id, caller_phone, user_profile=profile)
    → all notify_ios_app() calls use profile.id
    → agent_functions.py uses get_user_id_for_call(call_sid) → CallRecord.user_id
```

---

## Backward Compatibility

- `create_call_record()` defaults `user_id="nathan"` — pre-existing code paths not yet updated won't break
- `get_user_id_for_call()` falls back to `"nathan"` if no matching CallRecord found
- Nathan's legacy profile seeded in migration with `id='nathan'` so existing DB rows still resolve
- Unknown Twilio numbers are **rejected at the webhook level** with a TwiML hangup message

---

## Tests Added (`test_user_profile.py`)

- `UserProfile` model defaults (persona_name, business_type, enable_dnd, etc.)
- UUID string auto-generation for id
- DB persistence and unique phone_number constraint
- `get_profile_by_twilio_number` — found, not found, None input
- `get_user_id_for_call` — found, fallback to "nathan"
- `create_call_record` — stores user_id / defaults to "nathan"
- `AIReceptionist` propagates `profile.id` to notifications (no "nathan" leak)

---

## Next Steps (Not in Scope for P1)

- Wire `UserProfile` to proper auth (JWT → profile lookup instead of `phone_number` query param)
- Migrate `UserSettings.user_id` to reference `UserProfile.id` as a FK
- Add `POST /api/settings/profile` for provisioning new tenants
- Update `callers` table to use `UserProfile.id` instead of freeform `user_id` string
- Backfill old CallRecords from `user_id="nathan"` to the seeded profile UUID if desired
