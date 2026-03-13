# TODO: Remove Hardcoded user_id and Enable Multi-Tenant User Profiles

## Priority: P1
## Repo: Ultrafone

### Problem
`user_id = "nathan"` is hardcoded in multiple backend files, blocking any multi-tenant SaaS usage. All phone calls and contacts are associated to a single hardcoded user.

### Action Items
- Audit all occurrences: `grep -r '"nathan"' backend/`
- Replace with JWT-authenticated user_id from Supabase auth
- Update all database queries to scope by authenticated user_id
- Implement Row Level Security in Supabase for contacts, calls, and transcripts tables
- Update iOS app to pass auth token in API requests
- Add test: two users cannot see each other's call data
- Enable Supabase RLS policies

### Impact
- Unlocks multi-tenant SaaS deployment
- Required for any paying customer beyond Nathan
- Eliminates data cross-contamination risk

### References
- ARCHITECTURE.md multi-tenant section
- TODO-417 (supabase-rls)
- TODO-880 (multi-tenant-user-profiles)
