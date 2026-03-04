# TODO-468: Add Template Preview / Dry-Run Mode

**Repo:** signal-studio-templates
**Priority:** P1
**Effort:** S (3h)
**Status:** pending
**Source:** judge-agent-v2 / BRAINSTORM.md Feature A

## Description

Sales demos need to show Invesco the template working without connecting to a real database. Add a preview/dry-run endpoint that returns schema-valid mock data based on the template's `exampleOutput`.

## Acceptance Criteria

- [ ] `POST /templates/:id/preview` endpoint returns mock rows (no DataProvider call)
- [ ] `SignalTemplate` schema extended with optional `previewData: ExampleRow[]` (3-5 rows)
- [ ] All 20 templates have preview data populated
- [ ] Preview mode also generates mock talking points if AIProvider not available
- [ ] API returns same shape as `/execute` with `{ dryRun: true }` flag in response

## Agent Prompt

```
In /data/workspace/projects/signal-studio-templates/:

1. Update schema/signal-template.ts:
   Add optional field to SignalTemplate: previewData?: ExampleRow[];

2. Update engine/template-engine.ts:
   Add preview() method:
   async preview(templateId: string, parameters: Record<string, any>): Promise<ExecutionResult> {
     // validate params as normal
     // return template.previewData as rows (no DataProvider call)
     // generate mock talking points string
     // return ExecutionResult with dryRun: true flag
   }

3. Update api/templates.ts:
   Add route: POST /templates/:id/preview
   Calls engine.preview() — no auth needed for this endpoint? (TBD — or same auth)

4. Populate previewData for all 20 templates in their respective .ts files
   (3-5 realistic example rows per template based on outputSchema)

5. Add test: __tests__/engine-preview.test.ts
```

## Dependencies

- None (additive feature, no existing functionality changed)
