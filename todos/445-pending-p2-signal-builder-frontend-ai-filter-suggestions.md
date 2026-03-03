# TODO-445: AI-Assisted Filter Suggestions in Signal Builder

**Repo:** signal-builder-frontend  
**Priority:** P2  
**Effort:** Large (1-2 weeks)  
**Created:** 2026-03-03

## Description

Add LLM-powered prompt input to the signal builder canvas. Advisor types natural language like "find growth stocks with momentum > 20%" and the system auto-populates filter nodes on the canvas.

## Motivation

- Major UX differentiator vs competitors
- Reduces time-to-signal from minutes to seconds
- Increases retention: advisors return to iterate signals
- Directly drives revenue: premium feature for enterprise tier

## Coding Prompt

```
Implement AI-assisted filter suggestions in signal-builder-frontend.

1. Add new component: src/modules/builder/containers/AIPromptBar/AIPromptBar.tsx
   - Floating input bar above the canvas (similar to GitHub Copilot chat)
   - Text input: "Describe your signal in plain English..."
   - Submit button + loading state
   - Dismissible

2. Connect to backend:
   - POST /api/v1/signals/ai-suggest with { prompt: string }
   - Response: { nodes: NodeConfig[], edges: EdgeConfig[], confidence: number }
   - Use React Query useMutation

3. Canvas integration in BuilderContainer:
   - On suggestion received, dispatch to Redux: addAISuggestedNodes(nodes, edges)
   - Show suggested nodes with a different color/border (dashed) indicating AI origin
   - "Accept All" / "Accept Selected" / "Discard" toolbar appears
   - On accept: convert to normal nodes

4. Add to LayoutWithNav: AIPromptBar renders when on /builder route

5. Track with Sentry: custom event 'ai_suggestion_accepted' / 'ai_suggestion_discarded'

6. Write Storybook story for AIPromptBar with mock responses
```

## Acceptance Criteria

- [ ] Natural language input generates filter nodes on canvas
- [ ] AI nodes visually distinct from manually-added nodes
- [ ] Accept/discard workflow works without data loss
- [ ] Loading/error states handled
- [ ] Sentry tracking fires on accept/discard
- [ ] Storybook story with mock data

## Dependencies

- signal-builder-backend must implement /api/v1/signals/ai-suggest endpoint
- TODO-379 (lodash cleanup) — independent
