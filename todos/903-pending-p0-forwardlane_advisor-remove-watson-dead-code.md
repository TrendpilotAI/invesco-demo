# TODO: Remove All Watson Dead Code and Legacy API Calls

## Priority: P0
## Repo: forwardlane_advisor

### Problem
Legacy Watson NLC/NLU code remnants with potentially hardcoded credentials remain in some code paths after the LLM gateway migration. This creates security risk and maintenance confusion.

### Action Items
- Search for all Watson SDK references: `grep -r "watson" app/ --include="*.js"`
- Remove all watson-developer-cloud / ibm-watson imports and handlers
- Remove conversation_scenario.xml if only for Watson
- Remove hardcoded Watson API keys/credentials from any config files
- Replace any remaining Watson dialog calls with LLM gateway equivalents
- Run full regression test after removal

### Impact
- Eliminates credential leakage risk
- Reduces codebase complexity
- Prevents accidental Watson API calls in production

### References
- AUDIT.md, BRAINSTORM.md
- app/dialogs/ directory
