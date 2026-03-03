# TODO 455 — forwardlane_advisor: N+1 Query Audit & Performance Fixes

**Priority:** P1 | **Effort:** M | **Repo:** forwardlane_advisor

## Description
Sequelize v3 models likely have N+1 query issues in portfolio, client, and recommendation views. Audit and fix with eager loading.

## Full Coding Prompt
```
Audit and fix N+1 query problems in forwardlane_advisor.

1. Add query logging to identify N+1 patterns:
   - Enable Sequelize logging with query counter
   - Test portfolio listing endpoint, client dashboard, recommendation views

2. Key areas to audit:
   - app/portfolios/ — portfolio with positions (portfolio_daily_price)
   - app/clients/ — client with segments and recommendations
   - app/recomendation/ — recommendations with portfolios and instruments
   - app/instruments/ — instruments with universe_instruments

3. Fix patterns:
   - Add `include: [...]` for eager loading associated models
   - Use `findAll` with proper `include` instead of sequential findById calls
   - Add `.limit()` and `.offset()` where missing (prevent full table scans)

4. Add database indexes:
   - Review seq_migrations/ for missing indexes
   - Add composite indexes on (client_id, created_at) for recommendations
   - Add index on portfolio_daily_price (portfolio_id, date)

5. Add caching for expensive queries:
   - Top equity indices (currently polled every 10s in app.js)
   - Add in-memory cache with 30s TTL for market data

6. Performance test: measure response times before/after
```

## Acceptance Criteria
- [ ] Portfolio listing responds in <200ms
- [ ] No N+1 queries on main dashboard
- [ ] Pagination applied to all list endpoints
- [ ] Market data cached appropriately

## Dependencies
- TODO 451

## Estimated Effort
3-4 days
