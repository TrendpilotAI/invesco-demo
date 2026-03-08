# TODO-836: Upgrade Sequelize v3 → v6 (forwardlane_advisor)

**Repo:** forwardlane_advisor  
**Priority:** P1  
**Effort:** Large (3-5 days)  
**Status:** pending

## Description
forwardlane_advisor uses Sequelize v3 (2016-era ORM). Sequelize v6 brings TypeScript support, better hooks, improved associations, Promise-based APIs (no more .then() chains), and active security support. v3 has known CVEs and is unmaintained.

## Coding Prompt
Upgrade Sequelize from v3 to v6 in `/data/workspace/projects/forwardlane_advisor/`:
1. `npm install sequelize@^6 sequelize-cli@^6 mysql2@^3` (replace mysql dependency)
2. Update all model files in `models/` to use Sequelize v6 class-based syntax (`Model.init()`)
3. Update `models/index.js` to use the v6 pattern
4. Replace `.success()/.error()` callbacks with Promise `.then()/.catch()` or async/await
5. Update associations syntax if needed
6. Run existing tests to verify: `npm test`
7. Update `seq_migrations/` config to use v6 CLI format

## Acceptance Criteria
- `npm install` completes without warnings about deprecated Sequelize peer deps
- All model files use Sequelize v6 class syntax
- Application starts without errors: `node app.js`
- `npm test` passes

## Dependencies
- None (standalone upgrade)
