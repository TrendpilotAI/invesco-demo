# TODO-456 DONE ✅

## Summary
Replaced Django 3.x deprecated utilities with Django 4.2 equivalents across the forwardlane-backend project.

## Files Changed (3)

### `user/resources/user/serializers.py`
- `from django.utils.encoding import force_bytes, force_text` → `from django.utils.encoding import force_bytes, force_str`
- `force_text(urlsafe_base64_decode(uid))` → `force_str(urlsafe_base64_decode(uid))`

### `user/resources/user/viewsets.py`
- `from django.utils.encoding import force_text` → `from django.utils.encoding import force_str`
- 3x `force_text(urlsafe_base64_decode(...))` → `force_str(urlsafe_base64_decode(...))`

### `forwardlane/middleware.py`
- `from django.utils.translation import ugettext as _` → `from django.utils.translation import gettext as _`

## Django Check
`python manage.py check` could not run (no DB/env config in sandbox), but the replacements are 1:1 compatible — `force_str` and `force_text` have identical signatures; `gettext`/`gettext_lazy` are direct replacements.

## Commit
`fix: replace Django 3.x deprecated utils with Django 4.2 equivalents (TODO-456)`

## Push
Rebased on remote changes and pushed to `origin/railway-deploy` successfully.
Commit: `3c899fb8`
