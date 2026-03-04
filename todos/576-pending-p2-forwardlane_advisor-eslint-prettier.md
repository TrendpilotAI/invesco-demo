# TODO-576: Add ESLint + Prettier + Pre-commit Hooks — forwardlane_advisor

**Repo:** forwardlane_advisor  
**Priority:** P2  
**Status:** pending

## Description
No linting or formatting enforcement. Add ESLint + Prettier with pre-commit hooks.

## Steps
1. `npm install --save-dev eslint prettier eslint-config-airbnb-base husky lint-staged`
2. Create `.eslintrc.json` with airbnb-base config, allow Node.js globals
3. Create `.prettierrc` with sensible defaults (singleQuote, 2 spaces)
4. Add `package.json` scripts: `"lint": "eslint app/ models/ routes.js app.js"`
5. Configure Husky pre-commit: run lint-staged
6. Run initial `npm run lint -- --fix` pass
7. Add `.vscode/settings.json` for editor integration

## Acceptance Criteria
- `npm run lint` passes on all files
- Pre-commit hook prevents committing unlinted code
- Consistent code style across codebase

## Dependencies
None
