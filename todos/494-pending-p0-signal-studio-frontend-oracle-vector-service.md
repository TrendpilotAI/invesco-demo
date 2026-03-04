# TODO-494: Complete Oracle AI Vector Service Implementation

**Repo:** signal-studio-frontend  
**Priority:** P0  
**Effort:** XL (3-5 days)  
**Status:** pending

## Description
The core value proposition of Signal Studio is semantic search over financial signals using Oracle 23ai vector capabilities. Currently `lib/oracle/vector-service.ts`, `lib/oracle/semantic-search.ts`, `lib/oracle/embeddings.ts`, and the associated agents (`lib/agents/vectorization-agent.ts`, `lib/agents/semantic-search-agent.ts`) are skeletal placeholders per the MVP-FINAL-STATUS.md reality check.

## Coding Prompt
Complete the Oracle AI vector implementation:

1. **`lib/oracle/embeddings.ts`**: Implement `generateEmbeddings()` and `generateDocumentEmbeddings()` using either:
   - Oracle 23ai's built-in VECTOR_EMBEDDING (preferred, no external call)
   - OR OpenAI/Anthropic embeddings API as fallback
   
2. **`lib/oracle/vector-service.ts`**: Implement `OracleVectorService`:
   - `vectorizeSignals(signals: SignalRec[])` — upsert vectors to SIGNAL_VECTORS table
   - `vectorizeClients(clients: ClientRec[])` — upsert to CLIENT_VECTORS table
   - `similaritySearch(embedding: number[], tableName: string, topK: number)` — VECTOR_DISTANCE query
   
3. **`lib/oracle/semantic-search.ts`**: Implement `SemanticSearchService`:
   - `searchSignals(query: string)` — embed query, run similarity search
   - `searchByClientProfile(clientId: string)` — find signals matching client attributes
   
4. **`scripts/setup-oracle-vectors.sql`**: Finalize DDL — ensure VECTOR columns are defined with correct dimensions (1536 for OpenAI, 768 for Oracle built-in)

5. **`app/api/chat/insights/route.ts`**: Create missing insights endpoint that uses SemanticSearchService as RAG context for chat

6. **Tests**: Update `__tests__/lib/oracle-vector-service.test.ts` to test against real service (use mocks for Oracle conn in unit tests, real DB in integration)

## Acceptance Criteria
- [ ] `pnpm test:vectorization` passes without errors
- [ ] `pnpm test:semantic-search` returns relevant results for test queries
- [ ] Chat `/api/chat/insights` returns AI response with signal context
- [ ] Vector similarity search returns top-5 signals for a sample query

## Dependencies
- Oracle 23ai database connection working (ORACLE_USER, ORACLE_PASSWORD, ORACLE_CONNECT_STRING)
- Oracle Instant Client installed
