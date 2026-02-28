# 315 · NarrativeReactor — README & Core Documentation

**Status:** pending  
**Priority:** high  
**Project:** NarrativeReactor  
**Effort:** ~2h  

---

## Task Description

NarrativeReactor has zero top-level README.md. New contributors and operators have no on-ramp. This task creates a comprehensive README plus a short CONTRIBUTING.md.

## Full Coding Prompt

```
You are working in /data/workspace/projects/NarrativeReactor/.

Create README.md at the repo root with the following sections:

1. **Project Overview** — AI-powered content generation platform (TypeScript/Express/Genkit).
   Services covered: video generation (Fal.ai), TTS (Fish Audio), social publishing (Blotato),
   campaigns, brand voice, competitor tracking, and 25+ more.

2. **Architecture Diagram** (ASCII) — show: web-ui (Next.js) → Express API → Genkit flows →
   32 services → external APIs (Fal.ai, Fish Audio, Blotato, Google Vertex AI).

3. **Prerequisites** — Node 20+, pnpm, required env vars (list every key from src/lib/env.ts).

4. **Quick Start**
   ```bash
   cp .env.example .env   # fill in keys
   pnpm install
   pnpm dev               # starts Express + Genkit dev server
   ```

5. **Project Structure** — src/services/, src/flows/, src/routes/, src/middleware/, web-ui/, dashboard/, tests/.

6. **Key Features** — one bullet per major service grouping.

7. **API Reference** — point to /docs or mention OpenAPI spec (TODO 318).

8. **Environment Variables** — table: VAR | Required | Description. Read src/lib/env.ts for the full list.

9. **Testing** — `pnpm test` runs Vitest suite.

10. **Deployment** — point to Railway/Docker (TODO 317).

11. **Contributing** — link to CONTRIBUTING.md.

Also create CONTRIBUTING.md with:
- Fork + branch conventions (feat/, fix/, chore/)
- Commit message format (conventional commits)
- PR checklist (tests pass, types compile, lint clean)
- How to add a new service (copy template in src/services/)
```

## Dependencies
- None (first task, no blockers)

## Acceptance Criteria
- [ ] `README.md` exists at repo root, all 11 sections present
- [ ] `CONTRIBUTING.md` exists
- [ ] Every env var from `src/lib/env.ts` is listed in the README table
- [ ] ASCII architecture diagram renders correctly in GitHub Markdown preview
- [ ] `pnpm build && pnpm test` still pass (docs only — no code change)
