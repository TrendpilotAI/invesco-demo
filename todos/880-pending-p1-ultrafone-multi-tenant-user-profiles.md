# 880 · Multi-Tenant User Profiles (Remove Hardcoded "nathan")

**Project:** Ultrafone  
**Priority:** P1 (SaaS Blocker)  
**Status:** pending  
**Effort:** 2 days  
**Created:** 2026-03-10

---

## Problem

`user_id="nathan"` is hardcoded in 5 places in `backend/services/receptionist.py` (lines 171, 276, 374, 424, 512). This makes Ultrafone a single-user system. Multi-tenancy and SaaS are impossible until this is fixed.

## Task

Implement proper multi-tenant user profile architecture.

## Implementation

### 1. Create `UserProfile` Model

```python
# backend/models/user_profile.py
from sqlalchemy import Column, String, Boolean, JSON
from models.base import Base

class UserProfile(Base):
    __tablename__ = "user_profiles"
    
    id = Column(String, primary_key=True)  # UUID
    phone_number = Column(String, unique=True, nullable=False)  # Twilio number
    owner_phone = Column(String, nullable=False)  # User's real phone
    persona_name = Column(String, default="Your AI Receptionist")
    business_type = Column(String, default="general")  # financial, healthcare, executive
    
    # Business-specific config
    interview_config = Column(JSON, default={})
    
    # Feature flags
    enable_dnd = Column(Boolean, default=False)
    enable_calendar_intel = Column(Boolean, default=False)
    
    created_at = Column(...)
```

### 2. Route Twilio by `To` Number → UserProfile

```python
# In webhook handler:
to_number = form_data.get("To")
user_profile = await db.query(UserProfile).filter_by(phone_number=to_number).first()
if not user_profile:
    # Unknown number — return TwiML error
    return Response(content="<Response><Reject/></Response>")

# Pass user_profile to receptionist
await receptionist.handle_call(call_sid, caller_number, user_profile=user_profile)
```

### 3. Update Receptionist to Accept UserProfile

```python
# backend/services/receptionist.py
class ReceptionistService:
    async def handle_call(self, call_sid: str, from_number: str, user_profile: UserProfile):
        # Replace all `user_id="nathan"` with `user_profile.id`
        call_record = await self.call_record_service.create_record(
            user_id=user_profile.id,  # Dynamic!
            from_number=from_number,
            ...
        )
```

### 4. Database Migration

```python
# alembic migration
op.create_table("user_profiles", ...)

# Seed Nathan's profile
op.execute("""
    INSERT INTO user_profiles (id, phone_number, owner_phone, persona_name, business_type)
    VALUES ('nathan', '+19129129545', '+13107798590', 'Nathan''s AI Receptionist', 'financial')
""")
```

## Acceptance Criteria
- [ ] `UserProfile` model created and migrated
- [ ] All 5 hardcoded `user_id="nathan"` replaced with dynamic lookup
- [ ] Twilio `To` number routes to correct user profile
- [ ] Nathan's profile seeded in migration (backward compatible)
- [ ] Test: second user profile works independently
- [ ] API: `GET /settings/profile` returns current user's profile
- [ ] API: `PUT /settings/profile` updates persona/config

## Dependencies
- Depends on: Nothing (foundation task)
- Blocks: Stripe billing (TODO 572), SaaS onboarding
