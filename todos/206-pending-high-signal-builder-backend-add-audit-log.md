# TODO 206 — Add Audit Log (HIGH)

**Project:** signal-builder-backend  
**Priority:** HIGH  
**Estimated Effort:** 8 hours  
**Status:** pending  
**Dependencies:** 200, 201, 203 (security baseline must be in place; audit log records who did what)

---

## Task Description

Financial services customers require an immutable audit trail of all system actions. Currently the signal-builder-backend has no audit logging — there is no record of who created, modified, published, or deleted signals, or who triggered schema syncs.

**Add an append-only `audit_events` table and middleware/decorator pattern** that:
1. Records every mutation (create/update/delete/publish/sync) with actor, timestamp, entity, and diff
2. Is queryable via `GET /audit-log` (admin only) with filtering
3. Is non-blocking — audit writes should not fail user requests
4. Is tamper-evident — no UPDATE or DELETE on audit_events rows

---

## Coding Prompt (Autonomous Agent)

```
TASK: Implement append-only audit log in signal-builder-backend

REPO: /data/workspace/projects/signal-builder-backend/

ARCHITECTURE:
- Alembic migration: `audit_events` table
- SQLAlchemy model: `AuditEvent` (append-only, no update/delete)
- Service: `AuditLogService` with async `log()` method
- Middleware or decorator: auto-capture mutations on key endpoints
- Admin router: `GET /audit-log` with filtering
- Dependency injection wiring

STEPS:

1. CREATE ALEMBIC MIGRATION
   File: `alembic/versions/{timestamp}_add_audit_events_table.py`
   
   ```python
   def upgrade():
       op.create_table(
           'audit_events',
           sa.Column('id', sa.BigInteger(), nullable=False, autoincrement=True),
           sa.Column('event_type', sa.String(100), nullable=False),
           # Entity info
           sa.Column('entity_type', sa.String(100), nullable=False),  # 'signal', 'signal_node', 'org_schema', etc.
           sa.Column('entity_id', sa.String(255), nullable=True),     # string to handle various ID types
           # Actor info
           sa.Column('actor_user_id', sa.Integer(), nullable=True),   # null for system actions
           sa.Column('actor_ip', sa.String(50), nullable=True),
           sa.Column('actor_user_agent', sa.String(500), nullable=True),
           # Change data
           sa.Column('before_state', sa.JSON(), nullable=True),       # state before change
           sa.Column('after_state', sa.JSON(), nullable=True),        # state after change
           sa.Column('metadata', sa.JSON(), nullable=True),           # extra context (org_id, etc.)
           # Timestamps
           sa.Column('occurred_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
           sa.PrimaryKeyConstraint('id'),
       )
       # Indexes for common query patterns
       op.create_index('ix_audit_entity', 'audit_events', ['entity_type', 'entity_id'])
       op.create_index('ix_audit_actor', 'audit_events', ['actor_user_id'])
       op.create_index('ix_audit_occurred_at', 'audit_events', ['occurred_at'])
       op.create_index('ix_audit_event_type', 'audit_events', ['event_type'])
   
   def downgrade():
       op.drop_table('audit_events')
   ```

2. CREATE SQLALCHEMY MODEL
   File: `apps/audit/models/audit_event.py`
   
   ```python
   from sqlalchemy import Column, BigInteger, String, Integer, JSON, DateTime
   from sqlalchemy.sql import func
   from core.database import Base
   
   class AuditEvent(Base):
       __tablename__ = "audit_events"
       
       id = Column(BigInteger, primary_key=True, autoincrement=True)
       event_type = Column(String(100), nullable=False)
       entity_type = Column(String(100), nullable=False)
       entity_id = Column(String(255), nullable=True)
       actor_user_id = Column(Integer, nullable=True)
       actor_ip = Column(String(50), nullable=True)
       actor_user_agent = Column(String(500), nullable=True)
       before_state = Column(JSON, nullable=True)
       after_state = Column(JSON, nullable=True)
       metadata_ = Column("metadata", JSON, nullable=True)
       occurred_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
       
       # Prevent modification — override __init__ to make this obvious
       def __init_subclass__(cls, **kwargs):
           super().__init_subclass__(**kwargs)
       
       class Config:
           # Enforce immutability at application level
           allow_mutation = False
   ```

3. CREATE AUDIT EVENT TYPES ENUM
   File: `apps/audit/audit_event_types.py`
   
   ```python
   from enum import Enum
   
   class AuditEventType(str, Enum):
       # Signal lifecycle
       SIGNAL_CREATED = "signal.created"
       SIGNAL_UPDATED = "signal.updated"
       SIGNAL_DELETED = "signal.deleted"
       SIGNAL_PUBLISHED = "signal.published"
       SIGNAL_UNPUBLISHED = "signal.unpublished"
       SIGNAL_ROLLED_BACK = "signal.rolled_back"
       
       # Signal nodes
       NODE_ADDED = "signal_node.added"
       NODE_UPDATED = "signal_node.updated"
       NODE_DELETED = "signal_node.deleted"
       
       # Schema / DB sync
       SCHEMA_SYNC_TRIGGERED = "schema.sync_triggered"
       SCHEMA_SYNC_COMPLETED = "schema.sync_completed"
       SCHEMA_SYNC_FAILED = "schema.sync_failed"
       
       # Auth
       USER_LOGIN = "auth.login"
       USER_LOGOUT = "auth.logout"
       USER_LOGIN_FAILED = "auth.login_failed"
       
       # Admin
       ADMIN_ACTION = "admin.action"
   ```

4. CREATE AUDIT LOG SERVICE
   File: `apps/audit/audit_log_service.py`
   
   ```python
   import asyncio
   import logging
   from typing import Any
   
   logger = logging.getLogger(__name__)
   
   class AuditLogService:
       """
       Append-only audit log writer.
       Uses fire-and-forget to avoid blocking request handlers.
       Falls back to stderr logging if DB write fails.
       """
       
       def __init__(self, session_factory):
           self.session_factory = session_factory
       
       async def log(
           self,
           event_type: str,
           entity_type: str,
           entity_id: str | int | None = None,
           actor_user_id: int | None = None,
           actor_ip: str | None = None,
           actor_user_agent: str | None = None,
           before_state: dict | None = None,
           after_state: dict | None = None,
           metadata: dict | None = None,
       ) -> None:
           """Write audit event. Non-blocking — failure is logged but not raised."""
           try:
               async with self.session_factory() as session:
                   async with session.begin():
                       event = AuditEvent(
                           event_type=event_type,
                           entity_type=entity_type,
                           entity_id=str(entity_id) if entity_id is not None else None,
                           actor_user_id=actor_user_id,
                           actor_ip=actor_ip,
                           actor_user_agent=actor_user_agent,
                           before_state=before_state,
                           after_state=after_state,
                           metadata_=metadata,
                       )
                       session.add(event)
           except Exception as e:
               # Audit failure must NEVER block the main request
               logger.error(f"AUDIT_WRITE_FAILED event_type={event_type} entity={entity_type}:{entity_id} error={e}")
       
       def log_fire_and_forget(self, *args, **kwargs) -> None:
           """Schedule audit log write without awaiting it."""
           asyncio.create_task(self.log(*args, **kwargs))
   ```

5. INTEGRATE INTO EXISTING CASES CLASSES
   Find the publish flow, create flow, update flow, and delete flow for signals.
   In each, inject `AuditLogService` and add audit calls:
   
   Example in `PublishSignalCases`:
   ```python
   # After successful publish:
   await self.audit_log.log(
       event_type=AuditEventType.SIGNAL_PUBLISHED,
       entity_type="signal",
       entity_id=signal.id,
       actor_user_id=user_id,
       actor_ip=request_context.ip,
       before_state={"status": previous_status},
       after_state={"status": "published", "version": new_version_num},
       metadata={"org_id": signal.org_id},
   )
   ```
   
   Example in `CreateSignalCases`:
   ```python
   await self.audit_log.log(
       event_type=AuditEventType.SIGNAL_CREATED,
       entity_type="signal",
       entity_id=new_signal.id,
       actor_user_id=user_id,
       after_state={"name": new_signal.name, "org_id": new_signal.org_id},
   )
   ```

6. CREATE FASTAPI MIDDLEWARE for request context
   File: `apps/audit/audit_middleware.py`
   
   ```python
   from fastapi import Request
   from starlette.middleware.base import BaseHTTPMiddleware
   import contextvars
   
   _request_context: contextvars.ContextVar[dict] = contextvars.ContextVar("request_context", default={})
   
   class AuditContextMiddleware(BaseHTTPMiddleware):
       async def dispatch(self, request: Request, call_next):
           ctx = {
               "ip": request.client.host if request.client else None,
               "user_agent": request.headers.get("user-agent", "")[:500],
               "path": request.url.path,
               "method": request.method,
           }
           _request_context.set(ctx)
           return await call_next(request)
   
   def get_request_context() -> dict:
       return _request_context.get({})
   ```
   
   Register middleware in `get_application.py`.

7. CREATE ADMIN QUERY ENDPOINT
   File: `apps/audit/routers/audit_log_router.py`
   
   ```python
   @router.get("/audit-log", response_model=AuditLogListOut)
   async def get_audit_log(
       entity_type: str | None = None,
       entity_id: str | None = None,
       event_type: str | None = None,
       actor_user_id: int | None = None,
       from_date: datetime | None = None,
       to_date: datetime | None = None,
       limit: int = Query(default=50, le=500),
       offset: int = 0,
       current_user=Depends(require_admin),  # admin-only
   ):
       """Query audit log. Admin access required."""
       ...
   ```

8. WRITE TESTS
   `tests/test_audit_log.py`:
   - Test: signal creation generates SIGNAL_CREATED event
   - Test: signal publish generates SIGNAL_PUBLISHED event with before/after state
   - Test: audit write failure does NOT raise exception in caller
   - Test: GET /audit-log returns 403 for non-admin user
   - Test: GET /audit-log filtering by entity_type works
   - Test: GET /audit-log filtering by date range works
   - Test: audit events are NOT deletable or updateable via API
   - Test: audit events are immutable in DB (no UPDATE succeeds)

9. Commit: "feat: add append-only audit log with middleware context capture and admin query endpoint"

VERIFICATION:
- `alembic upgrade head` succeeds
- Create a signal → GET /audit-log shows SIGNAL_CREATED event
- Publish a signal → GET /audit-log shows SIGNAL_PUBLISHED event with diff
- Non-admin GET /audit-log → 403
- DB: `UPDATE audit_events SET event_type='tampered'` — add DB trigger to prevent this (optional)
- All 8+ tests pass
```

---

## Dependencies

- **200** — CORS fix (stable deployment base)
- **201** — JWT secrets fix (audit log records authenticated users — needs proper auth)
- **203** — Pinned dependencies (stable build)

## Acceptance Criteria

- [ ] `audit_events` table exists with correct schema
- [ ] All signal mutations (create/update/delete/publish) generate audit events
- [ ] Audit write failures are logged but do NOT fail the originating request
- [ ] `GET /audit-log` endpoint exists (admin-only, 403 for regular users)
- [ ] Filtering by entity_type, event_type, actor, date range works
- [ ] Request IP and user-agent captured via middleware
- [ ] All 8+ tests pass
- [ ] Performance: audit writes are async and non-blocking (fire-and-forget)
- [ ] Committed and pushed
