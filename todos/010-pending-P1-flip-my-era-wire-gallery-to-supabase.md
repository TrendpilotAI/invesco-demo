---
status: pending
priority: P1
issue_id: "010"
tags: [flip-my-era, gallery, supabase, frontend]
dependencies: []
---

# 010 — Wire Gallery Page to Real Supabase Data

## Overview

The Gallery page at `src/app/pages/Gallery.tsx` currently renders a hardcoded `SAMPLE_EBOOKS` array of 6 placeholder items. Real users cannot discover community-created ebooks, and the page has no value. This is a live app at flipmyera.com — the gallery is in the nav and accessible to all users, creating a poor first impression.

**Why P1:** Social proof and discoverability are critical to conversion. Users who see a gallery of real community stories are more likely to create their own. An empty/fake gallery actively hurts credibility.

## Coding Prompt

You are working on FlipMyEra, a React 18 + TypeScript + Supabase SaaS app at `/data/workspace/projects/flip-my-era/`.

**Task:** Replace the hardcoded mock data in the Gallery page with real Supabase queries.

### Step 1 — Audit the Supabase schema

Read the Supabase types file at `src/integrations/supabase/types.ts` to understand the `ebooks` table shape. Also check `supabase/migrations/` for any relevant migrations. You need to know columns available on the `ebooks` (or equivalent) table: at minimum `id`, `title`, `era`, `cover_image_url`, `created_at`, and whether there is a `user_id` or `creator_name` column.

### Step 2 — Update Gallery.tsx

File: `src/app/pages/Gallery.tsx`

1. Remove the `SAMPLE_EBOOKS` constant entirely.
2. Add a `useEffect` + `useState` to fetch from Supabase:
   ```typescript
   import { supabase } from '@/core/integrations/supabase/client';
   ```
3. Query: select ebooks that are marked public (if a `is_public` or `visibility` column exists) OR all ebooks ordered by `created_at desc` with a limit of 50.
4. Map the Supabase response to the existing `GalleryEbook` interface — adjust the interface if the DB column names differ.
5. Add loading state (show a skeleton grid of 6 cards while loading).
6. Add error state (show a friendly message if the query fails).
7. The `featured` property can be determined by a `featured` column on the ebook, or by likes count threshold (e.g., >10 likes = featured), whichever exists.

### Step 3 — Add empty-state UI

If zero public ebooks exist (fresh DB), show a compelling empty state:
```
"No ebooks yet — be the first to create one! ✨"
```
with a CTA button linking to the story creation wizard (`/stories`).

### Step 4 — Pagination (optional, implement if time allows)

If the total row count is > 50, add a "Load More" button that fetches the next page using `.range(offset, offset+49)`.

### Step 5 — Make sure RLS allows public reads

Check `supabase/migrations/` for the `ebooks` table RLS policy. If there is no `SELECT` policy for `anon` role, add a new migration file at `supabase/migrations/{timestamp}_allow_public_gallery_read.sql`:
```sql
CREATE POLICY "Anyone can view public ebooks"
  ON public.ebooks
  FOR SELECT
  USING (is_public = true);
```
(Adjust column name as needed based on actual schema.)

### Acceptance Criteria
- Gallery page fetches from Supabase, not hardcoded array
- Loading spinner shown while fetching
- Error message shown on failure
- Empty state shown when no public ebooks exist
- Existing filter (search + artist filter) still works on fetched data
- `npm run typecheck` passes with no new errors
- `npm run test:ci` passes

## Dependencies

None — can be done independently.

## Effort

S (2-4 hours)

## Acceptance Criteria

- [ ] `SAMPLE_EBOOKS` constant removed from Gallery.tsx
- [ ] Gallery fetches real data from Supabase `ebooks` table
- [ ] Loading state renders skeleton cards
- [ ] Error state shows friendly message
- [ ] Empty state shows CTA to create a story
- [ ] TypeScript compiles clean (`npm run typecheck`)
- [ ] Unit tests pass (`npm run test:ci`)
- [ ] Deployed to staging, gallery renders real data or empty state
