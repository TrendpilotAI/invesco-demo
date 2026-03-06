# TODO-647: Upgrade Storybook v6 → v8 in Signal Builder Frontend

**Repo:** signal-builder-frontend  
**Priority:** P2  
**Effort:** Medium (1-2 days)  
**Category:** Dependencies / Security

## Description
Storybook v6 has known CVEs and is no longer maintained. v8 has massive improvements: Vite-native builds, CSF3, improved performance, better TypeScript support.

## Coding Prompt
```
In /data/workspace/projects/signal-builder-frontend/:
1. Run the Storybook migration tool: npx storybook@latest upgrade
2. Follow migration prompts
3. Update all @storybook/* packages to v8
4. Migrate any .stories.js to .stories.tsx with CSF3 format
5. Test: yarn storybook — verify no component errors
6. Remove: @storybook/builder-webpack5, @storybook/manager-webpack5 (replaced by Vite builder)
```

## Acceptance Criteria
- [ ] All @storybook/* packages at v8.x
- [ ] yarn storybook runs without errors
- [ ] Stories display correctly
- [ ] No webpack-based storybook packages in package.json

## Dependencies
- TODO-645 (TS upgrade) preferred first
