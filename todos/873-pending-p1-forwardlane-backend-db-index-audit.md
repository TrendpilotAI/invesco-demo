# FL-029: Database Index Audit

**Repo:** forwardlane-backend  
**Priority:** P1  
**Effort:** S-M (1-2 days)  
**Status:** pending

## Task Description
Enable `pg_stat_statements` on production PostgreSQL, identify the 20 slowest queries, run `EXPLAIN ANALYZE` on each, and add missing indexes via Django migrations. Expected impact: 2-10x query speedup on ranking and market data endpoints.

## Problem
No database index audit has been performed. With Invesco using the system actively, slow queries directly impact their experience. Key tables (`client_ranking_*`, `market_data_*`, `entities_*`) likely have missing composite indexes on common filter patterns (tenant+date, ticker+date).

## Coding Prompt
```
STEP 1 — Enable pg_stat_statements (run on Railway PostgreSQL):
```sql
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
```
Add to DATABASE_URL environment or run via psql on Railway.

STEP 2 — Create diagnostic migration (safe, no schema changes):
In /data/workspace/projects/forwardlane-backend/:
Create management command core/management/commands/db_index_audit.py:
```python
from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Run database index audit'
    
    def handle(self, *args, **kwargs):
        with connection.cursor() as cursor:
            # Find tables with high seq scans
            cursor.execute("""
                SELECT relname, seq_scan, idx_scan,
                       n_live_tup as row_count
                FROM pg_stat_user_tables 
                WHERE seq_scan > 100
                ORDER BY seq_scan DESC 
                LIMIT 20;
            """)
            tables = cursor.fetchall()
            
            # Find slow queries
            cursor.execute("""
                SELECT query, calls, 
                       total_exec_time/calls as avg_ms,
                       rows/calls as avg_rows
                FROM pg_stat_statements 
                WHERE calls > 50
                ORDER BY avg_ms DESC 
                LIMIT 20;
            """)
            queries = cursor.fetchall()
        
        # Write report to AUDIT_INDEXES.md
```

STEP 3 — Based on audit findings, add indexes:
Likely candidates (create migration after running audit):
```python
# client_ranking — filter by tenant + date
class Migration(migrations.Migration):
    operations = [
        migrations.AddIndex(
            model_name='clientranking',
            index=models.Index(fields=['tenant_id', 'created_at'], name='cr_tenant_date_idx'),
        ),
        # market_data — filter by ticker + date
        migrations.AddIndex(
            model_name='marketdata', 
            index=models.Index(fields=['ticker', 'data_date'], name='md_ticker_date_idx'),
        ),
    ]
```

STEP 4 — Write AUDIT_INDEXES.md in repo root with:
- List of identified slow queries
- Tables with high seq_scan counts
- Indexes added
- Before/after performance comparison (if measurable)

Files to create:
- core/management/commands/db_index_audit.py (new)
- Various app migrations for missing indexes
- AUDIT_INDEXES.md (new)
```

## Acceptance Criteria
- [ ] `db_index_audit` management command runs and produces report
- [ ] Top 20 slowest queries identified and documented
- [ ] At least 3-5 missing indexes identified and added via migrations
- [ ] AUDIT_INDEXES.md committed to repo
- [ ] Migration runs cleanly (`migrate --check` passes)

## Dependencies
- FL-025 (migration CI check) — run after index migrations added.
