# TODO-224: ForwardLane → Supabase User Migration Script

**Priority:** HIGH  
**Repo:** signal-studio-auth  
**Status:** pending  

## Description
There's no script to migrate existing ForwardLane users to Supabase Auth.
This is the blocking item for any production cutover from ForwardLane auth to Supabase auth.

## Task
Write `scripts/migrate_users.py` that:
1. Reads all users from ForwardLane Postgres
2. Creates each user in Supabase via Admin API
3. Sets `app_metadata` with legacy_user_id, org info, role
4. Supports dry-run mode and resume (idempotent)

## Coding Prompt
```
Create /data/workspace/projects/signal-studio-auth/scripts/migrate_users.py:

import os, httpx, psycopg2, json, time

FORWARDLANE_DB_URL = os.environ["FORWARDLANE_DATABASE_URL"]
SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_SERVICE_KEY = os.environ["SUPABASE_SERVICE_KEY"]
DRY_RUN = os.environ.get("DRY_RUN", "true").lower() == "true"

def get_forwardlane_users(conn):
    """Query users + org info from ForwardLane Postgres."""
    # SELECT u.id, u.email, u.first_name, u.last_name, u.role,
    #        o.id as org_id, o.name as org_name, o.vertical
    # FROM users u LEFT JOIN organizations o ON u.organization_id = o.id
    pass

def create_supabase_user(client, user):
    """Create user in Supabase with metadata. Returns (created, user_id)."""
    # POST /auth/v1/admin/users
    # If email exists, return existing user ID
    pass

def set_user_metadata(client, supabase_user_id, fl_user):
    """Set app_metadata + user_metadata on Supabase user."""
    from mapping.user_mapping import forwardlane_to_supabase_metadata
    meta = forwardlane_to_supabase_metadata(fl_user)
    # PUT /auth/v1/admin/users/{supabase_user_id}
    pass

def main():
    conn = psycopg2.connect(FORWARDLANE_DB_URL)
    users = get_forwardlane_users(conn)
    print(f"Found {len(users)} users to migrate. DRY_RUN={DRY_RUN}")
    
    results = {"created": 0, "skipped": 0, "errors": 0}
    with httpx.Client() as client:
        for user in users:
            try:
                if not DRY_RUN:
                    supabase_id, created = create_supabase_user(client, user)
                    if created:
                        set_user_metadata(client, supabase_id, user)
                        results["created"] += 1
                    else:
                        results["skipped"] += 1
                else:
                    print(f"[DRY RUN] Would migrate: {user['email']}")
            except Exception as e:
                print(f"ERROR migrating {user['email']}: {e}")
                results["errors"] += 1
    
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()

Requirements: Add psycopg2-binary to requirements.txt
Add to MIGRATION_GUIDE.md: Step-by-step for running migration script
```

## Dependencies
- TODO-222 (RBAC) should be done first so roles are set correctly during migration
- Requires FORWARDLANE_DATABASE_URL and Supabase credentials

## Estimated Effort
M (4-6 hours)

## Acceptance Criteria
- Dry-run mode shows all users without creating any
- Full run creates all users in Supabase with correct app_metadata
- Idempotent (re-running skips existing users)
- Logs errors without crashing
