# TODO-480: Storybook v6 → v8 Migration with Vite Builder

**Project:** signal-builder-frontend
**Priority:** P1 (MEDIUM impact, M effort)
**Estimated Effort:** 4-6 hours
**Dependencies:** TODO-479 (TypeScript 5.x — v8 needs TS ≥4.9)

## Description

Storybook v6 with webpack5 builder is EOL and has known CVEs. Migrate to v8 with Vite builder to match dev stack. Write stories for all FlowNode types.

## Coding Prompt

```
You are working on signal-builder-frontend at /data/workspace/projects/signal-builder-frontend/.

TASK: Migrate Storybook v6 to v8 with Vite builder.

STEPS:
1. Remove all old Storybook packages:
   pnpm remove @storybook/addon-actions @storybook/addon-essentials @storybook/addon-interactions @storybook/addon-links @storybook/addon-postcss @storybook/addons @storybook/builder-webpack5 @storybook/manager-webpack5 @storybook/node-logger @storybook/preset-create-react-app @storybook/react @storybook/testing-library @storybook/theming storybook-css-modules

2. Install Storybook v8:
   pnpm dlx storybook@latest init --skip-install
   Or manually:
   pnpm add -D @storybook/react-vite @storybook/addon-essentials @storybook/addon-interactions @storybook/addon-links @storybook/blocks storybook

3. Create .storybook/main.ts:
   - framework: '@storybook/react-vite'
   - stories: ['../src/**/*.stories.@(ts|tsx)']
   - addons: essentials, interactions, links

4. Create .storybook/preview.ts with Tailwind CSS import and global decorators

5. Update existing stories (src/shared/widgets/Navigation/Navigation.stories.tsx, any Checkbox stories) to CSF3 format

6. Write new stories for FlowNode types:
   - src/modules/builder/containers/FlowNode/Filter/Filter.stories.tsx
   - src/modules/builder/containers/FlowNode/Dataset/Dataset.stories.tsx
   - src/modules/builder/containers/FlowNode/GroupFunction/GroupFunction.stories.tsx
   - src/modules/builder/containers/FlowNode/Target/Target.stories.tsx

7. Add scripts: "storybook": "storybook dev -p 6006", "build-storybook": "storybook build"
8. Run: pnpm storybook — verify it starts
9. Run: pnpm build-storybook — verify static build works

CONSTRAINTS:
- Use Vite builder (not webpack)
- CSF3 format for all stories
- Stories should show components with realistic mock data
- Remove deprecated @sentry/tracing while at it (TODO-365 overlap)
```

## Acceptance Criteria
- [ ] Storybook v8 with Vite builder running
- [ ] All old v6 packages removed
- [ ] Stories exist for all 4 FlowNode types
- [ ] `pnpm storybook` launches successfully
- [ ] `pnpm build-storybook` produces static output
- [ ] No webpack dependencies remain from Storybook
