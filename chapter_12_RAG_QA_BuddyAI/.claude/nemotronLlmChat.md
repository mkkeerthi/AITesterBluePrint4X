# QABuddy: Hybrid RAG for QA Engineers

## Architecture Overview

This is a hybrid Retrieval-Augmented Generation system that combines multiple retrieval methods to answer QA-related questions across diverse knowledge sources.

Core Retrieval Pipeline

1. Dense Embeddings (qabuddy/embed.py):
   - Qwen3-Embedding model via Ollama (1024-dimensional vectors)
   - Instruction-aware query encoding: "Instruct: ...\nQuery: {question}"
   - Used for semantic meaning matching
2. Sparse BM25 (qabuddy/sparse.py):
   - Code-aware tokenizer that preserves identifiers, ticket IDs (VWO-26), file names
   - Light stemmer consistent with browser demo (ui/src/bm25.js)
   - TF-IDF weighted, hashed to uint32 indices
   - Handles camelCase, dotted paths, and technical identifiers
3. RRF Fusion (qabuddy/store.py):
   - Qdrant's Reciprocal Rank Fusion combines dense and sparse results
   - Single batched query with three query types: dense-only, sparse-only, fused RRF
4. Cross-Encoder Reranking (qabuddy/rerank.py):
   - sentence-transformers.CrossEncoder for precision
   - Runs question+candidate together for better relevance judgment
   - Default: cross-encoder/ms-marco-MiniLM-L-6-v2
5. Exact ID Lookup (qabuddy/store.py):
   - Direct fetch of JIRA keys (VWO-26, LOGIN-002) and test case IDs
   - Bypasses search for known identifiers

Data Ingestion Pipeline

From qabuddy/ingest.py:
- Sources defined in sources.yaml (8 kinds: testcases, jira, docs, transcript, diagram, logs, code, figma)
- Chunks per kind using appropriate chunker:
  - Code (Java/TS/JS): AST-aware splitting by methods/classes/scopes
  - Docs (PDF/MD): Heading-aware section chunking with merge/split logic
  - Jira: Ticket body + per-comment chunks
  - Testcases: CSV/XLSX row-based
  - Logs: Failure windows, build summaries, flaky test detection
  - Transcripts: Speaker turns with overlap
  - Diagrams: Shape/edge data from Lucid exports
- Incremental indexing: SHA256 manifest tracks changes; only re-indexes modified files
- Vector storage: Qdrant with dense (1024D cosine) + sparse (BM25 with IDF) vectors

Answer Generation

qabuddy/answer.py:
- Modes: ask, rca, test_design, triage, code, rtm - each with source quotas and instructions
- Citation rules: Inline [1], [2][3] format only; no 【】 or line ranges
- Token budgeting: Water-filling algorithm across sources
- LLM: Groq by default, pluggable (Ollama, OpenAI)
- Rewrite: Conversation follow-ups converted to standalone search queries

Key Design Decisions

┌──────────────────────┬──────────────────────────────────────────────────────────────────────────────────────────────┐
│       Feature        │                                    Why it matters for QA                                     │
├──────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────┤
│ Code-aware BM25      │ QA questions use identifiers (TimeoutException, WaitHelpers.java) that prose tokenizers miss │
├──────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────┤
│ Exact ID lookup      │ Engineers constantly reference VWO-26, LOGIN-002 etc. - must fetch directly                  │
├──────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────┤
│ Per-source quotas    │ Prevent 500 test case rows from crowding out a single PRD section                            │
├──────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────┤
│ Water-filling tokens │ Long docs get proportionally more context; short docs keep full length                       │
├──────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────┤
│ Modes with quotas    │ RCA needs both jenkins + jira + meeting_notes; RTM needs requirements + test_cases           │
└──────────────────────┴──────────────────────────────────────────────────────────────────────────────────────────────┘

Evaluation

- 38 test cases in eval/golden.yaml covering citation counting, tokenizer agreement, JIRA parsing, doc chunking, log analysis, code chunking, transcripts
- Runs headless: pytest -q (no Qdrant/Ollama/LLM needed)

The system is well-engineered for the QA domain, carefully balancing recall (hybrid BM25 + dense) with precision (cross-encoder reranking), and paying special attention to the identifier-heavy language QA engineers use in their daily work.

## Qdrant collection decision

❯ i am creating new collection in qdrant what is the suitable use case for this project Global search or Multitenancy?

  Thought for 43s

Based on my analysis of the QABuddy project, Global search (single collection) is the suitable approach for your Qdrant setup. Here's why:

Why Global Search (Single Collection) fits QABuddy

1. Cross-source queries are core to the use case

The project's modes explicitly require integrated searches across sources:
- RCA mode: Needs jenkins + jira + meeting_notes together
- RTM mode: Needs requirements + test_cases + jira together
- Test design: Compares requirements with test_cases across sources

These queries would be impossible with multitenancy (separate collections), as the system needs to correlate failures in Jenkins logs with Jira tickets and meeting notes in a single search.

2. RRF fusion works globally

The hybrid search uses Qdrant's Reciprocal Rank Fusion across all points in the collection, combining dense and sparse results. This fusion happens before any source filtering, meaning the best candidates from all sources are considered together.

3. Vector comparability

All chunks use the same embedding model (qwen3-embedding:0.6b, 1024-dim) and BM25 parameters. This means vectors from "code" chunks are directly comparable to vectors from "docs" chunks — essential for the hybrid reranking logic.

4. The quotas system operates within one collection

Per-source caps (e.g., max 2 test cases, max 3 requirements) are implemented via source_id payload filters within a single collection. The retrieve() function in qabuddy/retrieve.py shows this pattern extensively.

5. Incremental indexing is collection-aware

The manifest (manifest.json) tracks source_id per file and supports incremental re-ingestion. This is designed for a single collection that grows over time as new files are added to any source.

6. The project already assumes this model

- sources.yaml defines 8+ sources as part of one knowledge base
- config.py creates one collection: qdrant_url → qabuddy
- store.py hybrid() function takes source_ids as filter parameter (not as collection selector)
- store.py summaries() returns inventory chunks for given sources from one collection

When Multitenancy Would Be Better

Multitenancy (separate Qdrant collections per team/organization) makes sense when:
- Data isolation is critical (PII, compliance, different ownership)
- Different embedding models are used per tenant (vectors from different models aren't comparable)
- Complete workload isolation is needed (no cross-tenant queries ever)
- Multiple organizations share the same QABuddy instance

For QABuddy Specifically

Stick with the single qabuddy collection and use source_id filtering. The system is deliberately designed so that:

# Example: RCA mode queries across sources
quotas = {"jenkins": 2}  # Get best 2 from Jenkins source
r = retrieve("Why did build fail?", quotas=quotas)
# The cross-encoder reranks across ALL candidates, then per-source caps apply

The existing code already has all the plumbing for this — source_id payload filtering, per-source quotas, RRF fusion, and cross-encoder reranking all work within one collection.

Quick Setup Note

If you do need to create a new collection (e.g., for a different project), you can use the existing create_collection() function from qabuddy/store.py:

from qabuddy.store import create_collection
create_collection(recreate=False)  # Creates "qabuddy" collection with dense + sparse vectors

Or via direct Qdrant API to create a collection named differently with the same vector config (1024-dim dense + bm25 sparse).

Bottom line: This project is architected as a single hybrid knowledge base for a QA team. Global search with source_id filtering is the correct approach — multitenancy would break the core cross-source query functionality that makes QABuddy useful.