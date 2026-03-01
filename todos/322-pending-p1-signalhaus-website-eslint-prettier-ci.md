# TODO 322 — Add ESLint + Prettier + CI Type-Check to signalhaus-website

**Priority:** P1 — High  
**Repo:** signalhaus-website  
**Effort:** S (1-2 hours)  
**Dependencies:** None

---

## Description

The site has no ESLint config, no Prettier config, and no lint/type-check step in CI. Code quality issues can slip through. This is a quick baseline fix.

---

## Coding Prompt

```
In /data/workspace/projects/signalhaus-website/:

1. Add ESLint:
   - Add to package.json devDependencies: `eslint`, `eslint-config-next`
   - Create `.eslintrc.json`:
     ```json
     {
       "extends": ["next/core-web-vitals"]
     }
     ```
   - Add to package.json scripts: `"lint": "next lint"`

2. Add Prettier:
   - Add to package.json devDependencies: `prettier`
   - Create `.prettierrc`:
     ```json
     {
       "semi": false,
       "singleQuote": false,
       "tabWidth": 2,
       "trailingComma": "es5",
       "printWidth": 100
     }
     ```
   - Add to package.json scripts: `"format": "prettier --write src/"`
   - Add to package.json scripts: `"format:check": "prettier --check src/"`

3. Update `.github/workflows/ci.yml` to add steps after existing build step:
   - `- name: Lint` → `run: yarn lint`
   - `- name: Type check` → `run: yarn tsc --noEmit`

4. Run `yarn lint` and fix any lint errors found.
5. Run `yarn build` to verify everything passes.
```

---

## Acceptance Criteria
- [ ] `.eslintrc.json` exists with next/core-web-vitals
- [ ] `.prettierrc` exists
- [ ] `yarn lint` runs without errors
- [ ] `yarn tsc --noEmit` passes
- [ ] CI workflow includes lint and type-check steps
