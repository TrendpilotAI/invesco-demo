# 319 — TypeScript Type Safety Hardening

**Priority:** HIGH  
**Effort:** S  
**Status:** pending

---

## Task Description

The template schema has several loose types that allow bugs to slip through without TypeScript catching them: `defaultConfig: Record<string, unknown>`, `outputSchema[].type` as a loose string, `requiredDataSources` as unchecked strings, and missing `satisfies SignalTemplate` assertions. Tighten these so type errors surface at template definition time, not at runtime.

---

## Autonomous Coding Prompt

```
REPO: /data/workspace/projects/signal-studio-templates

TASK: Harden TypeScript types across the template schema and all 20 templates.

STEPS:

1. Open src/types/index.ts (or wherever SignalTemplate is defined).
   Make these changes:

   a. OutputFieldType:
      Before: type was a loose string or string literal
      After:
        export type OutputFieldType =
          | 'string' | 'currency' | 'percentage' | 'date'
          | 'array' | 'number' | 'boolean' | 'object';

   b. DataSource union:
      Audit all 20 templates for unique requiredDataSources values.
      Create:
        export type DataSource =
          | 'advisor_profiles' | 'holdings_summary' | 'client_interactions'
          | 'meeting_notes' | 'territory_data' | 'compliance_flags'
          // ... add all found values;
      Update SignalTemplate.requiredDataSources: DataSource[]

   c. ParameterType:
      export type ParameterType = 'string' | 'number' | 'boolean' | 'date' | 'enum';
      Update SignalTemplateParameter.type: ParameterType

   d. Per-template generic defaultConfig:
      Before: defaultConfig?: Record<string, unknown>
      After:  defaultConfig?: Record<string, string | number | boolean>
      (or make it generic: SignalTemplate<TConfig extends Record<string, ...>> if feasible)

   e. visualBuilderNodes:
      If currently optional, make it required with default []:
        visualBuilderNodes: VisualBuilderNode[];  // required, can be []

   f. Add satisfies assertion type:
      Export a helper: export const defineTemplate = <T extends SignalTemplate>(t: T): T => t;
      This gives template authors autocomplete + error surfacing at definition.

2. Update all 20 template files under templates/*/:
   - Wrap each export with defineTemplate({ ... }) instead of a plain object literal
   - OR add `satisfies SignalTemplate` at the end of each export
   - Add missing visualBuilderNodes: [] to any template that omits it
   - Fix any type errors surfaced by the stricter types

3. Update TemplateEngine and router to use the new strict types:
   - No `as any` or type assertions unless absolutely necessary (document why)
   - Replace any `Record<string, unknown>` with proper types

4. Update tsconfig.json to ensure strictest mode:
   {
     "strict": true,
     "noImplicitAny": true,
     "strictNullChecks": true,
     "noUncheckedIndexedAccess": true
   }
   Fix any new errors this surfaces.

5. Run: pnpm typecheck
   Zero errors required.

6. Add a test in tests/schema/templateSchema.test.ts (from TODO 318) that imports
   the DataSource and OutputFieldType unions and asserts all template values are valid
   members — belt-and-suspenders runtime check backing the compile-time check.

ACCEPTANCE: pnpm typecheck exits 0 with strict mode.
All 20 templates use defineTemplate() or satisfies SignalTemplate.
No `any` types in src/ (eslint @typescript-eslint/no-explicit-any: error enforces this).
```

---

## Dependencies

- **317** (ESLint with `no-explicit-any` rule needed to enforce no-`any`)

---

## Acceptance Criteria

- [ ] `OutputFieldType` is a strict union type (no loose `string`)
- [ ] `DataSource` is a union type covering all 20 templates' actual values
- [ ] `ParameterType` is a strict union
- [ ] All 20 templates use `defineTemplate()` or `satisfies SignalTemplate`
- [ ] `visualBuilderNodes` is required (non-optional) on `SignalTemplate`
- [ ] `pnpm typecheck` exits 0 in strict mode
- [ ] Zero `any` types in `src/` (enforced by ESLint)
