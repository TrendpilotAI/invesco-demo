# TODO 361 — Signal Studio Frontend: Type Safety — Replace `Record<string, unknown>` with Discriminated Unions

**Status:** pending  
**Priority:** medium  
**Project:** signal-studio-frontend  
**Estimated Effort:** 4–6 hours  

---

## Description

`DataSource`, `SignalNode`, and `Template` types use `config: Record<string, unknown>` and `preview_data: Record<string, unknown>` as escape hatches. This loses type safety and makes working with these types error-prone. This task replaces them with discriminated unions typed to each specific variant.

---

## Coding Prompt (Autonomous Agent)

```
Repo: /data/workspace/projects/signal-studio-frontend

Task: Replace loose Record<string, unknown> types with discriminated unions.

Step 1 — Audit
  Open `src/types/index.ts` (or wherever DataSource, SignalNode, Template are defined).
  Identify all uses of `Record<string, unknown>` in config fields.

Step 2 — DataSource Discriminated Union
  For DataSource, create a union based on `type`:
  ```ts
  type DatabaseSourceConfig = { host: string; port: number; database: string; table: string; };
  type ApiSourceConfig = { url: string; method: 'GET' | 'POST'; headers?: Record<string, string>; };
  type FileSourceConfig = { path: string; format: 'csv' | 'json' | 'parquet'; };
  
  type DataSource =
    | { type: 'database'; config: DatabaseSourceConfig; id: string; name: string; }
    | { type: 'api';      config: ApiSourceConfig;      id: string; name: string; }
    | { type: 'file';     config: FileSourceConfig;     id: string; name: string; };
  ```
  Add any additional source types you find in the codebase or API response samples.

Step 3 — SignalNode Discriminated Union
  Similarly for SignalNode (filter, transform, output nodes):
  ```ts
  type FilterNodeConfig = { field: string; operator: string; value: unknown; };
  type TransformNodeConfig = { expression: string; outputField: string; };
  type OutputNodeConfig = { destination: string; format: string; };
  
  type SignalNode =
    | { type: 'filter';    config: FilterNodeConfig;    id: string; position: { x: number; y: number }; }
    | { type: 'transform'; config: TransformNodeConfig; id: string; position: { x: number; y: number }; }
    | { type: 'output';    config: OutputNodeConfig;    id: string; position: { x: number; y: number }; };
  ```

Step 4 — Template preview_data
  Replace `preview_data: Record<string, unknown>` with:
  ```ts
  type TemplatePreviewData = {
    nodes?: SignalNode[];
    edges?: Array<{ source: string; target: string }>;
    sample_output?: unknown[];
  };
  ```

Step 5 — Fix Callsites
  Run `pnpm tsc --noEmit` and fix all type errors introduced by the narrower types.
  Use type guards where discriminated union narrowing is needed:
    if (node.type === 'filter') { // node.config is now FilterNodeConfig }

Step 6 — Verify
  `pnpm tsc --noEmit` passes with zero errors.
  `pnpm build` succeeds.
```

---

## Dependencies

- None (pure type refactor, no runtime changes)

---

## Acceptance Criteria

- [ ] No `Record<string, unknown>` in DataSource, SignalNode, or Template config fields
- [ ] Discriminated unions defined for all major variant types
- [ ] All callsites updated to use narrowed types or type guards
- [ ] `pnpm tsc --noEmit` passes with zero errors
- [ ] `pnpm build` succeeds
- [ ] No `as any` or `as unknown` casts introduced
