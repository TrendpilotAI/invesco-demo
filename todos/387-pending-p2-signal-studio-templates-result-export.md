# TODO 387: Signal Studio Templates — Result Export (CSV/Excel/PDF)

**Priority:** P2  
**Repo:** signal-studio-templates  
**Effort:** M (1-2 days)  
**Status:** pending

---

## Description

Add result export capability to the TemplateEngine and API layer. Invesco's compliance team requires that signal query results can be exported to CSV and Excel for reporting. PDF export for presentation-ready reports is a nice-to-have.

## Coding Prompt

```
Add export functionality to signal-studio-templates:

1. Add to engine/template-engine.ts:
   - New method: exportResults(rows: Record<string, any>[], outputSchema: OutputField[], format: 'csv' | 'excel'): Buffer
   - CSV: use built-in string building (no external dep needed)
   - Excel: use 'xlsx' package (add to dependencies)
   - Apply column labels from OutputField.label (not raw DB column names)
   - Apply type formatting: currency → "$1,234.56", percentage → "12.34%", date → "Mar 2, 2026"

2. Add to api/templates.ts:
   - POST /templates/:id/execute/export
   - Body: { params: {}, format: 'csv' | 'excel', options?: { includeTalkingPoints?: boolean } }
   - Response: file download with Content-Disposition header
   - CSV: Content-Type: text/csv
   - Excel: Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet

3. Add __tests__/export.test.ts:
   - Test CSV output with correct headers and row formatting
   - Test currency/percentage/date formatting
   - Test that empty result set returns header-only file

4. Add to README: Export section with curl example
```

## Dependencies
- TODO 101 (API auth) recommended but not blocking for core logic

## Acceptance Criteria
- [ ] `exportResults()` method on TemplateEngine
- [ ] CSV export produces correct headers and formatted values
- [ ] Excel export produces valid .xlsx file
- [ ] API endpoint responds with file download
- [ ] Tests passing
