# TODO 417: Complete Supabase RLS Policies

**Repo:** Ultrafone  
**Priority:** High  
**Effort:** S (half day)  
**Dependencies:** None

## Description
Row-Level Security (RLS) policies in Supabase are likely incomplete. Without them, any authenticated user could read all call records, contacts, and settings — a serious privacy issue.

## Coding Prompt
```
1. Review all Supabase tables: call_records, callers, contacts, call_transcripts, user_settings
2. For each table, enable RLS if not already: ALTER TABLE x ENABLE ROW LEVEL SECURITY;
3. Create policies:
   - call_records: user can only SELECT/INSERT/UPDATE their own records (user_id = auth.uid())
   - callers: same user_id scoping
   - contacts: scoped to user_id
   - call_transcripts: joined through call_records user_id
   - user_settings: user_id = auth.uid()
4. Test: create two test users, verify user A cannot see user B's call records
5. Update supabase/migrations/ with new migration files
6. Document RLS policies in ARCHITECTURE.md
```

## Acceptance Criteria
- All tables have RLS enabled with appropriate policies
- Cross-user data access is impossible
- Supabase migration files updated
