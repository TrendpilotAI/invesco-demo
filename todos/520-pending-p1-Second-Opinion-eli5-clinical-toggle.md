# TODO 520: ELI5 ↔ Clinical Language Toggle
**Repo:** Second-Opinion  
**Priority:** P1 — Quick Win  
**Effort:** 3h  
**Status:** pending

## Description
The analysis pipeline already produces both consumer-friendly and clinical outputs. Adding a toggle lets users (and Kaggle judges) flip between "Plain English" and "Doctor Language" — massive demo impact for minimal effort.

## Coding Prompt
```
In /data/workspace/projects/Second-Opinion/components/:

1. Add a LanguageToggle component: two-button toggle "🧑 Plain English" | "👨‍⚕️ Clinical"
2. Add to SecondOpinionScore.tsx and ReasoningChain.tsx
3. Pass toggle state via local React state (no global store needed)
4. In SecondOpinionScore: show consumer_summary when "Plain English", clinical_analysis when "Clinical"
5. Animate transition with framer-motion (already installed)
6. Default to "Plain English" for new users
```

## Acceptance Criteria
- [ ] Toggle visible in results view
- [ ] Smooth animated transition between modes
- [ ] Plain English: jargon-free, empathetic language
- [ ] Clinical: technical terminology, ICD codes if present
- [ ] State persists within session (not across sessions)

## Dependencies
None
