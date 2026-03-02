# TODO 389: Signal Studio Templates — Zod Schema Validation

**Priority:** P1  
**Repo:** signal-studio-templates  
**Effort:** M (1-2 days)  
**Status:** pending

---

## Description

Replace loose `Record<string, any>` parameter types with Zod runtime schemas. This catches invalid parameters at the API boundary with clear error messages instead of failing silently at SQL execution time. Also enables auto-generation of TypeScript types.

## Coding Prompt

```
Add Zod validation to signal-studio-templates:

1. Add zod to dependencies: pnpm add zod

2. New file: utils/schema-builder.ts
   - Function buildZodSchema(params: ParameterDef[]): z.ZodObject<any>
   - Maps each ParameterDef to its Zod equivalent:
     - type "string" → z.string()
     - type "number" → z.number().min(min).max(max)
     - type "date" → z.string().date() or z.coerce.date()
     - type "boolean" → z.boolean()
     - type "select" → z.enum(options.map(o => o.value))
     - type "multi-select" → z.array(z.enum(...))
     - required: false → .optional().default(defaultValue)

3. Update engine/template-engine.ts:
   - In validateParameters(): replace manual validation with Zod parse
   - Return Zod error messages formatted as ValidationError[]
   - Add type: export type TemplateParams<T extends SignalTemplate> = z.infer<ReturnType<typeof buildZodSchema>>

4. Update api/templates.ts:
   - Use Zod to validate request body before calling engine
   - Return 400 with Zod error details on validation failure

5. Add __tests__/schema-builder.test.ts:
   - Test each ParameterDef type maps to correct Zod type
   - Test required vs optional fields
   - Test min/max enforcement
   - Test select enum validation
```

## Acceptance Criteria
- [ ] `buildZodSchema()` utility function created
- [ ] All ParameterDef types have Zod equivalents
- [ ] `validateParameters()` uses Zod internally
- [ ] API returns Zod-formatted 400 errors
- [ ] Tests for schema builder
- [ ] No `Record<string, any>` for validated parameters
