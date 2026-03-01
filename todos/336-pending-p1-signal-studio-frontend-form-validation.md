# TODO-336: Add Form Validation to Auth Pages

**Repo:** signal-studio-frontend  
**Priority:** P1  
**Effort:** S (2-4 hours)  
**Dependencies:** none

## Description
Auth pages (login, signup, forgot-password) use raw `<input>` elements with no validation. Add zod schemas + react-hook-form for client-side validation with inline error messages.

## Coding Prompt
```
In /data/workspace/projects/signal-studio-frontend/:

1. Install: npm install zod react-hook-form @hookform/resolvers

2. Create src/lib/validators/auth.ts with zod schemas:
   - loginSchema: email (valid email), password (min 8 chars)
   - signupSchema: email, password, confirmPassword (must match), fullName (min 2 chars)
   - forgotPasswordSchema: email

3. Update src/app/(auth)/login/page.tsx:
   - Replace raw inputs with react-hook-form Controller or register
   - Show inline errors below each field
   - Disable submit button while submitting
   - Show server errors (wrong password etc) from Supabase

4. Update src/app/(auth)/signup/page.tsx similarly

5. Update src/app/(auth)/forgot-password/page.tsx similarly

6. Add loading spinner to submit buttons during async operations
```

## Acceptance Criteria
- [ ] Login form shows errors for invalid email / short password
- [ ] Signup shows error when passwords don't match
- [ ] Submit buttons disabled during submission
- [ ] Server errors displayed under form
- [ ] TypeScript strict, no `any`
