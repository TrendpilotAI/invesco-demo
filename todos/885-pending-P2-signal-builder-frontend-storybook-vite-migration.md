# TODO-885: Migrate Storybook from webpack5 to Vite Builder

**Repo:** signal-builder-frontend  
**Priority:** P2 (Medium)  
**Effort:** S (half day)  
**Status:** pending

## Problem

Storybook v6 uses webpack5 builder (`@storybook/builder-webpack5`) while the app runs Vite. This mismatch causes:
- Different module resolution behavior between Storybook and app
- Dead devDependencies bloating install time
- Storybook v6 is EOL (v8 current)
- Blocks Chromatic visual regression integration

## Coding Prompt

```
Migrate Storybook from webpack5 to Vite:

1. Remove old webpack Storybook deps from package.json devDependencies:
   - @storybook/builder-webpack5
   - @storybook/manager-webpack5  
   - @storybook/preset-create-react-app
   - webpack (if only used for Storybook)
   - babel-plugin-named-exports-order
   - @babel/plugin-proposal-private-property-in-object
   - storybook-css-modules (may need replacement)

2. Upgrade Storybook to v8:
   npx storybook@latest upgrade
   
   OR do a manual migration:
   yarn add -D @storybook/react-vite@8 @storybook/react@8 @storybook/addon-essentials@8

3. Update .storybook/main.js (or main.ts):
   export default {
     framework: {
       name: '@storybook/react-vite',
       options: {},
     },
     stories: ['../src/**/*.stories.@(ts|tsx|js|jsx)'],
     addons: [
       '@storybook/addon-links',
       '@storybook/addon-essentials',
       '@storybook/addon-interactions',
     ],
   };

4. Remove postcss addon from Storybook — Vite handles PostCSS natively.

5. Update package.json scripts:
   "storybook": "storybook dev -p 6006"
   "build-storybook": "storybook build"

6. Test: yarn storybook — verify all existing stories render correctly.

7. Fix any stories that relied on webpack-specific features.
```

## Acceptance Criteria
- [ ] `yarn storybook` starts successfully with Vite builder
- [ ] All existing component stories render without errors
- [ ] `yarn build-storybook` produces static build
- [ ] No webpack packages in devDependencies
- [ ] Storybook version is 8.x
- [ ] Tailwind CSS works in Storybook (via shared PostCSS config)
