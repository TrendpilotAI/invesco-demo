# TODO-342: Migrate Storybook v6 → v8 with Vite Builder

**Repo:** signal-builder-frontend  
**Priority:** P2 | **Effort:** M (1 week)  
**Status:** pending

## Problem
Storybook v6 with webpack5 builder is EOL. Has known CVEs in webpack deps. Conflicts with Vite-based dev setup. No stories written for core components.

## Task
1. Upgrade Storybook from v6 → v8 using `npx storybook upgrade`
2. Switch from webpack5 to @storybook/builder-vite (matches dev stack)
3. Write stories for all FlowNode types:
   - FilterContent (node view + sidebar view)
   - FlowNode (all node types)
   - FlowEdge
   - Header components (CreateSignalModal, PublishModal, ValidationModal)
4. Set up Chromatic for visual regression

## Coding Prompt
```
cd /data/workspace/projects/signal-builder-frontend
1. Run: npx storybook@latest upgrade
2. Install: npm install --save-dev @storybook/builder-vite
3. Update .storybook/main.js: set builder to '@storybook/builder-vite'
4. Migrate .storybook/preview.js to preview.ts, import Tailwind styles
5. Write stories in src/modules/builder/containers/FlowNode/*.stories.tsx
6. Run: npm run storybook to verify
```

## Acceptance Criteria
- [ ] Storybook v8 running on Vite builder
- [ ] Stories for all FlowNode variants
- [ ] No webpack deps in storybook config
- [ ] Visual regression via Chromatic (optional but recommended)
