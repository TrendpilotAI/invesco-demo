# TODO-578: Upgrade Critical Dependencies

**Repo:** signal-builder-frontend  
**Priority:** P1 🔥  
**Effort:** S (1-2 days)  
**Status:** pending

## Task Description
Several major dependencies are outdated with known vulnerabilities or significant improvements:
- TypeScript 4.4 → 5.x (better type narrowing, const type params)
- React Query v4 → v5 (breaking API changes but much improved)  
- ReactFlow v11 → v12 (performance improvements, new features)
- @sentry/react v7 → v8

## Acceptance Criteria
- [ ] `yarn audit` shows 0 high/critical vulnerabilities
- [ ] TypeScript upgraded to 5.x with no new type errors
- [ ] All tests pass after upgrades
- [ ] App builds successfully with `yarn build`

## Coding Prompt (Agent-Executable)
```
Navigate to /data/workspace/projects/signal-builder-frontend/

1. Run security audit:
   yarn audit --level high
   Note all high/critical findings

2. Upgrade TypeScript:
   yarn add -D typescript@5
   yarn typecheck
   Fix any new type errors (TS5 is stricter)

3. Upgrade React Query (BREAKING CHANGES - careful):
   yarn add @tanstack/react-query@5
   - useQuery API changed: { isLoading } → { isPending }
   - Find all useQuery calls: grep -r "useQuery\|useMutation" src/ --include="*.ts" --include="*.tsx" -l
   - Update each file per migration guide: https://tanstack.com/query/v5/docs/react/guides/migrating-to-v5

4. Upgrade Sentry:
   yarn add @sentry/react@8
   Remove @sentry/tracing (merged into @sentry/react in v8)
   Update Sentry.init() call if needed

5. Run full build and test suite:
   yarn typecheck && yarn lint && yarn test && yarn build
```

## Dependencies
None — do this first before adding new features

## Notes
- ReactFlow v11→v12 is a significant upgrade; may need separate TODO
- Check reactflow changelog before upgrading
