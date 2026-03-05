# 230 — Remove Dead Flask Code

**Repo:** core-entityextraction  
**Priority:** P0 (Clarity — these files are never imported)  
**Effort:** 30 minutes  
**Dependencies:** None

## Description
The `services/` and `controllers/` directories contain the original Flask implementation. The FastAPI rewrite in `main.py` does not import any of these files. They are dead code causing confusion.

## Coding Prompt
```
In /data/workspace/projects/core-entityextraction/:

1. Delete the following files (they are dead Flask code):
   - controllers/entity_extraction_controller.py
   - services/cache_service.py
   - services/db.py
   - services/fixed_lists_service.py
   - services/inialization.py  (also has typo)
   - services/pattern_matcher.py (superseded by logic in main.py)
   - uswgi.py (if exists — dead stub with typo)
   - app.py (if exists — old Flask app factory)

2. Check if services/__init__.py is still needed — if it only imported dead modules, delete it too.

3. Verify nothing in main.py imports from services/ or controllers/:
   grep -r "from services" main.py
   grep -r "from controllers" main.py
   (Should return no results.)

4. Remove the utils/ directory if it only contained Flask-specific helpers 
   (check if main.py imports from utils/).

5. After deletion, run: python -c "import main" to verify the app still imports cleanly.

6. Commit: "chore: remove dead Flask code (controllers/, services/ legacy layer)"
```

## Acceptance Criteria
- [ ] No files in services/ or controllers/ that are dead code
- [ ] `python -c "import main"` succeeds
- [ ] Docker build still succeeds
- [ ] All FastAPI endpoints still functional
