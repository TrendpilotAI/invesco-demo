# TODO-568: Sequelize v3 → v6 Migration — forwardlane_advisor

**Repo:** forwardlane_advisor  
**Priority:** P0  
**Status:** pending

## Description
Sequelize v3 is EOL and incompatible with modern Node.js patterns. Migrate all 30+ model files to Sequelize v6.

## Steps
1. Update `sequelize` and `sequelize-cli` in package.json to v6
2. Migrate all `models/*.js` from `classMethods`/`instanceMethods` to `Model.init()` pattern
3. Fix deprecated `.find()` → `.findOne()`, `.upsert()` changes
4. Update `models/index.js` initialization pattern
5. Fix all associations syntax
6. Run all existing tests and routes

## Files to Update
All files in `models/` (30+ files), `app/*/` that use Sequelize queries

## Acceptance Criteria
- All models load without warnings
- All existing routes return expected data
- No Sequelize deprecation warnings in console
- `npm test` passes

## Dependencies
TODO-567 (CVE audit) should complete first
