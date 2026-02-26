---
status: pending
priority: medium
issue_id: "014"
tags: [signal-builder-backend, performance, database, postgresql, indexes, alembic]
dependencies: []
---

# TODO 014 — Database Index Optimization

**Status:** pending  
**Priority:** medium  
**Repo:** signal-builder-backend  
**Effort:** M (1-2 days)

## Problem Statement

As the signals dataset grows (more orgs, more signals, more signal nodes), query performance degrades without proper indexes. The PostgreSQL tables for signals, signal nodes, and user/org lookups likely lack composite indexes on the most common query patterns.

Key query patterns without known indexes:
- Signal lookup by `org_id` + `signal_id` (most common read)
- Signal nodes fetched by `signal_id` (tree assembly)
- User lookup by `email` in auth (login path)
- Analytical DB sync queries filtered by `org_id` + `updated_at`

## Findings

- `db/` directory contains Alembic migrations
- `apps/signals/models/`, `apps/users/models/`, `apps/analytical_db/` have SQLAlchemy models
- SQLAlchemy 2.0 supports `Index()` declarations in model definitions
- No evidence of composite indexes in the current model files

## Proposed Solutions

### Option A: Add Indexes via Alembic Migration (Recommended)
Audit all models, identify missing indexes, create a single Alembic migration.

**Pros:** Tracked in version control, applied automatically on deploy  
**Cons:** Must be careful not to lock tables during migration on large datasets

### Option B: CONCURRENTLY via raw SQL scripts
Run `CREATE INDEX CONCURRENTLY` outside of Alembic to avoid table locks.

**Pros:** No table lock  
**Cons:** Not tracked in Alembic history, manual process

**Recommendation:** Option A for new indexes + CONCURRENTLY flag on production deployment.

## Coding Prompt

```
You are optimizing database indexes for signal-builder-backend.

Repository: /data/workspace/projects/signal-builder-backend/
Stack: SQLAlchemy 2.0, Alembic, PostgreSQL

TASK: Audit models and add missing indexes via Alembic migration.

1. Read ALL model files:
   - apps/signals/models/
   - apps/users/models/
   - apps/analytical_db/ (schema_manager, db_config, db_resources)
   - Any other model files under apps/

2. For each model, identify:
   - Columns used in WHERE clauses (foreign keys, status fields, timestamps)
   - Columns used in ORDER BY (created_at, updated_at)
   - Columns used in JOIN conditions
   - Columns with uniqueness constraints that should be unique indexes

3. Add Index declarations to SQLAlchemy models:
   - Single column: Column("org_id", Integer, index=True)
   - Composite: Index("ix_signals_org_id_created_at", "org_id", "created_at")
   - Unique: UniqueConstraint("email", name="uq_users_email")

   Priority indexes to add:
   a) signals table:
      - Index on (org_id) — filter by tenant
      - Index on (org_id, created_at DESC) — list by tenant, sorted
      - Index on (org_id, status) if status column exists
   
   b) signal_nodes (or similar) table:
      - Index on (signal_id) — tree assembly
      - Index on (signal_id, node_type) if applicable
   
   c) users table:
      - Unique index on (email) — login lookup
      - Index on (org_id) — list users by org
   
   d) Any tables with updated_at column used in sync:
      - Index on (org_id, updated_at) — analytical DB sync delta queries

4. Generate Alembic migration:
   cd /data/workspace/projects/signal-builder-backend
   pipenv run alembic revision --autogenerate -m "add_performance_indexes"

5. Review generated migration in db/versions/:
   - Verify all expected op.create_index() calls are present
   - Add postgresql_concurrently=True to each create_index call for production safety:
     op.create_index("ix_signals_org_id", "signals", ["org_id"],
                     postgresql_concurrently=True)
   - Add op.execute("SET lock_timeout = '5s'") at the top of upgrade()

6. Test the migration:
   pipenv run alembic upgrade head
   pipenv run alembic downgrade -1  # verify rollback works

7. Add EXPLAIN ANALYZE output for 3 key queries to document baseline performance:
   - Signal list by org
   - Signal node tree fetch
   - User login lookup
   Save to: db/index_analysis.md

8. Update existing model files to declare indexes inline (SQLAlchemy best practice):
   __table_args__ = (
       Index("ix_signals_org_created", "org_id", "created_at"),
   )

Constraints:
- Use CONCURRENTLY for all new indexes to avoid table locks in production
- Do NOT drop existing indexes
- Test migration both upgrade and downgrade
- Document estimated query improvement in migration comment
- If a table has >1M rows, note in migration comment: requires maintenance window
```

## Acceptance Criteria

- [ ] All model files audited for missing indexes
- [ ] Alembic migration created with all new indexes
- [ ] Indexes use `postgresql_concurrently=True`
- [ ] Migration `upgrade` and `downgrade` both succeed cleanly
- [ ] `email` column on users table has unique index
- [ ] Signal queries by `org_id` have supporting index
- [ ] Signal node tree assembly by `signal_id` has supporting index
- [ ] Analytical DB sync delta queries by `(org_id, updated_at)` indexed
- [ ] `db/index_analysis.md` documents before/after EXPLAIN ANALYZE
- [ ] No existing indexes are dropped

## Dependencies

None — can execute independently.

## Work Log

### 2026-02-26 - Todo Created

**By:** Planning Agent

**Actions:**
- Identified likely missing composite indexes from code review
- Recommended CONCURRENTLY approach for production safety
- Scoped to most impactful query patterns: tenant reads, tree assembly, auth

**Learnings:**
- Alembic autogenerate may miss Index() declarations if models aren't updated first
- Must add indexes to model __table_args__ AND generate migration
