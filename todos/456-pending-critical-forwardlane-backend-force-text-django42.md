# TODO-456: Fix force_text → force_str (Django 4.2 compat)

**Priority:** CRITICAL  
**Repo:** forwardlane-backend  
**Effort:** XS (< 1 hour)  
**Dependencies:** None

## Description
`user/resources/user/viewsets.py` imports `force_text` which was removed in Django 4.2. This will cause a runtime crash in production after the Django 4.2 upgrade.

## Coding Prompt
```
In /data/workspace/projects/forwardlane-backend/:
1. Run: grep -r "force_text\|ugettext_lazy\|ugettext\b\|ugettext_noop" --include="*.py" -l
2. For each file found, replace:
   - `from django.utils.encoding import force_text` → `from django.utils.encoding import force_str`
   - All usages of `force_text(...)` → `force_str(...)`
   - `from django.utils.translation import ugettext_lazy` → `from django.utils.translation import gettext_lazy`
   - `from django.utils.translation import ugettext` → `from django.utils.translation import gettext`
3. Run: python manage.py check
4. Run: python -m pytest core/tests/ -x
5. Commit: "fix: replace Django 3.x deprecated utils with Django 4.2 equivalents"
```

## Acceptance Criteria
- [ ] `python manage.py check` passes with 0 errors
- [ ] No `force_text` or `ugettext` imports remain
- [ ] Tests pass
