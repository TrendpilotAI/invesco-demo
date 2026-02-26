# 211 — Fix Build System: Install Deps, Fix tsconfig Paths, Generate dist/

**Priority:** critical  
**Project:** signal-studio-templates  
**Repo:** /data/workspace/projects/signal-studio-templates/  
**Status:** pending  
**Estimated Effort:** 2h  

---

## Context

The signal-studio-templates repo contains 20 pre-built TypeScript signal templates for ForwardLane Signal Studio (Invesco client). Currently there are **no build artifacts** (no `dist/` directory), which means the templates cannot be consumed by the Next.js Signal Studio frontend or any downstream service. The `tsconfig.json` may have incorrect paths, and `node_modules` may be absent or incomplete.

---

## Task Description

1. `cd /data/workspace/projects/signal-studio-templates`
2. Inspect `package.json` for build scripts, main/types entry points, and engine requirements.
3. Inspect `tsconfig.json` for compiler options (outDir, rootDir, paths, module resolution).
4. Run `npm install` (or `yarn install`) to install all dependencies.
5. Fix any `tsconfig.json` issues:
   - Set `"outDir": "./dist"`
   - Set `"rootDir": "./src"`
   - Set `"declaration": true` and `"declarationMap": true`
   - Set `"sourceMap": true`
   - Ensure module is `"ESNext"` or `"CommonJS"` as appropriate
6. Run `npm run build` and fix any TypeScript compilation errors until build succeeds cleanly.
7. Verify `dist/` directory is created with `.js`, `.d.ts`, and `.js.map` files.
8. Update `package.json` main/types fields to point to `dist/index.js` and `dist/index.d.ts`.
9. Add `.gitignore` entry for `dist/` if not already present (build artifacts should be generated, not committed — unless this is a published package).
10. Commit the fixed tsconfig and package.json.

---

## Coding Prompt (Autonomous Agent)

```
You are fixing the build system for the signal-studio-templates TypeScript project.

REPO: /data/workspace/projects/signal-studio-templates/

Steps:
1. Read package.json, tsconfig.json, and src/index.ts (or src/index.ts equivalent)
2. Install dependencies: run `npm install` in the repo directory
3. Fix tsconfig.json to ensure:
   - outDir: ./dist
   - rootDir: ./src (or wherever source files live)
   - declaration: true
   - declarationMap: true
   - sourceMap: true
   - strict: true
4. Run `npm run build` and capture output
5. Fix ALL TypeScript errors one by one until build passes cleanly
6. Verify dist/ contains index.js + index.d.ts
7. Update package.json: set "main": "dist/index.js", "types": "dist/index.d.ts"
8. Run the build once more to confirm it's clean
9. Report: list of files in dist/, any errors fixed, build time

Do NOT skip errors. The build must be 100% clean.
```

---

## Dependencies

- None (this is the first task — everything else depends on it)

---

## Acceptance Criteria

- [ ] `npm install` completes without errors
- [ ] `npm run build` exits with code 0
- [ ] `dist/` directory exists with `.js` and `.d.ts` files
- [ ] `package.json` main/types fields point to `dist/`
- [ ] No TypeScript compilation errors or warnings
- [ ] Build is reproducible (running build twice gives same output)
