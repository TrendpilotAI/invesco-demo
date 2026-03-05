# TODO-602: Org Membership Validation on /invite-to-org

**Repo:** signal-studio-auth  
**Priority:** P1 (MEDIUM)  
**Effort:** 2h  
**Status:** pending

## Problem
`/invite-to-org` checks that caller has `admin` role but does NOT verify the caller belongs to the target organization. An admin of org A can invite users to org B.

## Fix

In `routes/auth_routes.py`, after the role check, query Supabase to verify membership:

```python
# After role check
org_id = body.org_id  # from request body

# Verify caller is a member of the target org
async with httpx.AsyncClient() as client:
    membership_resp = await client.get(
        f"{SUPABASE_URL}/rest/v1/organization_members",
        params={"user_id": f"eq.{caller_user_id}", "org_id": f"eq.{org_id}"},
        headers={
            "apikey": SUPABASE_SERVICE_KEY,
            "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}",
        },
    )
    members = membership_resp.json()
    if not members:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this organization.",
        )
```

## Files to Change
- `routes/auth_routes.py` — add org membership check in `/invite-to-org` handler

## Acceptance Criteria
- [ ] Admin of org A cannot invite to org B (403 returned)
- [ ] Admin of org A can still invite to org A
- [ ] Unit test: admin cross-org invite → 403
- [ ] Existing invite test still passes

## Dependencies
- TODO-600 (httpx pooling — use shared client)
- Migration `001_organizations.sql` must be deployed (has `organization_members` table)
