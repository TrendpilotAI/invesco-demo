# TODO-359: Add Signal Export and Shareable Links

**Priority:** P2
**Effort:** M
**Repo:** signal-studio
**Status:** pending

## Description
No way to share or export signals. Users can create signals but can't export results (JSON/CSV) or share signals with colleagues. This is a key revenue feature for team/enterprise plans.

## Coding Prompt
```
In /data/workspace/projects/signal-studio:

1. Create export API at app/api/signals/[id]/export/route.ts:
   - GET ?format=json → return signal definition + last results as JSON
   - GET ?format=csv → return results as CSV (use papaparse or fast-csv)
   - Requires auth

2. Create shareable link API at app/api/signals/[id]/share/route.ts:
   - POST → generate JWT-signed share token, return shareable URL
   - GET /signals/shared/[token] → public view of signal (read-only, no auth required)
   - Token expires in 7 days, stored in Redis

3. Add export/share buttons to signal detail page and canvas page:
   - "Export JSON" button → triggers download
   - "Export CSV" button → triggers CSV download
   - "Share" button → copies link to clipboard, shows toast

4. Create app/(public)/signals/shared/[token]/page.tsx:
   - Validates JWT token
   - Shows read-only signal view
   - "Sign up to create your own" CTA

5. Install if needed: pnpm add papaparse jose

6. Commit: "feat(sharing): add signal export (JSON/CSV) and shareable links"
```

## Dependencies
- TODO-354 (execution must work first)

## Acceptance Criteria
- Export JSON/CSV works for signal results
- Shareable link generated with 7-day expiry
- Public shared view loads without auth
- Share CTA drives signups (conversion funnel)
