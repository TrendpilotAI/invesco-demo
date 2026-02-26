# FlipMyEra — Clerk to Supabase Auth Migration

**Date:** 2026-02-18
**Commit:** 729443b
**Branch:** main
**Status:** ✅ Complete — build passes, 31/31 test files pass, pushed to GitHub

## What Changed

### New File
- **`src/core/integrations/supabase/auth.ts`** — Complete Supabase Auth module:
  - `SupabaseAuthProvider` — React context provider with session management
  - `useSupabaseAuth()` / `useAuth()` — Auth state hooks
  - Email/password sign-in and sign-up
  - Google OAuth via `signInWithOAuth`
  - Password reset flow (`resetPassword` + `updatePassword`)
  - Automatic session initialization and `onAuthStateChange` listener
  - Profile sync (creates profile + 3 free credits for new users)
  - Credit balance fetching with 30s cache TTL

### Removed
- `@clerk/clerk-react` and `@clerk/types` npm packages
- `src/integrations/supabase/clerk-client.ts`
- `src/modules/auth/contexts/ClerkAuthContext.fixed.tsx`
- `ClerkProvider` wrapper from `main.tsx`
- All `getToken({ template: 'supabase' })` calls → `getToken()`
- `createSupabaseClientWithClerkToken()` calls → direct `supabase` usage

### Updated (30+ files)
- **Supabase client** — enabled `persistSession`, `autoRefreshToken`, `detectSessionInUrl`
- **Auth components** — Auth.tsx (email/password forms + Google), AuthCallback.tsx, ResetPassword.tsx
- **Layout** — replaced `<SignedIn>`/`<SignedOut>` with `isAuthenticated` conditional
- **AuthDialog** — built-in sign-in/sign-up forms instead of Clerk modal buttons
- **StoryForm** — `<a href="/auth">` link replaces `<SignInButton>`
- **All consumer components** — switched from `@clerk/clerk-react` imports to `useSupabaseAuth`
- **Tests** — updated all mocks from `@clerk/clerk-react` to `@/core/integrations/supabase/auth`
- **Backward compat** — `useClerkAuth` re-exports `useSupabaseAuth` so existing imports still work

### Env Vars
- **Removed:** `VITE_CLERK_PUBLISHABLE_KEY`
- **Required:** `VITE_SUPABASE_URL`, `VITE_SUPABASE_PUBLISHABLE_KEY` (already existed)

## Edge Functions Note
The Supabase edge functions (`credits`, `credits-validate`, `create-checkout`, `groq-storyline`) extract user IDs from JWT `sub` claim. Supabase Auth tokens use the same JWT structure, so these should work without changes. However, **Supabase Auth user IDs are UUIDs** (not Clerk's `user_xxx` format), so any existing users with Clerk IDs in the database will need migration or the app will create new profiles.

## Next Steps
1. **Enable Google OAuth** in Supabase Dashboard → Authentication → Providers → Google
2. **Configure email templates** in Supabase for password reset, email confirmation
3. **User data migration** — existing Clerk user IDs (`user_xxx`) in profiles/user_credits tables won't match new Supabase Auth UUIDs. Plan a migration strategy.
4. **Remove VITE_CLERK_PUBLISHABLE_KEY** from all deployment environments (Vercel, etc.)
5. **Update RLS policies** if any reference Clerk JWT claims specifically
