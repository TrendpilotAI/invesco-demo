# TODO-502: Supabase Webhook Handler

**Priority:** P2  
**Effort:** M (~4h)  
**Repo:** signal-studio-auth  
**Status:** pending

## Description
When users are deleted or verify their email in Supabase, the auth service has no way to clean up related Redis tokens or trigger downstream flows. Add a webhook endpoint.

## Implementation
```python
# routes/webhooks.py
@router.post("/webhooks/supabase")
async def supabase_webhook(request: Request):
    # Verify SUPABASE_WEBHOOK_SECRET header
    # Handle: user.deleted → purge rt:{token} keys from Redis
    # Handle: user.updated (email_confirmed_at set) → trigger onboarding
    ...
```

## Acceptance Criteria
- [ ] Webhook HMAC signature verified
- [ ] User deletion purges Redis tokens
- [ ] Email verification event logged
- [ ] Tests cover happy path + invalid signature rejection
