# TODO 390: Signal Studio Templates — Template Diff / Audit Trail

**Priority:** P1  
**Repo:** signal-studio-templates  
**Effort:** S (1 day)  
**Status:** pending

---

## Description

Compliance requirement for Invesco: maintain an audit trail of template SQL changes. When a template is updated, the system should record what changed (SQL diff), who changed it, and when. Critical for financial regulatory compliance.

## Coding Prompt

```
Add template diff and audit trail to signal-studio-templates:

1. New file: utils/template-diff.ts
   - Function diffTemplates(oldTemplate: SignalTemplate, newTemplate: SignalTemplate): TemplateDiff
   - Interface TemplateDiff { templateId: string; changedFields: string[]; sqlDiff: string | null; timestamp: Date; summary: string }
   - sqlDiff: produce line-by-line diff of sqlTemplate strings using built-in string comparison (no external diff lib needed — split on newlines, compare)
   - changedFields: list field names that changed (name, description, parameters, sqlTemplate, etc.)
   - summary: human-readable change description: "SQL modified (3 lines changed), 1 parameter added"

2. New file: utils/audit-log.ts
   - Interface AuditEntry { templateId: string; action: 'created' | 'updated' | 'deleted' | 'executed'; diff?: TemplateDiff; userId?: string; tenantId?: string; timestamp: Date }
   - Class AuditLog { private entries: AuditEntry[]; log(entry: AuditEntry): void; getHistory(templateId: string): AuditEntry[]; export(): AuditEntry[] }
   - In-memory implementation (pluggable — can swap for DB backend later)

3. Update engine/template-engine.ts:
   - Accept optional auditLog: AuditLog in constructor
   - Log 'executed' entry on each template execution (templateId, userId, params hash, rowCount)
   - Log 'updated' entry when customize() is called

4. Add __tests__/template-diff.test.ts:
   - Test diff detects SQL changes
   - Test diff detects parameter additions/removals
   - Test no-change case returns empty changedFields
   - Test audit log records entries and retrieves history
```

## Acceptance Criteria
- [ ] `diffTemplates()` function produces accurate diffs
- [ ] `AuditLog` class stores and retrieves entries
- [ ] TemplateEngine logs executions and customizations
- [ ] Tests pass for diff and audit log
- [ ] Audit log export returns all entries (for compliance reporting)
