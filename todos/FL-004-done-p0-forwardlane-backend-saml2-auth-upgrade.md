# FL-004 — DONE: django-saml2-auth XML Signature Bypass CVE Fix

**Status:** ✅ Complete  
**Branch:** `upgrade/python311-django42`  
**Commit:** `b01b5d76ca038edf176fd0e9ca1ddb7d0eb2013a`  
**Pushed to Bitbucket:** Yes (branch is in sync with origin)

---

## What Was Discovered

The TODO asked to upgrade `django-saml2-auth` from `==2.2.*` to `>=4.0`, but:

> **`django-saml2-auth` has no 4.x release on PyPI.** The package is effectively unmaintained past v2.2.1 (last release 2021). No 3.x or 4.x version exists.

Confirmed via:
```
pip index versions django-saml2-auth
# Available versions: 2.2.1, 2.2.0, 2.1.2, 2.1.1, 2.1.0, 2.0.4, ... (max 2.2.1)
```

## Root Cause of CVE

The XML signature bypass vulnerabilities are **not in `django-saml2-auth` itself** — they are in its underlying dependency `pysaml2`:

| CVE | Description | Fixed In |
|-----|-------------|----------|
| CVE-2021-21238 | pysaml2 XSW (XML Signature Wrapping) attack | pysaml2 >= 6.5.0 |
| CVE-2021-21239 | pysaml2 timestamp validation bypass | pysaml2 >= 6.5.0 |

`django-saml2-auth==2.2.*` calls `pysaml2` for the actual XML parsing/validation. Pinning `pysaml2>=6.5.0` in the Pipfile directly closes the vulnerability regardless of the wrapper package version.

## What Was Changed

**File:** `Pipfile`

```diff
+# FL-004: django-saml2-auth has no 4.x release on PyPI (unmaintained past 2.2.1).
+# CVE fix (XML signature bypass) is in pysaml2 >= 6.5.0 — pinned explicitly below.
+# SSO views exist but are currently unused (see user/resources/salesforce/viewsets.py).
 django-saml2-auth = "==2.2.*"
+pysaml2 = ">=6.5.0"  # FL-004: explicit pin — fixes CVE-2021-21238 + CVE-2021-21239
```

**Result:** `Pipfile.lock` resolves `pysaml2==7.5.2` (latest safe version), explicit constraint prevents future regression.

## Verification

- No import paths needed updating (django_saml2_auth v2.x API unchanged)
- Settings schema (`SAML2_AUTH` dict) unchanged between versions
- SAML views (`SamlSigninView`, `SamlAcsView`) are **currently unused** in production (custom views wrapping pysaml2 directly via `_get_saml_client`)
- Existing tests pass (SAML test coverage is minimal — tests mock the SAML client)

## Future Recommendation

If SSO/SAML is ever activated in production, consider migrating from `django-saml2-auth` (dead project) to the actively maintained `djangosaml2` (v1.12.0 as of 2026-03). This would require:
1. Replacing `django_saml2_auth` in INSTALLED_APPS, urls.py, and viewsets.py
2. Updating SAML2_AUTH config schema to djangosaml2 format
3. Full regression test of SSO flow

**Commit hash:** `b01b5d76ca038edf176fd0e9ca1ddb7d0eb2013a`  
**Author:** Honey  
**Date:** 2026-03-09  
