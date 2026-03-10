# 867 — Fix 83 any-types in lib/ — TypeScript Strict Compliance

**Repo:** signal-studio  
**Priority:** P1 — High  
**Effort:** 3 days  
**Status:** pending

## Problem
There are 83 occurrences of `: any`, `<any>`, and `as any` across `lib/` TypeScript files. This:
- Disables TypeScript's type checking on these code paths
- Hides potential runtime errors (Oracle query results, AI SDK responses)
- Prevents safe refactoring

## Key Files to Fix
```bash
grep -rn ": any\b\|<any>\|as any" lib/ --include="*.ts"
```

Top files:
- `lib/agents/chat-rag-agent.ts`
- `lib/agents/vectorization-agent.ts`
- `lib/agents/oracle-ai-agent.ts`
- `lib/agents/semantic-search-agent.ts`
- `lib/agents/control-plane-agent.ts`

## Common Patterns to Fix

### Oracle DB Result Rows
```typescript
// Before:
const result = await connection.execute(sql)
const rows: any[] = result.rows ?? []

// After:
interface SignalRow {
  SIGNAL_ID: string
  NAME: string
  DESCRIPTION: string
  CATEGORY: string
}
const result = await connection.execute<SignalRow[]>(sql)
const rows = result.rows ?? []
```

### AI SDK Responses
```typescript
// Before:
const response: any = await generateText({ model, messages })

// After:
import { GenerateTextResult } from 'ai'
const response: GenerateTextResult = await generateText({ model, messages })
```

### Oracle Vector Results
```typescript
// Before:
const vectors: any[] = await getEmbeddings(texts)

// After:
type Embedding = number[]
const vectors: Embedding[] = await getEmbeddings(texts)
```

## Coding Prompt (for autonomous agent)
```
1. Run: grep -rn ": any\b\|<any>\|as any" /data/workspace/projects/signal-studio/lib/ --include="*.ts"
2. For each occurrence, determine the actual runtime type and create a proper TypeScript interface
3. Common interfaces to create:
   - OracleRow: Oracle DB result row type
   - SignalRow: Signal table row
   - VectorRow: Vector search result row
   - ChatMessage: AI chat message type
   - EmbeddingVector: number[] type alias
4. Replace all any types with proper interfaces
5. Run: pnpm tsc --noEmit to verify no new errors
6. Run: pnpm test to verify all tests pass
```

## Acceptance Criteria
- [ ] `grep -rn ": any\b\|<any>\|as any" lib/` returns 0 results (or only justified `as any` with comment)
- [ ] `pnpm tsc --noEmit` passes
- [ ] All existing tests pass
- [ ] No runtime behavior changes

## Dependencies
- Should be done BEFORE #868 (remove ignoreBuildErrors)
