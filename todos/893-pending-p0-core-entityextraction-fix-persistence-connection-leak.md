# TODO-893: Fix Connection Leak in persistence.py (else clause pattern)

**Repo:** core-entityextraction  
**Priority:** P0  
**Effort:** XS (15 minutes)  
**Status:** pending

## Problem

`persistence.py` has multiple functions (`load_all`, `save_entities`, `delete_entities`) using a `try/except/else` pattern where `_put_conn(conn)` is in the `else` clause. This means if an exception is raised, the connection is returned with `close=True`, but if `_put_conn(conn)` is somehow skipped (e.g., early return), the connection leaks.

More critically, `init_db()` has a bug in the try/except/else:
```python
def init_db():
    ...
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(CREATE_TABLE_SQL)
        return True
    except Exception as exc:
        ...
        _put_conn(conn, close=True)
        return False
    else:           # ← This runs ONLY if no exception — but 'return True' already exits!
        _put_conn(conn)  # ← NEVER REACHED — connection leaks on success!
```

The `else` after `try` in Python only runs if the `try` block completes without exception AND without `return`. Since `return True` is in the `try` block, the `else` never runs, so the connection is never returned to the pool on success.

## Fix

Convert all `try/except/else` connection return patterns to use `finally`:

```python
def init_db() -> bool:
    conn = _get_conn()
    if conn is None:
        return False
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(CREATE_TABLE_SQL)
        LOGGER.info("Entity persistence table ready.")
        return True
    except Exception as exc:
        LOGGER.error("Failed to init DB: %s", exc)
        _put_conn(conn, close=True)
        return False
    finally:
        _put_conn(conn)  # always return to pool
```

Wait — the `finally` would run even on the `except` path, causing double-return. Instead use a flag:

```python
def init_db() -> bool:
    conn = _get_conn()
    if conn is None:
        return False
    broken = False
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(CREATE_TABLE_SQL)
        LOGGER.info("Entity persistence table ready.")
        return True
    except Exception as exc:
        LOGGER.error("Failed to init DB: %s", exc)
        broken = True
        return False
    finally:
        _put_conn(conn, close=broken)
```

Apply the same pattern to `load_all`, `save_entities`, and `delete_entities`.

## Coding Prompt

```
Edit /data/workspace/projects/core-entityextraction/persistence.py

For each of these four functions: init_db(), load_all(), save_entities(), delete_entities()

Replace the try/except/else pattern with try/except/finally using a `broken` flag:

Pattern to apply:
    broken = False
    try:
        # ... existing try body ...
        return success_value
    except Exception as exc:
        LOGGER.error("...", exc)
        broken = True
        return failure_value
    finally:
        _put_conn(conn, close=broken)

This ensures connections are always returned to the pool, whether the operation succeeded or failed.

Run the test suite after: pytest tests/ -x -q
```

## Acceptance Criteria
- [ ] All 4 persistence functions use `finally` for connection return
- [ ] No connection leak on success path (previously broken for `init_db`)
- [ ] Existing tests continue to pass

## Dependencies
None
