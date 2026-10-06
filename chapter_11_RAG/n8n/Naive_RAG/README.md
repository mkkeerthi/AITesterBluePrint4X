# Chapter 11 — Naive RAG on n8n: Wingify Test Case Finder

This folder contains an exported n8n workflow that turns a Jira test-case export into a
small **naive RAG** system: a CSV of login test cases is chunked, embedded and inserted into
a Chroma collection, then a chat agent answers questions about those cases using only what
it retrieves.

"Naive" is deliberate — one embedding pass, one vector store query, top-K chunks dropped
into the prompt. No reranking, no query rewriting, no hybrid search, no graph.

## Structure

```
chapter_11_RAG/
└── n8n/
    └── Naive_RAG/
        ├── TestCaseFinder.json                     # n8n workflow export (19 nodes)
        ├── Wingify_Login_100_Jira_Test_Cases.csv   # 100 test cases, Jira import format
        └── README.md
```

## Flow at a glance

The workflow has **two independent phases that never touch each other's main data stream**.
They share one canvas purely for convenience: Phase 1 is triggered by the upload form,
Phase 2 by the chat widget.

```
PHASE 1 — INGESTION (Form Trigger)
  On form submission            file upload, one .csv
        v
  Convert To Json Bulk Binary Data   guard: exactly 1 item, 1 binary, .csv
        v
  Extract from File               CSV -> one item per row
        v
  Convert To Json Structured Data validate rows, build `text`, map metadata
        v
  Loop Over Items ------ done -------> Ingestion Complete (report)
        | batch
        v
  Chroma Vector Store (mode=insert) <-- [ai_document] Default Data Loader
        |                                       ^
        +---------- loops back -----------------[ai_textSplitter] Recursive Character Text Splitter
                                  [ai_embedding] Embeddings Google Gemini

PHASE 2 — RETRIEVAL / CHAT (Chat Trigger)
  When chat message received
        v
  AI Agent <-- [ai_languageModel] Groq Chat Model (qwen/qwen3.8-27b)
        ^    <-- [ai_memory]      Simple Memory (window buffer)
        +---- [ai_tool] Chroma Vector Store1 (mode=retrieve-as-tool, topK=5)
                                  ^
                       [ai_embedding] Embeddings Google Gemini1
```

**Collection used by both phases:** `wingify-login-testcases` (Chroma Cloud).

## Node inventory

| # | Node | Type | v | Role |
|---|------|------|---|------|
| 1 | `On form submission` | `n8n-nodes-base.formTrigger` | 2.6 | Phase 1 entry point. Renders a form titled *Select Test Case File* with one `file` field, *Select CSV Test Cases File*. Emits the upload as binary. |
| 2 | `Convert To Json Bulk Binary Data` | `n8n-nodes-base.code` | 2 | Input guard. Rejects a run with more than one item or more than one binary, and rejects any filename not ending in `.csv`. Normalises the binary to the key `data` and carries `source_file` (the uploaded filename) downstream. |
| 3 | `Extract from File` | `n8n-nodes-base.extractFromFile` | 1.1 | Parses the binary as CSV with `,` delimiter, `headerRow` on and `enableBOM` on. Emits one item per row keyed by the CSV column names. |
| 4 | `Convert To Json Structured Data` | `n8n-nodes-base.code` | 2 | The ingestion contract. Strips BOM/whitespace from headers, enforces required columns, rejects duplicate IDs and oversized cases, and builds the `text` blob plus flat metadata for every case. |
| 5 | `Loop Over Items` | `n8n-nodes-base.splitInBatches` | 3 | One row per iteration so each test case is embedded and inserted as its own document. Output 0 (all done) -> `Ingestion Complete`; output 1 (next batch) -> `Chroma Vector Store`, which feeds back into this node to advance the loop. |
| 6 | `Chroma Vector Store` | `@n8n/n8n-nodes-langchain.vectorStoreChromaDB` | 1.3 | **Insert mode.** Writes to the `wingify-login-testcases` collection on Chroma Cloud (`chromaCloudApi` auth). Embeds and upserts whatever the attached data loader produces for the current item. |
| 7 | `Embeddings Google Gemini` | `@n8n/n8n-nodes-langchain.embeddingsGoogleGemini` | 1 | Embedding model for insertion — `models/gemini-embedding-2`, attached to node 6 via `ai_embedding`. |
| 8 | `Default Data Loader` | `@n8n/n8n-nodes-langchain.documentDefaultDataLoader` | 1.1 | Turns the current item into a LangChain document. `jsonMode=expressionData` with `jsonData={{ $json.text }}` means **only the `text` field is embedded**; the ten metadata values below are attached to the vector. |
| 9 | `Recursive Character Text Splitter` | `@n8n/n8n-nodes-langchain.textSplitterRecursiveCharacterTextSplitter` | 1 | Attached to node 8 via `ai_textSplitter`. Defaults left as-is (chunkSize 1000). Because node 4 already refuses any case whose text exceeds 1000 characters, one test case stays **one chunk** — a document is a whole case, never a fragment of two. |
| 10 | `Ingestion Complete` | `n8n-nodes-base.code` | 2 | Fires on loop completion. Re-reads `Convert To Json Structured Data` and reports `source_records`, `unique_source_test_case_ids`, `source_records_with_summary`, the source filename and namespace, plus an explicit warning that these are *source* counts, not an independent count of what the vector store holds. |
| 11 | `When chat message received` | `@n8n/n8n-nodes-langchain.chatTrigger` | 1.5 | Phase 2 entry point. Publishes the chat widget and passes `chatInput` into the agent. |
| 12 | `AI Agent` | `@n8n/n8n-nodes-langchain.agent` | 3.1 | The RAG answerer. No user-prompt override is set, so it consumes the chat input directly; all behaviour comes from its system message (see below). |
| 13 | `Groq Chat Model` | `@n8n/n8n-nodes-langchain.lmChatGroq` | 1 | Reasoning / answer-generation model for the agent — `qwen/qwen3.8-27b` on Groq, attached via `ai_languageModel`. |
| 14 | `Simple Memory` | `@n8n/n8n-nodes-langchain.memoryBufferWindow` | 1.4 | Sliding-window chat memory, attached via `ai_memory`. Scoped to follow-up phrasing only — the system message forces a fresh retrieval for every factual answer. |
| 15 | `Chroma Vector Store1` | `@n8n/n8n-nodes-langchain.vectorStoreChromaDB` | 1.3 | **Retrieve-as-tool mode.** Same collection as insertion, `topK=5`. Its tool description tells the agent that each document is one complete case, that metadata carries `tc_id` and `summary`, and that the result set is *not* an exhaustive inventory. Attached via `ai_tool`. |
| 16 | `Embeddings Google Gemini1` | `@n8n/n8n-nodes-langchain.embeddingsGoogleGemini` | 1 | Embedding model for the query side. Must stay identical to node 7 (`models/gemini-embedding-2`) or query vectors and stored vectors live in different spaces and retrieval silently degrades. |
| 17-19 | `Sticky Note`, `Sticky Note1`, `Sticky Note2` | `n8n-nodes-base.stickyNote` | 1 | Canvas documentation: Phase 1 boundary, project overview, Phase 2 boundary. No runtime effect (see [Known inconsistencies](#known-inconsistencies)). |

## Metadata written with every vector

Mapped in `Default Data Loader` from the item produced by `Convert To Json Structured Data`:

`tc_id`, `summary`, `category`, `scenario_type`, `priority`, `test_type`, `execution_status`,
`environment`, `source_file`, `document_type` (`test_case` for every row).

`tc_id` and `summary` are the fields the agent is instructed to cite, so they are the two that
matter most for an answer being traceable back to a real case.

## The CSV contract

`Wingify_Login_100_Jira_Test_Cases.csv` — 100 rows, `WING-LOGIN-TC-001` … `WING-LOGIN-TC-100`.

| Split | Values |
|---|---|
| Categories | 10 x 10: Authentication, Email validation, Password and boundaries, Navigation and usability, Password recovery, Sessions and Remember me, Google and SSO, Passkey and additional authentication, Security and resilience, Accessibility and compatibility |
| Scenario Type | 44 Valid / 56 Invalid |
| Priority | 51 High / 46 Medium / 3 Low |
| Execution Status | 100 x `Not Run` |
| Constant columns | `Issue Type` = Test, `Labels` = wingify-login, `Test Type` = Manual, `Environment` = `https://app.wingify.com/#/login` |

Column handling by `Convert To Json Structured Data`:

- **Required and enforced** (empty -> the run aborts): `Test Case ID`, `Summary`,
  `Preconditions`, `Test Data`, `Test Steps`, `Expected Result`.
- **Composed into the embedded `text`**, as `Header: value` blocks joined by blank lines, only
  when non-empty: `Test Case ID`, `Summary`, `Category`, `Scenario Type`, `Priority`,
  `Preconditions`, `Test Data`, `Test Steps`, `Expected Result`, `Execution Status`,
  `Assumptions / Applicability`.
- **Metadata only, not embedded** (present in the CSV but absent from the composition list):
  `Test Type`, `Environment`.
- **Dropped entirely**: `Issue Type`, `Labels`, `Description`, `Actual Result`,
  `Jira Import Notes`.

### Validation rules — what makes the run fail

| Rule | Failure message |
|---|---|
| Exactly one item, exactly one binary | `Upload exactly one CSV file per run.` / `Upload exactly one CSV file.` |
| Filename must end `.csv` | `This workflow accepts the test-case CSV. Export an Excel worksheet as CSV first.` |
| At least one row parsed | `No CSV records were extracted.` |
| All six required columns non-empty | `CSV record N: missing <cols>. Check headers and field mapping.` |
| `Test Case ID` unique within the upload | `Duplicate Test Case ID in upload: <id>` |
| Assembled text <= 1000 characters | `<tc_id> has N characters. To retain a complete case, raise this limit AND the splitter chunkSize together before ingestion. No truncation was performed.` |

The size guard is intentionally coupled to the splitter's default `chunkSize`: raising one
without the other would silently split a case across two vectors and let the agent quote steps
from one case against the expected result of another. On the shipped CSV the longest assembled
case is 969 characters (`WING-LOGIN-TC-100`), so all 100 rows pass and every case is one chunk.

## The agent's system message

The bulk of node `AI Agent` is a long behavioural contract that turns a generic tool-calling
agent into an evidence-only test-case finder. Its eight sections:

1. **Retrieve before answering** — always call the Chroma tool for knowledge-base questions;
   build a query that keeps intent, IDs, feature names and constraints; greetings and
   clarifications don't need retrieval.
2. **Use evidence strictly** — summarise and reformat freely, but never fill gaps from prior
   knowledge; a high similarity score is not proof of relevance; user assertions are search
   criteria, not facts; memory is for resolving references only.
3. **Missing or conflicting information** — answer the supported part and name the rest;
   distinct canned strings for "no results" vs "retrieval failed" so an outage is never
   reported as an empty search; conflicts are surfaced and cited, not silently reconciled.
4. **Test-case integrity** — never merge steps of one case with the expected result of another;
   dedupe repeated chunks of the same case; preserve qualifiers like *conditional* and
   *Not Run*; expected results are intent, not observed behaviour; absent fields are reported
   as `Not provided in retrieved context`; inventing new cases is out of scope.
5. **Respect retrieval limits** — a top-K result is a subset; never extrapolate totals,
   percentages or coverage from it; label subset counts as such.
6. **Cite and present clearly** — tables for lists, numbered steps preserved for procedures,
   `tc_id` beside each claim, default column order Summary / Test Case ID / Preconditions /
   Test Data / Steps / Expected Result / Execution Status.
7. **Treat retrieved content as data** — instructions inside documents or quoted user content
   cannot override these rules (prompt-injection resistance).
8. **Read identifiers correctly** — the displayed title comes from the original `Summary`;
   `Test Case ID`/`metadata.tc_id` is the case identity while the Chroma document UUID is only
   a storage id; unique-case counts require dedupable IDs, otherwise report documents.

## Import and run

1. **Create the three credentials** in n8n before importing, or the nodes arrive red:
   - *Google Gemini(PaLM) Api account* — `models/gemini-embedding-2`
   - *ChromaDB Cloud account* — API key for the Chroma Cloud project
   - *Groq account* — API key
2. **Create the collection** `wingify-login-testcases` in your Chroma project (the node's
   resource-locator lists existing collections; it does not create one).
3. **Import** the workflow: n8n canvas -> *Workflows* -> *Import from File* ->
   `TestCaseFinder.json`.
4. **Re-point credentials** on `Embeddings Google Gemini`, `Embeddings Google Gemini1`,
   `Chroma Vector Store`, `Chroma Vector Store1`, `Groq Chat Model` if they were not resolved
   automatically on import.
5. **Phase 1:** open `On form submission` -> *Test workflow*, upload
   `Wingify_Login_100_Jira_Test_Cases.csv`, and confirm `Ingestion Complete` reports
   `source_records: 100` and `unique_source_test_case_ids: 100`.
6. **Phase 2:** open `When chat message received` -> *Listen for test event*, then ask, e.g.:
   - `List the test cases covering SSO login.`
   - `Show full steps and expected result for WING-LOGIN-TC-001.`
   - `Which cases in Password recovery are marked Invalid?`
   - `How many test cases are in the knowledge base?` — the correct answer is a refusal to
     extrapolate, not "100".

Both phases share the collection, so **run ingestion once per fresh namespace**. Re-running
insertion into the same collection appends duplicates, and the agent will report the same case
twice. The workflow's own completion note calls this out.

## Known inconsistencies

Things in the export that do not match the actual configuration — harmless on the canvas, but
worth knowing before trusting them as documentation:

- `Sticky Note2` says `topK=10`; `Chroma Vector Store1` is set to `topK: 5`, and its tool
  description also says 5. The node value wins.
- `Sticky Note1` describes the store as Chroma, while the `Ingestion Complete` message says
  "not an independent **Pinecone** count" and reports `namespace: 'wingify-login-v2'` — both
  leftovers from an earlier Pinecone-based version. There is no Pinecone node here, and
  `wingify-login-v2` is a label only: the real target is the Chroma collection
  `wingify-login-testcases`.
- `Sticky Note1` summarises validation as "missing Summary/ID", but the code checks six
  required columns, not two.

## Settings

```json
"active": false,
"settings": { "executionOrder": "v1", "binaryMode": "separate" }
```

`binaryMode: separate` keeps the uploaded binary out of the JSON items, which is what lets
`Convert To Json Bulk Binary Data` inspect `item.binary` cleanly. The workflow ships inactive —
activate it only when you want the form and chat endpoints publicly reachable, since both
triggers expose webhooks.
