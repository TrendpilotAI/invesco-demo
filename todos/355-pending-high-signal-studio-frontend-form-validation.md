# TODO 355 — Signal Studio Frontend: Auth Form Validation (Zod + React Hook Form)

**Status:** pending  
**Priority:** high  
**Project:** signal-studio-frontend  
**Estimated Effort:** 4–6 hours  

---

## Description

Auth pages (login, signup, forgot-password) currently use raw uncontrolled inputs with no validation. This creates security and UX risks — invalid emails pass through, weak passwords are accepted, and error messages are absent. This task introduces Zod schemas and React Hook Form across all three auth pages.

---

## Coding Prompt (Autonomous Agent)

```
Repo: /data/workspace/projects/signal-studio-frontend

Task: Add Zod + React Hook Form validation to all auth pages.

Dependencies to install (if not already present):
  pnpm add zod react-hook-form @hookform/resolvers

Steps:
1. Create `src/lib/validations/auth.ts` with three Zod schemas:
   - `loginSchema`: email (valid email), password (min 8 chars)
   - `signupSchema`: email, password, confirmPassword (must match password),
     full_name (min 2 chars)
   - `forgotPasswordSchema`: email (valid email)

2. Refactor `src/app/(auth)/login/page.tsx`:
   - Replace raw inputs with `<input {...register('field')} />`
   - Add `<p>{errors.field?.message}</p>` under each field
   - Use `handleSubmit` from useForm with the loginSchema resolver
   - Show a form-level error if Supabase auth returns an error

3. Apply the same pattern to signup and forgot-password pages.

4. Extract a shared `FormField` component to `src/components/ui/FormField.tsx`
   that renders label + input + error message to eliminate duplication.

5. Ensure all forms display inline error messages in red below each input.

6. Run `pnpm tsc --noEmit` and fix any type errors.

7. Run `pnpm build` and verify success.

Constraints:
- Do not change the visual design of the auth pages beyond adding error text.
- Keep Supabase auth calls exactly as-is; only add client-side validation before submission.
- The FormField component must accept `register`, `error`, `label`, `type`, `name` props.
```

---

## Dependencies

- None

---

## Acceptance Criteria

- [ ] Login, signup, forgot-password pages all validate inputs before submitting
- [ ] Inline error messages appear under each invalid field
- [ ] Form submission is blocked when validation fails
- [ ] `FormField` shared component exists and is used by all three auth pages
- [ ] `pnpm tsc --noEmit` passes
- [ ] `pnpm build` succeeds
