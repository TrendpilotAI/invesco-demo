# TODO-711: Complete OracleVectorService Implementation

**Repo**: signal-studio-frontend  
**Priority**: P0  
**Effort**: L (3-5 days)  
**Status**: pending

## Description
The `OracleVectorService` in `/lib/oracle/vector-service.ts` is a skeletal placeholder. Oracle 23ai vector search is the core differentiator for Signal Studio. This task completes the implementation.

## Coding Prompt
```
Implement OracleVectorService in /data/workspace/projects/signal-studio-frontend/lib/oracle/vector-service.ts

Requirements:
1. Create DDL scripts in /scripts/oracle-ddl/ for:
   - SIGNAL_VECTORS table with VECTOR(1536) column (Oracle 23ai)
   - HNSW index on the vector column for approximate nearest neighbor search
   - Sequence and trigger for auto-incrementing IDs

2. Implement these methods in OracleVectorService:
   - testConnection(): Promise<{success: boolean, message: string}>
   - vectorizeSignals(signals: Signal[]): Promise<{inserted: number, failed: number}>
     - Call OpenAI embeddings API (text-embedding-3-small) for each signal's name+description
     - Store embedding vectors in SIGNAL_VECTORS table
   - searchSimilar(query: string, limit?: number): Promise<SimilarSignal[]>
     - Generate embedding for query
     - Use Oracle 23ai vector_distance() function for cosine similarity search
     - Return top N results with scores

3. All Oracle SQL must use oracledb's bind variables (no string interpolation)
4. Add TypeScript types for all inputs/outputs
5. Export from lib/oracle/index.ts

Dependencies: oracledb, @ai-sdk/openai (for embeddings)
```

## Acceptance Criteria
- [ ] DDL scripts exist and can be run on Oracle 23ai
- [ ] vectorizeSignals() successfully inserts records with real embeddings
- [ ] searchSimilar() returns ranked results via vector cosine distance
- [ ] All methods have TypeScript return types (no `any`)
- [ ] Unit tests exist in `__tests__/lib/oracle/vector-service.test.ts` with mocked oracledb
