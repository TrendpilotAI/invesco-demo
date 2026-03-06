# TODO 730: Schema Diff & Change Event Emission

**Repo:** signal-studio-data-provider  
**Priority:** MEDIUM  
**Effort:** M (1-2 days)  
**Dependencies:** TODO 593 (Redis cache, optional)

## Description
When `SchemaRegistry.refresh()` detects changes vs cached schema, emit structured `SchemaChangeEvent` objects. Publish to configurable destinations: in-memory callback, Redis pub/sub, or webhook URL.

## Acceptance Criteria
- [ ] `SchemaChangeEvent` pydantic model: event_type (table_added/dropped/column_added/removed/type_changed), org_id, table_name, detail
- [ ] `SchemaRegistry.refresh()` diffs old vs new schema and yields change events
- [ ] `OrgConfig.schema_change_webhook: str | None` — POST events to this URL
- [ ] Optional `on_schema_change: Callable[[SchemaChangeEvent], Awaitable[None]]` callback
- [ ] Tests verify diff detection for all change types

## Coding Prompt
```python
# schema/events.py
from pydantic import BaseModel
from typing import Literal

SchemaChangeType = Literal["table_added","table_dropped","column_added","column_removed","type_changed"]

class SchemaChangeEvent(BaseModel):
    org_id: str
    event_type: SchemaChangeType
    table_name: str
    column_name: str | None = None
    old_value: str | None = None
    new_value: str | None = None
    detected_at: str

# schema/registry.py additions:
def _diff_schemas(self, old: SchemaInfo, new: SchemaInfo) -> list[SchemaChangeEvent]:
    events = []
    old_tables = {t.name: t for t in old.tables}
    new_tables = {t.name: t for t in new.tables}
    
    for name in new_tables - old_tables.keys():
        events.append(SchemaChangeEvent(org_id=old.org_id, event_type="table_added", table_name=name, ...))
    for name in old_tables - new_tables.keys():
        events.append(SchemaChangeEvent(org_id=old.org_id, event_type="table_dropped", table_name=name, ...))
    # column-level diffs...
    return events

async def refresh(self, org_id: str) -> list[SchemaChangeEvent]:
    old = self._cache.get(org_id)
    new = await self._provider.get_schema(org_id)
    self._cache[org_id] = new
    
    events = self._diff_schemas(old, new) if old else []
    if events and self._webhook_url:
        await self._post_webhook(events)
    if events and self._on_change:
        for e in events:
            await self._on_change(e)
    return events
```
