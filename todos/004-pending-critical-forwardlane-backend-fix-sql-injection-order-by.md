# 004 — Fix SQL Injection in AdvisorListView ORDER BY

**Repo:** forwardlane-backend  
**Priority:** critical  
**Effort:** S (1-2h)  
**Status:** pending

## Description

`easy_button/views.py` — `AdvisorListView.get()` constructs a raw SQL query using Python f-strings for the ORDER BY clause and direction parameter:

```python
order_expr = ordering_map.get(ordering, 'a.aum_current')
direction = request.query_params.get('direction', 'desc').lower()
# ...
ORDER BY {order_expr} {direction} NULLS LAST
```

While `ordering_map` provides some protection, `direction` is only validated with a simple `if direction not in ('asc', 'desc')` check AFTER it's been `.lower()`-ed from untrusted user input. The f-string interpolation into raw SQL is a SQL injection risk. The `order_expr` also comes from a dict but the raw string is still interpolated.

## Coding Prompt

File: `/data/workspace/projects/forwardlane-backend/easy_button/views.py`

1. In `AdvisorListView.get()`, replace the f-string ORDER BY interpolation with a strict allowlist approach:

```python
ALLOWED_ORDER_FIELDS = {
    'aum': 'a.aum_current',
    'change': 'aum_change_pct',
    'risk': 'aum_change_pct',
    'name': 'a.full_name',
    'firm': 'a.firm_name',
}
ALLOWED_DIRECTIONS = ('asc', 'desc')

ordering = request.query_params.get('ordering', 'aum')
direction = request.query_params.get('direction', 'desc').lower()

order_expr = ALLOWED_ORDER_FIELDS.get(ordering, 'a.aum_current')
if direction not in ALLOWED_DIRECTIONS:
    direction = 'desc'
```

2. Move these constants to module level (outside the class) for reuse.
3. Add a test in `easy_button/tests.py` that passes `ordering='; DROP TABLE advisors; --'` and `direction="asc; SELECT 1"` and verifies they are safely handled.
4. Add similar validation to any other views in easy_button that accept user-controlled sort/filter parameters.

## Dependencies
- None (standalone fix)

## Acceptance Criteria
- [ ] No f-string interpolation of user-controlled values into SQL
- [ ] All sort/direction values validated against explicit allowlists
- [ ] Unit test covering malicious ordering/direction inputs
- [ ] Code review confirms no other SQL injection vectors in easy_button/views.py
