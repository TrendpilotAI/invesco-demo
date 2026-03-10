# TODO-894: Set Up Vitest Unit Test Suite
**Repo:** signalhaus-website  
**Priority:** P1  
**Status:** pending  
**Effort:** 2-3h

## Problem
The signalhaus-website has 0% test coverage. No test runner is configured. Critical business logic (`validateContact()`, ROI calculator math, MDX parsing) has no automated verification. A regression in form validation or email logic would not be caught before production deployment.

## Task
Set up Vitest as the unit test runner and write tests for all critical business logic paths.

## Coding Prompt
```
In /data/workspace/projects/signalhaus-website:

1. Install Vitest and testing utilities:
   npm install --save-dev vitest @vitest/coverage-v8 @testing-library/react @testing-library/jest-dom jsdom

2. Create vitest.config.ts:
   import { defineConfig } from 'vitest/config'
   import react from '@vitejs/plugin-react'
   import path from 'path'
   
   export default defineConfig({
     plugins: [react()],
     test: {
       environment: 'jsdom',
       globals: true,
       setupFiles: ['./src/tests/setup.ts'],
       coverage: { reporter: ['text', 'lcov'], include: ['src/**/*.ts', 'src/**/*.tsx'] }
     },
     resolve: { alias: { '@': path.resolve(__dirname, './src') } }
   })

3. Create src/tests/setup.ts:
   import '@testing-library/jest-dom'

4. Add package.json scripts:
   "test": "vitest run",
   "test:watch": "vitest",
   "test:coverage": "vitest run --coverage"

5. Create src/tests/validateContact.test.ts:
   Test all branches of validateContact():
   - missing name → error
   - name > 100 chars → error  
   - invalid email → error
   - invalid budget (not in whitelist) → error
   - message < 10 chars → error
   - XSS patterns (<script, javascript:, on*=) → error
   - valid complete payload → ok: true with parsed data
   - optional company/budget → ok when missing

6. Create src/tests/roi.test.ts:
   Extract ROI calculation logic from ROICalculator.tsx into src/lib/roi.ts
   Test with known inputs:
   - 10 employees × $75/hr × 20% time saved → expected annual savings
   - Verify payback period calculation
   - Edge cases: 0 employees, 0% savings

7. Create src/tests/mdx.test.ts:
   Mock fs.readdir and fs.readFile
   Test getAllPosts() returns sorted by date DESC
   Test getPostBySlug() returns null for missing slug
   Test frontmatter parsing extracts title, date, excerpt, tags

8. Add TypeScript interface for PostFrontmatter in src/lib/mdx.ts:
   interface PostFrontmatter {
     title: string
     date: string
     excerpt: string
     tags: string[]
     author?: string
   }
```

## Dependencies
- Should run BEFORE Playwright E2E tests (614-pending)
- ESLint setup (615-pending) should be done alongside

## Acceptance Criteria
- `npm test` runs without errors
- validateContact() has 100% branch coverage
- ROI math functions extracted and tested
- MDX parsing tested
- CI (611-pending) runs `npm test` on every push
