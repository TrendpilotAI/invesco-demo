# TODO-398: NarrativeReactor — TypeScript `any` Type Cleanup

**Priority:** high
**Repo:** NarrativeReactor
**Effort:** M (2-3 days)

## Description
169 `: any` type violations in source code. These hide runtime errors and make refactoring dangerous.

## Coding Prompt
```
Fix TypeScript `any` type violations in /data/workspace/projects/NarrativeReactor/src/

Run: grep -rn ": any" src/ --include="*.ts" | grep -v __tests__

For each hit:
1. If it's a service return type, create proper interface in src/types/
2. If it's an API request body, use Zod schema and z.infer<> for the type
3. If it's an external API response, create typed interface matching the API docs
4. Enable strict: true in tsconfig.json after all fixes pass

Priority order:
- src/services/*.ts (most impactful)
- src/routes/*.ts 
- src/flows/*.ts
- src/middleware/*.ts
```

## Acceptance Criteria
- [ ] `grep -rn ": any" src/ | wc -l` returns 0
- [ ] `tsc --noEmit` passes with strict mode
- [ ] All existing tests still pass

## Dependencies
None
