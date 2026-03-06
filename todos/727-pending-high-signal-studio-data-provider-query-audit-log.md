# TODO 727: Query Audit Log

**Repo:** signal-studio-data-provider  
**Priority:** HIGH  
**Effort:** S (1 day)  
**Dependencies:** None (optional Redis for persistence)

## Description
Every query execution must be logged for compliance (SOC2, FINRA). Implement a `QueryAuditMiddleware` wrapper in `factory.py` that intercepts all provider calls and appends to an audit log.

## Acceptance Criteria
- [ ] Every `execute_query` call logs: org_id, sql_hash, timestamp, row_count, execution_time_ms, cost
- [ ] Raw SQL is never logged (only sha256 hash) for privacy
- [ ] Audit log appends to JSONL file at configurable path (default: `~/.signal-studio/audit.jsonl`)
- [ ] Optional: async write to Supabase `signal_audit_log` table
- [ ] `AuditEntry` is a pydantic model with all required fields
- [ ] Tests verify logging behavior

## Coding Prompt
```python
# Create providers/audit_middleware.py
import hashlib, json, time
from datetime import datetime, timezone
from pathlib import Path
from pydantic import BaseModel

class AuditEntry(BaseModel):
    org_id: str
    sql_hash: str  # sha256 of raw SQL
    timestamp: str
    row_count: int
    execution_time_ms: float
    cost: float = 0.0

class AuditedProvider:
    """Wraps any DataProvider to add audit logging."""
    def __init__(self, provider: DataProvider, org_id: str, audit_path: Path):
        self._provider = provider
        self._org_id = org_id
        self._audit_path = audit_path

    async def execute_query(self, sql, params=None):
        start = time.monotonic()
        result = await self._provider.execute_query(sql, params)
        elapsed = (time.monotonic() - start) * 1000
        entry = AuditEntry(
            org_id=self._org_id,
            sql_hash=hashlib.sha256(sql.encode()).hexdigest(),
            timestamp=datetime.now(timezone.utc).isoformat(),
            row_count=result.row_count,
            execution_time_ms=elapsed,
            cost=result.cost,
        )
        with open(self._audit_path, "a") as f:
            f.write(entry.model_dump_json() + "\n")
        return result
    
    def __getattr__(self, name):
        return getattr(self._provider, name)

# In factory.py, wrap provider before returning:
if org_config.audit_enabled:
    provider = AuditedProvider(provider, org_config.org_id, audit_path)
```
