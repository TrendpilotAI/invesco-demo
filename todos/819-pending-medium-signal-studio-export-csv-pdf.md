# TODO-819: Add CSV/PDF export for signal results

**Priority**: MEDIUM (P2)
**Repo**: signal-studio
**Source**: BRAINSTORM.md → 3.1

## Description
Signal results are displayed in the UI but cannot be exported. Compliance teams need printable/downloadable reports.

## Coding Prompt
```
In /data/workspace/projects/signal-studio:

1. Install: pnpm add papaparse jspdf jspdf-autotable
   pnpm add -D @types/papaparse

2. Create app/api/signals/[id]/results/export/route.ts:
   GET /api/signals/[id]/results/export?format=csv|pdf
   - Fetch signal results from BFF/signal builder
   - If format=csv: use papaparse to generate CSV, return with Content-Disposition: attachment
   - If format=pdf: use jspdf-autotable to generate PDF with signal metadata header + results table

3. Add export buttons to signal results UI:
   - "Export CSV" button with download icon
   - "Export PDF" button
   Both call the export API route and trigger browser download.

4. Include signal metadata in export header:
   - Signal name, ID, run timestamp, parameters used

5. Add rate limiting to export route (5 req/min — exports are expensive).

6. Add audit log entry for exports.
```

## Acceptance Criteria
- [ ] CSV export downloads correct data with headers
- [ ] PDF export includes signal metadata + results table
- [ ] Export buttons visible in signal results view
- [ ] Export actions appear in audit_log

## Effort
2 days

## Dependencies
TODO-817 (Zod validation) recommended first
