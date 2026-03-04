# TODO-462: Enforce MFA for Admin Users (django-otp)

**Priority:** HIGH  
**Repo:** forwardlane-backend  
**Effort:** M (4-6 hours)  
**Dependencies:** None (django-otp already installed)

## Description
`django-otp` is already in the Pipfile but MFA enforcement is not wired up for admin users. Financial data platform — MFA is non-negotiable for compliance.

## Coding Prompt
```
In /data/workspace/projects/forwardlane-backend/:

1. Verify django-otp is in INSTALLED_APPS (forwardlane/settings/base.py):
   Add if missing: 'django_otp', 'django_otp.plugins.otp_totp', 'django_otp.plugins.otp_static'

2. Add OTP middleware to MIDDLEWARE (after AuthenticationMiddleware):
   'django_otp.middleware.OTPMiddleware'

3. Enforce MFA for Django admin:
   In forwardlane/admin.py (or equivalent):
   from django_otp.admin import OTPAdminSite
   admin.site.__class__ = OTPAdminSite

4. Add API endpoint for MFA setup (TOTP enrollment):
   - POST /api/v1/auth/mfa/setup/ → generate TOTP device + QR code
   - POST /api/v1/auth/mfa/verify/ → verify TOTP token
   - Use qrcode library (already in Pipfile) for QR generation

5. Add user preference: require_mfa (default False, org admins can enforce for all)

6. Run migrations

7. Add tests:
   - Test admin login requires OTP
   - Test TOTP enrollment flow

8. Commit: "security: enforce MFA for admin via django-otp TOTP"
```

## Acceptance Criteria
- [ ] Django admin requires MFA
- [ ] TOTP enrollment API endpoints work
- [ ] QR code generation works with qrcode library
- [ ] Tests cover MFA flow
