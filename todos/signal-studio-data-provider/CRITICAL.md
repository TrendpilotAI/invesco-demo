# 🔴 CRITICAL ISSUES — signal-studio-data-provider

**Updated:** 2026-03-15

---

## 1. RUNTIME BREAKAGE: SecretStr fields accessed without `.get_secret_value()`

**Impact:** All provider connections CRASH at runtime — nothing works  
**Root cause:** `config.py` uses `pydantic.SecretStr` for passwords/keys, but provider code still accesses them as plain `str`.

**Affected files:**
| File | Line | Code | Fix |
|------|------|------|-----|
| `providers/snowflake_provider.py` | 71 | `password=self._sf.password` | `password=self._sf.password.get_secret_value()` |
| `providers/oracle_provider.py` | 49 | `password=self._ora.password` | `password=self._ora.password.get_secret_value()` |
| `providers/supabase_provider.py` | 43 | `self._sb.database_url` | `self._sb.database_url.get_secret_value()` |

**Also check:** Any usage of `anon_key` or `service_role_key` in supabase_provider.py.

**Effort:** 15 minutes  
**Risk:** Zero — purely mechanical fix

---

## 2. TEST RUNNER BROKEN: Zero Tests Executing

**Impact:** No test coverage verification possible  
**Error:** `ValueError: numpy.dtype size changed, may indicate binary incompatibility`  
**Fix:** `pip install --upgrade numpy pandas` or pin compatible versions in `pyproject.toml`  
**Effort:** 10 minutes

---

## 3. CORTEX SQL INJECTION — Vulnerable Pattern

**Impact:** Model name interpolated into f-string SQL despite allowlist existing  
**Files:** `providers/snowflake_provider.py` lines ~224, ~233  
**Details:** `_CORTEX_MODEL_ALLOWLIST` frozenset exists (line 201) and validation exists (line 213), but `cortex_complete()` and `cortex_embed()` still use f-string interpolation:
```python
f"SELECT SNOWFLAKE.CORTEX.COMPLETE('{model}', %s) AS response"
```
**Risk:** If validation is bypassed or model name contains quotes, SQL injection is possible.  
**Fix:** Verify `_validate_cortex_model()` is called before interpolation in both methods. Consider using parameterized queries if Snowflake supports it for function names.

---

## 4. DEPRECATED asyncio.get_event_loop() — Snowflake Provider

**Impact:** DeprecationWarning in Python 3.10+, will break in future Python versions  
**Files:** `providers/snowflake_provider.py` lines 108, 128, 191  
**Fix:** Replace with `asyncio.to_thread()` (same pattern Oracle already uses)  
**Effort:** 15 minutes

---

## Resolution Priority

1. Fix #1 FIRST — SecretStr regression makes ALL providers non-functional
2. Fix #2 — Unblocks test verification for all other fixes
3. Fix #3 — Security vulnerability in enterprise tier
4. Fix #4 — Deprecated API, ticking time bomb
