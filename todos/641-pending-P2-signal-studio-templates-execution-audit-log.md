---
id: 641
status: pending
priority: P2
repo: signal-studio-templates
title: Execution history and compliance audit log
effort: M (2-3 days)
dependencies: [634]
---

# Execution History / Compliance Audit Log

## Problem
Financial firms require audit trails of every query. Currently no execution history is persisted.

## Task
Add execution logging to the template engine and a history API endpoint.

## Coding Prompt
```
In /data/workspace/projects/signal-studio-templates/:

1. Create src/audit/audit-logger.ts:
   interface AuditRecord {
     id: string;           // uuid
     templateId: string;
     templateName: string;
     userId: string;       // JWT sub
     parameters: Record<string, any>;
     rowCount: number;
     executionTimeMs: number;
     timestamp: string;    // ISO8601
     success: boolean;
     errorMessage?: string;
   }
   
   interface AuditStorage {
     log(record: AuditRecord): Promise<void>;
     getHistory(userId: string, limit?: number): Promise<AuditRecord[]>;
   }
   
   class InMemoryAuditStorage implements AuditStorage (for development/testing)
   class PostgresAuditStorage implements AuditStorage (for production — requires pg connection)

2. Update TemplateEngine.execute() to accept optional auditLogger
   and log every execution (success or failure)

3. Add to api/templates.ts:
   GET /templates/history — returns last 50 executions for authenticated user
   GET /templates/history/:templateId — filtered by template

4. Tests for InMemoryAuditStorage
```

## Acceptance Criteria
- [ ] Every execute() call logs an AuditRecord
- [ ] GET /templates/history returns execution history for authenticated user
- [ ] InMemoryAuditStorage works out of the box (no DB needed)
- [ ] PostgresAuditStorage stubbed with schema + migration SQL
- [ ] `pnpm test` passes
