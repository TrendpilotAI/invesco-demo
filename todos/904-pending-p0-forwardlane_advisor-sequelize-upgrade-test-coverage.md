# TODO: Upgrade Sequelize v3→v6 and Add Test Coverage Gates

## Priority: P0
## Repo: forwardlane_advisor

### Problem
Using Sequelize v3 (EOL), AWS SDK v2 (deprecated), and Jade template engine (deprecated). Near-zero test coverage with no CI configured.

### Action Items
- Upgrade Sequelize from v3 to v6 (handle breaking changes: model definitions, associations, query methods)
- Upgrade AWS SDK from v2 to v3 (modular imports)
- Replace jade with pug or remove template engine if not needed
- Add Jest/Mocha test suite with coverage threshold at 60%
- Set up CI pipeline (GitHub Actions or Bitbucket) to run tests on PR

### Impact
- Eliminates security vulnerabilities in EOL dependencies
- Required for long-term maintainability
- Prevents runtime errors from deprecated APIs

### References
- PLAN.md dependency upgrade section
- Existing package.json
