# TODO-895: Replace Hand-Rolled Validation with Zod
**Repo:** signalhaus-website  
**Priority:** P2  
**Status:** pending  
**Effort:** 1h

## Problem
`/src/app/api/contact/route.ts` contains 50+ lines of manual validation logic (`validateContact()`). This is error-prone, verbose, and not reusable on the client side. Using Zod provides:
- Shared types between client and server
- Better error messages
- Fewer lines of code
- Type inference

## Task
Replace `validateContact()` with a Zod schema and share the type with ContactForm.tsx.

## Coding Prompt
```
In /data/workspace/projects/signalhaus-website:

1. Install Zod:
   npm install zod

2. Create src/lib/schemas.ts:
   import { z } from 'zod'
   
   const BUDGET_OPTIONS = ['Under $10K', '$10K–$50K', '$50K–$150K', '$150K+', 'Not sure'] as const
   const XSS_PATTERNS = [/<script/i, /javascript:/i, /on\w+=/i]
   
   function noXss(val: string) {
     return !XSS_PATTERNS.some(p => p.test(val))
   }
   
   export const contactSchema = z.object({
     name: z.string()
       .min(1, 'name is required')
       .max(100)
       .refine(noXss, 'Input contains disallowed content'),
     email: z.string()
       .min(1, 'email is required')
       .email('email is invalid')
       .max(254)
       .transform(v => v.toLowerCase()),
     company: z.string().max(200).optional(),
     budget: z.enum(BUDGET_OPTIONS).optional(),
     message: z.string()
       .min(10, 'message must be at least 10 characters')
       .max(5000)
       .refine(noXss, 'Input contains disallowed content'),
   })
   
   export type ContactInput = z.infer<typeof contactSchema>

3. Update src/app/api/contact/route.ts:
   - Remove validateContact() function and ContactInput/ValidationResult interfaces
   - Import contactSchema from src/lib/schemas
   - Replace validateContact(rawBody) call with:
     const result = contactSchema.safeParse(rawBody)
     if (!result.success) {
       return NextResponse.json(
         { error: 'Validation failed', details: result.error.flatten().fieldErrors },
         { status: 422 }
       )
     }
     const { name, email, company, budget, message } = result.data

4. Update src/app/contact/ContactForm.tsx:
   - Import ContactInput from src/lib/schemas
   - Type the form state using ContactInput
```

## Dependencies
- Should be done after TODO-894 (Vitest tests) so tests catch regressions

## Acceptance Criteria
- validateContact() function removed from route.ts
- Zod schema in src/lib/schemas.ts
- ContactForm.tsx typed using Zod inference
- All existing behavior preserved (same validation rules, same error messages)
- `npm run typecheck` passes
