# TODO 352: Fix ESM Build Output (package.json references missing files)

**Repo:** signal-studio-templates  
**Priority:** P0 (Breaks npm publishing and Next.js/Vite consumers)  
**Effort:** S (1-2 hours)  
**Status:** pending

---

## Problem

`package.json` declares `"module": "dist/index.esm.js"` and ESM exports, but `tsconfig.json` only emits CommonJS. The ESM files do not exist. Any modern bundler (Next.js, Vite, Webpack 5) will fail when consuming this package.

## Coding Prompt

```
In /data/workspace/projects/signal-studio-templates/:

1. Install tsup as dev dependency:
   pnpm add -D tsup

2. Create tsup.config.ts:
   import { defineConfig } from 'tsup'
   export default defineConfig({
     entry: ['index.ts', 'schema/signal-template.ts', 'engine/template-engine.ts'],
     format: ['cjs', 'esm'],
     dts: true,
     splitting: false,
     sourcemap: true,
     clean: true,
     outDir: 'dist',
   })

3. Update package.json scripts:
   "build": "tsup",
   "build:watch": "tsup --watch",

4. Run: pnpm build

5. Verify dist/ now contains:
   - index.js (CJS)
   - index.mjs or index.esm.js (ESM)
   - index.d.ts (types)
   - schema/signal-template.js + .mjs + .d.ts
   - engine/template-engine.js + .mjs + .d.ts

6. Update package.json exports to match actual output filenames from tsup.

7. Run: npm test to verify nothing broke.
```

## Acceptance Criteria

- [ ] `pnpm build` succeeds without errors
- [ ] `dist/index.mjs` (or `index.esm.js`) exists
- [ ] `dist/index.d.ts` exists
- [ ] All exports in package.json resolve to real files
- [ ] `npm test` still passes

## Dependencies

None — standalone fix. Should be done alongside or after TODO 351.
