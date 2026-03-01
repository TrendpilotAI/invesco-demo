# TODO-347: Complete Settings Page

**Repo:** signal-studio-frontend  
**Priority:** P2  
**Effort:** M (4-6 hours)  
**Dependencies:** TODO-337, TODO-338

## Description
Settings page is likely a stub. Build out full settings with org management, profile, integrations, and notification preferences.

## Coding Prompt
```
In /data/workspace/projects/signal-studio-frontend/src/app/(app)/settings/:

Use Radix Tabs to organize:

1. Profile Tab (page.tsx or profile/page.tsx):
   - Full name, email, avatar upload
   - Change password form
   - Delete account (danger zone)

2. Organization Tab:
   - Org name, logo upload
   - Org slug (read-only)
   - Invite member by email (useOrgMembers)
   - Members list with role dropdown (admin/editor/viewer)
   - Remove member button (admin only)

3. Integrations Tab:
   - Data sources list (useDataSources)
   - Connect new: Snowflake, Supabase, Oracle, Postgres, API
   - Each shows status badge + last sync time
   - Test connection button

4. Notifications Tab:
   - Email notifications toggle per event type
   - Signal run complete, signal failed, weekly digest
   - Webhook URL for org-level notifications

5. Billing Tab → link to TODO-344
```

## Acceptance Criteria
- [ ] All 5 tabs render
- [ ] Profile can be updated
- [ ] Members can be invited
- [ ] Data sources listed with status
- [ ] Notification prefs saved
