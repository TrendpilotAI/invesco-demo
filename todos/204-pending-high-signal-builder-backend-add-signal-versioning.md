# TODO 204 — Add Signal Versioning / Snapshot History (HIGH)

**Project:** signal-builder-backend  
**Priority:** HIGH  
**Estimated Effort:** 8 hours  
**Status:** pending  
**Dependencies:** 200, 201, 202, 203 (requires security fixes first; deploy to stable base)

---

## Task Description

Every time a signal is published, the system should snapshot the node tree + generated SQL as an immutable version record. This enables:

- **Rollback** — revert to a previous working signal definition
- **Diff** — see what changed between versions
- **Audit trail** — compliance requirement for financial services
- **A/B testing** — compare signal performance across versions
- **Enterprise sales** — "we version everything" is a key differentiator

**Current state:** Signals can be edited and published multiple times with no history preserved.  
**Desired state:** Each publish creates a version record; all previous versions are queryable.

---

## Coding Prompt (Autonomous Agent)

```
TASK: Implement signal versioning with snapshot history in signal-builder-backend

REPO: /data/workspace/projects/signal-builder-backend/

ARCHITECTURE:
- New Alembic migration: `signal_versions` table
- New SQLAlchemy model: `SignalVersion`
- New storage class: `SignalVersionStorage`
- New cases class: `SignalVersionCases`
- New router: `signal_versions_router` mounted at `/signals/{signal_id}/versions`
- Hook into existing publish flow to create a version on each publish

STEPS:

1. CREATE ALEMBIC MIGRATION
   File: `alembic/versions/{timestamp}_add_signal_versions_table.py`
   
   ```python
   def upgrade():
       op.create_table(
           'signal_versions',
           sa.Column('id', sa.Integer(), nullable=False),
           sa.Column('signal_id', sa.Integer(), sa.ForeignKey('signals.id', ondelete='CASCADE'), nullable=False),
           sa.Column('version_num', sa.Integer(), nullable=False),
           sa.Column('node_tree_json', sa.JSON(), nullable=False),
           sa.Column('generated_sql', sa.Text(), nullable=True),
           sa.Column('published_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
           sa.Column('published_by_user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=True),
           sa.Column('label', sa.String(255), nullable=True),  # optional user-provided label
           sa.Column('is_active', sa.Boolean(), nullable=False, server_default='false'),
           sa.PrimaryKeyConstraint('id'),
           sa.UniqueConstraint('signal_id', 'version_num', name='uq_signal_version'),
       )
       op.create_index('ix_signal_versions_signal_id', 'signal_versions', ['signal_id'])
   
   def downgrade():
       op.drop_table('signal_versions')
   ```

2. CREATE SQLALCHEMY MODEL
   File: `apps/signals/models/signal_version.py`
   
   ```python
   from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON
   from sqlalchemy.orm import relationship
   from sqlalchemy.sql import func
   from core.database import Base
   
   class SignalVersion(Base):
       __tablename__ = "signal_versions"
       
       id = Column(Integer, primary_key=True)
       signal_id = Column(Integer, ForeignKey("signals.id", ondelete="CASCADE"), nullable=False, index=True)
       version_num = Column(Integer, nullable=False)
       node_tree_json = Column(JSON, nullable=False)
       generated_sql = Column(Text, nullable=True)
       published_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
       published_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
       label = Column(String(255), nullable=True)
       is_active = Column(Boolean, nullable=False, default=False)
       
       signal = relationship("Signal", back_populates="versions")
       published_by = relationship("User", foreign_keys=[published_by_user_id])
   ```
   
   Update `Signal` model to add:
   ```python
   versions = relationship("SignalVersion", back_populates="signal", order_by="SignalVersion.version_num.desc()")
   ```

3. CREATE PYDANTIC SCHEMAS
   File: `apps/signals/schemas/signal_version_schemas.py`
   
   ```python
   from pydantic import BaseModel
   from datetime import datetime
   from typing import Optional, Any
   
   class SignalVersionOut(BaseModel):
       id: int
       signal_id: int
       version_num: int
       node_tree_json: dict[str, Any]
       generated_sql: Optional[str]
       published_at: datetime
       published_by_user_id: Optional[int]
       label: Optional[str]
       is_active: bool
       
       class Config:
           from_attributes = True
   
   class SignalVersionListOut(BaseModel):
       versions: list[SignalVersionOut]
       total: int
   
   class RollbackRequest(BaseModel):
       label: Optional[str] = None  # optional label for the new version created on rollback
   ```

4. CREATE STORAGE CLASS
   File: `apps/signals/storages/signal_version_storage.py`
   
   ```python
   class SignalVersionStorage:
       def __init__(self, session: AsyncSession):
           self.session = session
       
       async def create_version(self, signal_id: int, node_tree: dict, sql: str | None,
                                 user_id: int | None, label: str | None = None) -> SignalVersion:
           # Get next version number
           result = await self.session.execute(
               select(func.max(SignalVersion.version_num)).where(SignalVersion.signal_id == signal_id)
           )
           max_version = result.scalar() or 0
           
           # Deactivate all previous versions
           await self.session.execute(
               update(SignalVersion)
               .where(SignalVersion.signal_id == signal_id)
               .values(is_active=False)
           )
           
           # Create new active version
           version = SignalVersion(
               signal_id=signal_id,
               version_num=max_version + 1,
               node_tree_json=node_tree,
               generated_sql=sql,
               published_by_user_id=user_id,
               label=label,
               is_active=True,
           )
           self.session.add(version)
           await self.session.flush()
           return version
       
       async def list_versions(self, signal_id: int, limit: int = 20, offset: int = 0) -> tuple[list[SignalVersion], int]:
           ...
       
       async def get_version(self, signal_id: int, version_num: int) -> SignalVersion | None:
           ...
       
       async def get_active_version(self, signal_id: int) -> SignalVersion | None:
           ...
   ```

5. HOOK INTO PUBLISH FLOW
   Find where signals are published (look for `publish_signal`, `PublishSignalCases`, or similar).
   After the signal is published and SQL is generated, call:
   ```python
   await signal_version_storage.create_version(
       signal_id=signal.id,
       node_tree=signal.node_tree,  # or however it's structured
       sql=generated_sql,
       user_id=current_user.id,
   )
   ```

6. CREATE API ROUTER
   File: `apps/signals/routers/signal_versions_router.py`
   
   Endpoints:
   - `GET /signals/{signal_id}/versions` — list versions (paginated)
   - `GET /signals/{signal_id}/versions/{version_num}` — get specific version
   - `POST /signals/{signal_id}/rollback/{version_num}` — rollback to version
   - `GET /signals/{signal_id}/versions/diff?from={v1}&to={v2}` — diff two versions (bonus)
   
   ```python
   @router.post("/{signal_id}/rollback/{version_num}", response_model=SignalVersionOut)
   async def rollback_to_version(signal_id: int, version_num: int, current_user=Depends(get_current_user)):
       """Roll back a signal to a previous version. Creates a new version record."""
       version = await signal_version_storage.get_version(signal_id, version_num)
       if not version:
           raise HTTPException(404, "Version not found")
       # Restore the node tree from the version and re-publish
       new_version = await signal_version_storage.create_version(
           signal_id=signal_id,
           node_tree=version.node_tree_json,
           sql=version.generated_sql,
           user_id=current_user.id,
           label=f"Rollback to v{version_num}",
       )
       return new_version
   ```

7. REGISTER ROUTER in main app router registration file.

8. WRITE TESTS
   `tests/test_signal_versioning.py`:
   - Test: publish signal creates version 1
   - Test: re-publish creates version 2, marks version 1 inactive
   - Test: rollback to v1 creates version 3 with same node_tree as v1
   - Test: cannot rollback to non-existent version (404)
   - Test: list versions returns correct count and ordering

9. UPDATE OPENAPI docs with descriptions for all new endpoints.

10. Commit: "feat: add signal versioning with snapshot history and rollback support"

VERIFICATION:
- `alembic upgrade head` succeeds
- All version endpoints return correct HTTP status codes
- Publish flow creates a new version record (check DB after test publish)
- Rollback creates a new version (not destructive)
- All 8+ tests pass
```

---

## Dependencies

- **200** CORS fix (deploy stability)
- **201** JWT secrets fix (deploy stability)  
- **202** SQL injection fix (the versioned SQL must be safe)
- **203** Pinned dependencies (stable build)

## Acceptance Criteria

- [ ] `signal_versions` table exists with correct schema (migration applied)
- [ ] `SignalVersion` SQLAlchemy model with all fields
- [ ] Every signal publish creates a new version record
- [ ] `GET /signals/{id}/versions` returns paginated version history
- [ ] `GET /signals/{id}/versions/{num}` returns specific version with node tree + SQL
- [ ] `POST /signals/{id}/rollback/{num}` restores node tree and creates a new version
- [ ] All 8+ tests pass
- [ ] Rollback is non-destructive (creates new version, doesn't delete history)
- [ ] Committed and pushed
