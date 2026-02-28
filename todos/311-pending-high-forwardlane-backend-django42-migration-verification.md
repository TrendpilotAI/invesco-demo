# TODO-311: Django 4.2 Migration Verification — forwardlane-backend

**Priority:** HIGH  
**Effort:** M  
**Repo:** forwardlane-backend  
**Status:** pending

## Description
The Pipfile was updated to `django = "==4.2.*"` as part of INFRA-004. Django 4.2 removes several 3.x aliases (`force_text`, `ugettext_lazy`, `ugettext`, etc.). The upgrade has NOT been verified in production yet.

## Autonomous Coding Prompt
```
In /data/workspace/projects/forwardlane-backend/:
1. Run: grep -r "force_text\|ugettext_lazy\|ugettext\|smart_text\|force_str" --include="*.py" -l | grep -v __pycache__
2. For each file found, replace deprecated imports with Django 4.2 equivalents:
   - force_text → force_str (from django.utils.encoding)
   - ugettext_lazy → gettext_lazy (from django.utils.translation)
   - ugettext → gettext
   - smart_text → smart_str
3. Run: python manage.py check --deploy (set env vars as needed)
4. Run: python manage.py showmigrations to verify no pending migrations are broken
5. Run the test suite: python -m pytest --tb=short -q
6. Fix any failures. Commit with message: "fix: Django 4.2 compatibility — replace deprecated text utilities"
```

## Acceptance Criteria
- [ ] `python manage.py check` passes with 0 errors
- [ ] No deprecated `force_text`/`ugettext` usages remain
- [ ] Full test suite passes
- [ ] Committed and pushed

## Dependencies
None — this is a prerequisite for safe production deploy.
