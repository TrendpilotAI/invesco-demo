# TODO-832: Oracle Vector Pipeline Implementation

**Repo**: signal-studio-frontend  
**Priority**: P0  
**Effort**: L (3-5 days)  
**Status**: pending  
**Depends on**: None

## Description
MVP-FINAL-STATUS.md confirms Oracle vector tables, indexes, and deployment scripts are NOT implemented in production. This is the core MVP blocker blocking all AI/RAG features.

## Coding Prompt
```
1. Finalize scripts/setup-oracle-vectors.sql DDL:
   CREATE TABLE SIGNAL_VECTORS (
     id VARCHAR2(36) PRIMARY KEY,
     signal_id VARCHAR2(36),
     embedding VECTOR(1536, FLOAT32),
     content CLOB,
     created_at TIMESTAMP DEFAULT SYSTIMESTAMP
   );
   CREATE VECTOR INDEX signal_vectors_idx ON SIGNAL_VECTORS(embedding) USING HNSW;

2. In lib/oracle-vector-service.ts implement:
   - vectorize(text: string): Promise<number[]> — call OpenAI text-embedding-3-small
   - insert(signalId: string, text: string): Promise<void> — embed + store
   - search(query: string, limit?: number): Promise<SearchResult[]> — ANN search

3. Wire /app/api/vectorization/health/route.ts to real Oracle ping

4. Create /app/api/chat/insights/route.ts — AI chat with RAG context injection

5. Add unit tests in __tests__/lib/oracle-vector.test.ts (mock Oracle)

6. Add integration test that skips without ORACLE_CONNECT_STRING env var
```

## Acceptance Criteria
- `pnpm test:vectorization` passes
- `/api/vectorization/health` returns `{ status: 'ok', vectorCount: N }`
- `/api/chat/insights` endpoint returns AI response with signal context
- Unit tests pass without Oracle connection (mocked)
