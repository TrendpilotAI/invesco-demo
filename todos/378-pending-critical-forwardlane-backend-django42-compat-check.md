# 378 — Django 4.2 Compatibility Check & Fix

**Repo:** forwardlane-backend  
**Priority:** critical  
**Effort:** M (2-4h)  
**Status:** pending

## Description
Django was upgraded from 3.2 → 4.2 in Pipfile but `pipenv install` has not been run in production. Django 4.2 removes `force_text`, `ugettext_lazy`, and other 3.x-only aliases. Must verify and fix all deprecation errors before next deploy.

## Coding Prompt
```
In /data/workspace/projects/forwardlane-backend/:

1. Run: pipenv install
2. Run: python manage.py check --settings=forwardlane.settings.development 2>&1
3. Find all uses of deprecated Django 3.x APIs:
   grep -r "force_text\|ugettext_lazy\|ugettext\|ungettext\|ugettext_noop\|force_unicode\|smart_unicode\|StrAndUnicode" --include="*.py" -l
4. Replace each with Django 4.x equivalents:
   - force_text → force_str
   - ugettext_lazy → gettext_lazy
   - ugettext → gettext
5. Run the full test suite: tox
6. Fix any remaining failures
7. Commit: "fix: Django 4.2 compatibility — replace deprecated 3.x API aliases"
```

## Acceptance Criteria
- `python manage.py check` returns 0 errors
- `tox` passes all tests
- No `force_text` or `ugettext` imports remain in codebase
