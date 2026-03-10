# TODO-828: CSV/Excel Export Endpoints for Signal Results

**Repo:** signal-builder-backend  
**Priority:** MEDIUM  
**Effort:** S (1 day)  
**Status:** pending

## Problem

Signal result data is only accessible via JSON API. Enterprise clients (Invesco) need downloadable CSV/Excel reports for further analysis in Excel/BI tools. `openpyxl` is already in Pipfile but unused.

## Solution

Add export endpoints:
- `GET /v1/signals/{id}/results/export?format=csv`
- `GET /v1/signals/{id}/results/export?format=xlsx`

Stream response for large datasets.

## Coding Prompt

```python
# In apps/signals/routers/signal_router.py (or new routers/export.py):

from fastapi.responses import StreamingResponse
import csv, io
import openpyxl

@router.get("/{signal_id}/results/export")
async def export_signal_results(
    signal_id: str,
    format: Literal["csv", "xlsx"] = "csv",
    current_user: User = Depends(get_current_user),
    signal_cases: SignalCases = Depends(get_signal_cases),
):
    # 1. Get latest signal_run result for this signal
    # 2. Get result data (rows + columns)
    # 3. If format == "csv": return StreamingResponse with csv.writer
    # 4. If format == "xlsx": create openpyxl Workbook, stream as bytes

    if format == "csv":
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(columns)
        for row in rows:
            writer.writerow(row)
        output.seek(0)
        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename=signal_{signal_id}.csv"}
        )
    elif format == "xlsx":
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(columns)
        for row in rows:
            ws.append(row)
        output = io.BytesIO()
        wb.save(output)
        output.seek(0)
        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename=signal_{signal_id}.xlsx"}
        )
```

## Acceptance Criteria
- `GET /v1/signals/{id}/results/export?format=csv` returns valid CSV with Content-Disposition header
- `GET /v1/signals/{id}/results/export?format=xlsx` returns valid Excel file
- Org scoping enforced (can't export another org's signal)
- Empty result set handled gracefully (return headers-only CSV/xlsx)
- Tests: `tests/test_signal_export.py`
