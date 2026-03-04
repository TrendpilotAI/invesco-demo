# TODO-572: Remove Test Rig Models from Production — forwardlane_advisor

**Repo:** forwardlane_advisor  
**Priority:** P1  
**Status:** pending

## Description
5 test rig model files are in the production `models/` directory. Move them to `test/fixtures/`.

## Files to Move
- `models/test_rig_intelligent_tagger_entities.js`
- `models/test_rig_intelligent_tagger_entity_company_attributes.js`
- `models/test_rig_intelligent_tagger_entity_country_attributes.js`
- `models/test_rig_intelligent_tagger_tags.js`
- `models/test_rig_intelligent_tagger_topics.js`

## Steps
1. `mkdir -p test/fixtures/models`
2. Move all 5 files to `test/fixtures/models/`
3. Update `models/index.js` to remove their imports
4. Search codebase for any production usage: `grep -rn test_rig app/ routes.js`
5. Verify app boots without them

## Acceptance Criteria
- `models/` contains no `test_rig_*` files
- `models/index.js` has no test_rig imports
- App boots successfully

## Dependencies
None
