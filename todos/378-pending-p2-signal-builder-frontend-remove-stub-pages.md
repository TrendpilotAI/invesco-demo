# TODO-378: Remove/Clean Up Stub and Abandoned Pages

**Repo:** signal-builder-frontend  
**Priority:** P2 (Medium)  
**Effort:** S (Small, ~1-2 hrs)  
**Created:** 2026-03-02

## Description

4 of 8 pages in the app are stubs or abandoned:

- `src/pages/index.tsx` — renders `<h1>Index Page</h1>` only
- `src/pages/creator/index.tsx` — contains only a datepicker demo (scratchpad, not connected to any module)
- `src/pages/services/index.tsx` — renders `<h1>Services Page</h1>` only
- `src/pages/settings/index.tsx` — renders `<h1>Settings Page</h1>` only
- `src/pages/catalog/index.tsx` — partially active, uses hardcoded `dataPreview` fixture instead of real API

These add dead routes to the app and confuse future developers.

## Coding Prompt

```
In /data/workspace/projects/signal-builder-frontend/:

1. Audit the router config at src/app/router/ to find which routes are actively used
2. For stub pages (creator, services, settings, index):
   - If a real feature is planned: add a TODO comment with ticket reference and show a "Coming soon" placeholder
   - If not planned: remove the page file and its route entry
3. For catalog/index.tsx: replace hardcoded dataPreview fixture with actual API call
4. Ensure no broken routes remain after cleanup
5. Update README if it references removed pages
```

## Acceptance Criteria
- No page renders just a `<h1>Page Name</h1>` stub
- Catalog page fetches real data from API
- Router has no dead routes pointing to empty pages
- All tests pass after cleanup
