# TODO-838: Remove Watson Dead Code — retrieve_and_rank + test_rig models (forwardlane_advisor)

**Repo:** forwardlane_advisor  
**Priority:** P0  
**Effort:** Small (2-4 hours)  
**Status:** pending

## Description
Multiple dead code artifacts remain after Watson EOL cleanup:
- `app/retrieve_and_rank/` — entire directory (Watson R&R was shut down Aug 2021)
- `models/test_rig_intelligent_tagger_*.js` — 5 test fixture models loaded in production
- `app/hdialog/` — Watson Dialog references (deprecated 2016, shut down 2017)

## Coding Prompt
In `/data/workspace/projects/forwardlane_advisor/`:
1. Delete `app/retrieve_and_rank/` entirely: `rm -rf app/retrieve_and_rank/`
2. Move test_rig model files to `test/fixtures/`: `mv models/test_rig_intelligent_tagger_*.js test/fixtures/`
3. Remove those models from `models/index.js` (grep for test_rig)
4. Audit `app/hdialog/` — remove any direct Watson Dialog API calls (not the LLM gateway ones)
5. Remove `watson-developer-cloud` from package.json if still present
6. Run `node app.js` to verify no startup errors
7. Run `npm test`
8. Commit with message: `chore: remove Watson dead code (retrieve_and_rank, test_rig models)`

## Acceptance Criteria
- `app/retrieve_and_rank/` directory is gone
- No `test_rig_intelligent_tagger` models in `models/index.js`
- `npm audit` shows no Watson SDK entries
- App starts cleanly

## Dependencies
- None — safe to do immediately
