# TODO 205 — Add Dry-Run Execution Mode (HIGH)

**Project:** signal-builder-backend  
**Priority:** HIGH  
**Estimated Effort:** 6 hours  
**Status:** pending  
**Dependencies:** 202 (SQL injection fix must be in place before adding more SQL execution paths)

---

## Task Description

Currently the signal workflow is: **build → validate → publish**. There is no lightweight "run it and show me 10 rows" step. Users have to fully publish a signal to see if it produces meaningful results, leading to:

- Wasted publishes of broken or nonsensical signals
- Poor UX in Signal Studio (no feedback loop)
- Support burden when users don't understand why their signal produces 0 results

**Add a `POST /signals/{id}/preview` endpoint** that:
1. Takes the current draft node tree (or the published node tree)
2. Translates it to SQL (reusing the existing translation pipeline)
3. Runs the SQL against the analytical DB with `LIMIT {N}` (default 10, max 100)
4. Returns column names + sample rows + total count estimate
5. Does NOT publish the signal or create any side effects

---

## Coding Prompt (Autonomous Agent)

```
TASK: Add dry-run preview endpoint to signal-builder-backend

REPO: /data/workspace/projects/signal-builder-backend/

ENDPOINT: POST /signals/{signal_id}/preview
DESCRIPTION: Execute signal SQL with a row limit and return sample results — no publish, no side effects.

STEPS:

1. UNDERSTAND EXISTING TRANSLATION PIPELINE
   Read and understand:
   - How `validate_signal` works (the existing validation endpoint)
   - How SQL is generated: trace `transform_signal_nodes_to_sql` or equivalent
   - How `AnalyticalDBStorage` or `ClientSignalResultStorage` executes queries
   - Where the analytical DB session is injected

2. CREATE PYDANTIC SCHEMAS
   File: `apps/signals/schemas/signal_preview_schemas.py`
   
   ```python
   from pydantic import BaseModel, Field
   from typing import Any, Optional
   
   class PreviewRequest(BaseModel):
       limit: int = Field(default=10, ge=1, le=100, description="Max rows to return (1-100)")
       node_tree: Optional[dict[str, Any]] = Field(
           default=None,
           description="Optional: override with a specific node tree to preview (for unsaved drafts)"
       )
   
   class PreviewColumn(BaseModel):
       name: str
       type: str  # e.g., "integer", "text", "numeric", "timestamp"
   
   class PreviewResult(BaseModel):
       signal_id: int
       sql: str  # the generated SQL (useful for debugging)
       columns: list[PreviewColumn]
       rows: list[dict[str, Any]]  # list of {column_name: value} dicts
       row_count: int  # actual rows returned
       estimated_total: Optional[int]  # COUNT(*) estimate if feasible
       execution_time_ms: float
       is_truncated: bool  # True if there are more rows than the limit
       warnings: list[str]  # e.g., "Signal has no filters — may return all rows"
   ```

3. CREATE CASES CLASS
   File: `apps/signals/features/signal_preview/signal_preview_cases.py`
   
   ```python
   import time
   from typing import Any
   from core.shared.sql_validator import validate_select_only, SQLValidationError
   
   class SignalPreviewCases:
       def __init__(
           self,
           signal_storage,          # to load the signal + node tree
           sql_translator,          # existing translation service
           analytical_db_session,   # read-only session to analytical DB
       ):
           self.signal_storage = signal_storage
           self.sql_translator = sql_translator
           self.analytical_db_session = analytical_db_session
       
       async def preview_signal(
           self,
           signal_id: int,
           user_id: int,
           org_id: int,
           limit: int = 10,
           node_tree_override: dict | None = None,
       ) -> PreviewResult:
           # 1. Load signal (verify ownership)
           signal = await self.signal_storage.get_by_id(signal_id)
           if not signal or signal.org_id != org_id:
               raise NotFoundError(f"Signal {signal_id} not found")
           
           # 2. Get node tree (use override if provided, else current signal state)
           node_tree = node_tree_override or signal.node_tree
           
           # 3. Translate to SQL using existing pipeline
           try:
               base_sql, metadata = await self.sql_translator.translate(node_tree)
           except TranslationError as e:
               raise PreviewError(f"Cannot generate SQL from signal nodes: {e}")
           
           # 4. Safety check
           try:
               validate_select_only(base_sql)
           except SQLValidationError as e:
               raise PreviewError(f"Generated SQL failed safety check: {e}")
           
           # 5. Add LIMIT to the SQL
           # Wrap in subquery to safely add LIMIT without breaking ORDER BY
           limited_sql = f"SELECT * FROM ({base_sql}) _preview_subquery LIMIT {limit}"
           
           # 6. Execute against analytical DB (read-only)
           start = time.monotonic()
           async with self.analytical_db_session.begin():
               await self.analytical_db_session.execute("SET LOCAL statement_timeout = '30s'")
               await self.analytical_db_session.execute("SET LOCAL default_transaction_read_only = true")
               
               result = await self.analytical_db_session.execute(text(limited_sql))
               rows_raw = result.fetchall()
               columns = [{"name": col, "type": "unknown"} for col in result.keys()]
               
               # Try to get estimated total (use EXPLAIN, not COUNT for performance)
               estimated_total = await self._estimate_row_count(base_sql)
           
           elapsed_ms = (time.monotonic() - start) * 1000
           
           # 7. Serialize rows to dicts
           col_names = [c["name"] for c in columns]
           rows = [dict(zip(col_names, row)) for row in rows_raw]
           
           # 8. Build warnings
           warnings = []
           if not node_tree.get("filters"):
               warnings.append("No filters applied — signal may return all rows in the dataset")
           if estimated_total and estimated_total > 10000:
               warnings.append(f"Large result set (~{estimated_total:,} rows) — preview shows first {limit}")
           
           return PreviewResult(
               signal_id=signal_id,
               sql=base_sql,
               columns=columns,
               rows=rows,
               row_count=len(rows),
               estimated_total=estimated_total,
               execution_time_ms=round(elapsed_ms, 2),
               is_truncated=len(rows) >= limit,
               warnings=warnings,
           )
       
       async def _estimate_row_count(self, sql: str) -> int | None:
           """Use EXPLAIN to estimate row count without running COUNT(*)."""
           try:
               result = await self.analytical_db_session.execute(
                   text(f"EXPLAIN (FORMAT JSON) {sql}")
               )
               plan = result.scalar()
               if plan and isinstance(plan, list):
                   return int(plan[0]["Plan"].get("Plan Rows", 0))
           except Exception:
               pass
           return None
   ```

4. CREATE ROUTER ENDPOINT
   File: `apps/signals/routers/signal_preview_router.py`
   
   ```python
   from fastapi import APIRouter, Depends, HTTPException
   from apps.signals.schemas.signal_preview_schemas import PreviewRequest, PreviewResult
   
   router = APIRouter(prefix="/signals", tags=["Signal Preview"])
   
   @router.post("/{signal_id}/preview", response_model=PreviewResult)
   async def preview_signal(
       signal_id: int,
       request: PreviewRequest,
       current_user=Depends(get_current_user),
       preview_cases: SignalPreviewCases = Depends(get_preview_cases),
   ):
       """
       Execute a signal's SQL with a row limit and return sample results.
       Does NOT publish the signal. Safe for use during signal construction.
       """
       try:
           return await preview_cases.preview_signal(
               signal_id=signal_id,
               user_id=current_user.id,
               org_id=current_user.org_id,
               limit=request.limit,
               node_tree_override=request.node_tree,
           )
       except NotFoundError:
           raise HTTPException(404, "Signal not found")
       except PreviewError as e:
           raise HTTPException(422, str(e))
   ```

5. DEPENDENCY INJECTION
   Add `get_preview_cases` to the dependency injection container.
   Wire up: signal_storage, sql_translator (reuse existing), analytical_db_session.

6. REGISTER ROUTER in the main app.

7. RATE LIMITING
   Preview executes real SQL — add rate limit:
   ```python
   from slowapi import Limiter
   @router.post("/{signal_id}/preview")
   @limiter.limit("10/minute")
   async def preview_signal(...):
   ```
   Or use the existing rate limiting mechanism if one exists.

8. WRITE TESTS
   `tests/test_signal_preview.py`:
   - Test: valid signal returns rows + columns + sql
   - Test: limit=5 returns at most 5 rows
   - Test: node_tree_override uses provided tree instead of saved signal
   - Test: signal belonging to different org returns 404
   - Test: signal with broken node tree returns 422 with descriptive error
   - Test: response includes execution_time_ms and is_truncated flag
   - Test: warnings are populated when no filters exist

9. UPDATE OpenAPI documentation for the new endpoint.

10. Commit: "feat: add POST /signals/{id}/preview dry-run execution endpoint"

NOTES:
- The preview endpoint should work on DRAFT signals (not just published ones)
- If the analytical DB isn't set up for the org yet, return a clear 422 error
- Add `X-Signal-Preview: true` header to response to distinguish from actual execution logs

VERIFICATION:
- `curl -X POST /signals/1/preview -d '{"limit": 5}' -H "Authorization: Bearer {token}"`
  returns JSON with columns, rows, sql, execution_time_ms
- Rate limiting works (11th request in 1 minute returns 429)
- All 7+ tests pass
```

---

## Dependencies

- **202** — SQL injection fix (validate_select_only must exist before this)

## Acceptance Criteria

- [ ] `POST /signals/{id}/preview` endpoint exists and is documented in OpenAPI
- [ ] Returns `{ columns, rows, sql, row_count, estimated_total, execution_time_ms, is_truncated, warnings }`
- [ ] `limit` parameter validated: 1–100 range
- [ ] Optional `node_tree` override for previewing unsaved drafts
- [ ] Executes in read-only transaction with 30s statement timeout
- [ ] Rate limited (10 req/min per user)
- [ ] Returns 404 for wrong-org signals
- [ ] Returns 422 for translation errors with descriptive message
- [ ] All 7+ tests pass
- [ ] Committed and pushed
