# TODO-396: Remove Dead services/ml_entity_extraction_service/ Directory

**Repo:** core-entityextraction  
**Priority:** P0  
**Effort:** XS (5 min)  
**Status:** pending

## Description
The `services/ml_entity_extraction_service/` directory contains Flask-era service class wrappers (`ml_entity_extraction_service.py`, `spacy_entity_extraction_service.py`) that are no longer imported or used. The ML/spaCy logic was inlined directly into `main.py` as `ml_predict()` and `spacy_predict()` during the FastAPI rewrite.

## Coding Prompt
```
In /data/workspace/projects/core-entityextraction/:
1. Confirm services/ml_entity_extraction_service/ files are NOT imported in main.py or any other active file:
   grep -r "ml_entity_extraction_service\|spacy_entity_extraction_service" . --include="*.py" | grep -v __pycache__
2. If confirmed unused, delete:
   rm -rf services/ml_entity_extraction_service/
3. Check if services/__init__.py exists and if services/ dir is now empty; if so remove:
   rm -rf services/
4. Also check/remove utils/common.py and utils/logger.py if not imported anywhere:
   grep -r "from utils\|import utils" . --include="*.py" | grep -v __pycache__
5. Commit: git commit -am "chore: remove dead Flask-era service wrappers"
```

## Dependencies
None

## Acceptance Criteria
- `services/` directory deleted or confirmed empty
- No import errors on `python -c "import main"`
- Git commit with removal
