# TODO-499: Bundle Size Audit — @xenova/transformers Client-Side Risk

**Repo:** signal-studio-frontend  
**Priority:** P1  
**Effort:** M (4-6 hours)  
**Status:** pending

## Description
`@xenova/transformers@^2.17.2` is a 100MB+ WASM-based ML library. If any client component imports it, it would catastrophically bloat the browser bundle. Must verify it's server-only. Also: dual reactflow adds ~400KB (see TODO-496).

## Coding Prompt
1. **Audit @xenova usage:**
   ```bash
   grep -r "@xenova/transformers" app/ components/ --include="*.tsx" --include="*.ts"
   ```
   Any client component import = critical bug. Move to server-only (`'use server'` or API route).

2. **Add bundle analyzer:**
   ```bash
   pnpm add -D @next/bundle-analyzer
   ```
   Update `next.config.mjs` to enable when `ANALYZE=true`.
   Run `ANALYZE=true pnpm build` and document findings.

3. **Add `server-only` guard:**
   In any file using @xenova or oracledb, add `import 'server-only'` at top to prevent accidental client bundling.

4. **Dynamic imports for heavy components:**
   - Visual builder: `const ReactFlow = dynamic(() => import('@xyflow/react'), { ssr: false })`
   - Chat markdown renderer
   - Any syntax highlighter (react-syntax-highlighter / shiki)

5. **Document findings in `/docs/bundle-audit.md`**

## Acceptance Criteria
- [ ] @xenova/transformers NOT in any client bundle (verified via bundle analyzer)
- [ ] `server-only` guards on all Oracle/ML service files
- [ ] Bundle analyzer configured and documented
- [ ] Main page JS < 200KB gzipped
