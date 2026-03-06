---
id: 640
status: pending
priority: P2
repo: signal-studio-templates
title: CSV and Excel export for template execution results
effort: S (1 day)
dependencies: [634, 635]
---

# CSV / Excel Export for Template Results

## Problem
Financial advisors expect to export query results to CSV/Excel. Currently no export functionality exists.

## Task
Add export endpoints and a frontend download button to the gallery component.

## Coding Prompt
```
In /data/workspace/projects/signal-studio-templates/:

1. pnpm add xlsx
2. pnpm add -D @types/xlsx (if needed, check if included)

3. Create src/utils/export.ts:
   - rowsToCSV(rows: Record<string, any>[], outputSchema: OutputField[]): string
     - Uses outputSchema labels as headers
     - Handles currency/percentage formatting
   - rowsToExcel(rows: Record<string, any>[], templateName: string, outputSchema: OutputField[]): Buffer
     - Creates workbook with single sheet named after template
     - Bold headers, auto-width columns

4. Add to api/templates.ts:
   GET /templates/:id/execute?format=csv — runs execute + returns CSV with Content-Disposition: attachment
   GET /templates/:id/execute?format=xlsx — runs execute + returns Excel binary

   Accept query params for template parameters (same as POST body fields)

5. In components/template-gallery.tsx:
   Add "Export CSV" and "Export Excel" buttons to TemplatePreview component

6. Tests for export utils: rowsToCSV returns valid CSV, rowsToExcel returns non-empty buffer
```

## Acceptance Criteria
- [ ] GET /templates/:id/execute?format=csv returns downloadable CSV
- [ ] GET /templates/:id/execute?format=xlsx returns downloadable Excel
- [ ] Export buttons visible in gallery preview
- [ ] Output uses human-readable labels from outputSchema
- [ ] `pnpm test` passes
