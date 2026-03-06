# TODO-590: Pin Wildcard Dependencies in Pipfile

**Priority:** MEDIUM  
**Repo:** forwardlane-backend  
**Effort:** S (1h)  
**Status:** pending  

## Description

Several critical dependencies use wildcard `"*"` version pins in Pipfile:
- `numpy = "*"`
- `pandas = "*"`
- `scipy = "*"`
- `lxml = "*"`
- `ipython = "*"`
- `jsonpickle = "*"`

Wildcards allow breaking major version changes to silently install, causing unpredictable prod failures.

## Task

1. Check current installed versions: `pipenv run pip freeze | grep -E "numpy|pandas|scipy|lxml|ipython|jsonpickle"`
2. Pin each to `>=current_major.current_minor,<next_major`:
   ```toml
   numpy = ">=1.26,<2.0"
   pandas = ">=2.0,<3.0"
   scipy = ">=1.11,<2.0"
   lxml = ">=4.9,<5.0"
   ```
3. Run `pipenv install` to verify lockfile resolves cleanly
4. Run `tox` to verify tests still pass

## Acceptance Criteria

- [ ] No `"*"` version specs remain for core scientific/data deps
- [ ] `Pipfile.lock` regenerated cleanly
- [ ] All tests pass
- [ ] CI pipeline passes
