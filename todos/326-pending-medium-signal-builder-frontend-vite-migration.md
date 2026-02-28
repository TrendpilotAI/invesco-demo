# TODO-326: Vite Migration from CRA+craco — Signal Builder Frontend

**Priority:** P1 (Medium)
**Status:** Pending
**Project:** signal-builder-frontend
**Effort:** M (2 days)
**Depends On:** TODO-324 (fix deprecated deps) must be done first
**Source:** PLAN.md → P1-001

---

## Task Description

Replace the deprecated Create React App + craco build system with Vite. This will dramatically improve dev server startup time (cold start from ~30s to ~2s) and build times. All craco path aliases must be replicated in the Vite config.

---

## Coding Prompt

```
You are working in the Signal Builder Frontend repo at /data/workspace/projects/signal-builder-frontend.

Migrate from CRA+craco to Vite. Do this in a branch to allow safe rollback.

Prerequisites: TODO-324 (deprecated deps) should already be done.

Steps:

1. Install Vite and plugins:
   ```
   yarn add -D vite @vitejs/plugin-react vite-tsconfig-paths
   ```

2. Audit current craco config:
   ```
   cat craco.config.js
   cat tsconfig.json  # check paths/baseUrl
   ```

3. Create `vite.config.ts` at project root:
   ```ts
   import { defineConfig } from 'vite';
   import react from '@vitejs/plugin-react';
   import tsconfigPaths from 'vite-tsconfig-paths';

   export default defineConfig({
     plugins: [react(), tsconfigPaths()],
     server: {
       port: 3000,
       open: true,
     },
     build: {
       outDir: 'build', // keep same as CRA for Dockerfile compat
       sourcemap: true,
     },
     define: {
       // CRA exposes process.env.REACT_APP_* — Vite uses import.meta.env.VITE_*
       // Option A: keep REACT_APP_ prefix working temporarily
       'process.env': 'import.meta.env',
     },
   });
   ```
   Note: If using `process.env` define shim, audit all env var usages and migrate to `import.meta.env.VITE_*` for new vars.

4. Move `public/index.html` to project root (Vite convention):
   - Copy `public/index.html` → `index.html`
   - In `index.html`, add: `<script type="module" src="/src/index.tsx"></script>`
   - Remove the `%PUBLIC_URL%` references (Vite handles static assets differently)

5. Update `package.json` scripts:
   ```json
   "scripts": {
     "start": "vite",
     "build": "tsc && vite build",
     "preview": "vite preview",
     "test": "vitest run",   // or keep jest if preferred
     "test:watch": "vitest"
   }
   ```

6. Update TypeScript config — replace CRA type reference:
   - In `src/react-app-env.d.ts` or `src/vite-env.d.ts`:
     ```ts
     /// <reference types="vite/client" />
     ```
   - Remove `/// <reference types="react-scripts" />`

7. Remove CRA+craco packages:
   ```
   yarn remove react-scripts craco @craco/craco
   ```
   (or whatever craco packages are installed — check package.json first)

8. Update Dockerfile:
   - Change build command if it references `react-scripts build`
   - Change `yarn start` → `yarn preview` or serve the `build/` dir with nginx

9. Update `bitbucket-pipelines.yml` build step similarly.

10. Test thoroughly:
    - `yarn start` — dev server loads, hot reload works
    - `yarn build` — production build succeeds
    - Check all route-based code splitting still works
    - Check all path aliases resolve
    - Check environment variables load correctly

Document any breaking changes in a MIGRATION.md file.
```

---

## Acceptance Criteria

- [ ] `vite.config.ts` created with all path aliases matching previous craco config
- [ ] `index.html` moved to project root with Vite script tag
- [ ] `package.json` scripts updated (`start`, `build`, `preview`)
- [ ] `react-app-env.d.ts` replaced with `vite/client` reference
- [ ] `react-scripts` and `craco` removed from dependencies
- [ ] `yarn start` launches dev server in < 5 seconds
- [ ] `yarn build` produces working production build
- [ ] Dockerfile and `bitbucket-pipelines.yml` updated
- [ ] All existing functionality works (manual smoke test of key flows)
- [ ] `MIGRATION.md` documents any breaking changes or env var renames
