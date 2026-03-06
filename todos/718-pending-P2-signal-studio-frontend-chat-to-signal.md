# TODO-718: Chat-to-Signal Natural Language Builder

**Repo**: signal-studio-frontend  
**Priority**: P2  
**Effort**: XL (1-2 weeks)  
**Status**: pending

## Description
High-value feature: user types natural language description → system generates a complete signal definition (ReactFlow graph + SQL). Core AI differentiation for Signal Studio.

## Coding Prompt
```
Implement Chat-to-Signal feature in signal-studio-frontend:

1. New API Route: POST /api/signals/generate
   Input: { description: string, availableTables?: string[] }
   
   System prompt:
   "You are a financial signal builder. Given a natural language description, 
   generate a signal definition as JSON with:
   - name: signal name
   - description: cleaned description  
   - nodes: array of ReactFlow nodes (filter, aggregation, join, output types)
   - edges: array of ReactFlow edges connecting nodes
   - sql: equivalent Oracle SQL query
   
   Available node types: FilterNode, AggregationNode, JoinNode, SortNode, OutputNode
   Each node has: id, type, data (config), position
   
   Return ONLY valid JSON, no explanation."
   
   Use Vercel AI SDK streamObject() with a Zod schema for structured output.

2. UI Component: components/signal-generator/signal-generator-input.tsx
   - Chat-style input: "Describe the signal you want to create..."
   - Shows generation progress (streaming)
   - Preview of generated graph before saving
   - "Looks good, save it" / "Let me refine it" buttons

3. Integration with Visual Builder:
   - Generated nodes/edges can be loaded into the ReactFlow editor for manual refinement
   - Add "Generate with AI" button to visual builder toolbar

4. Refinement Loop:
   - User can say "change the revenue threshold to 2M" 
   - System updates the existing signal definition
   - Maintains conversation context for multi-turn refinement
```

## Acceptance Criteria
- [ ] User can describe signal in plain English and get a working signal definition
- [ ] Generated signal loads correctly in visual builder for editing
- [ ] Generated SQL is valid Oracle syntax
- [ ] Multi-turn refinement works ("change X to Y")
