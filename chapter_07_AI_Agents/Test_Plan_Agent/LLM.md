# Test Plan Agent — LLM.md (Project Constitution)

> Data schemas, behavioral rules, and architectural invariants.
> This is the source of truth for how the Test Plan Agent thinks and what it produces.

## Data schemas

### 1. Jira ticket (input)

```json
{
  "key": "PROJ-123",
  "summary": "string",
  "description": "string",
  "acceptance_criteria": "string"
}
```

- `key` — the Jira issue ID, matched via `\b([A-Z][A-Z0-9]+-\d+)\b`.
- `summary` — plain string from `fields.summary`.
- `description` — flattened from ADF `fields.description.content` to plain text.
- `acceptance_criteria` — best-effort scan of all `customfield_*` entries (string / ADF / checklist).

### 2. Config (input)

```json
{
  "jira_url": "https://your-domain.atlassian.net",
  "jira_email": "you@example.com",
  "jira_api_token": "secret",
  "groq_api_key": "secret",
  "groq_model": "openai/gpt-oss-120"
}
```

### 3. Test plan (output) — LOCKED schema

The output is the markdown document defined in `test_plan_template.md`. It has 14 sections in this exact order:

1. Objective
2. Scope
3. Inclusions
4. Test Environments
5. Defect Reporting Procedure
6. Test Strategy
7. Test Schedule
8. Test Deliverables
9. Entry and Exit Criteria
10. Test Execution
11. Test Closure
12. Tools
13. Risks and Mitigations
14. Approvals

Template placeholders (filled before the LLM call):

| Placeholder | Source |
|-------------|--------|
| `{{FEATURE}}` | ticket summary |
| `{{KEY}}` | ticket key |
| `{{URL}}` | `{jira_url}/browse/{key}` |
| `{{TITLE}}` | ticket summary |
| `{{DATE}}` | generation date |
| `{{MODEL}}` | configured model |

The LLM receives the ticket fields (summary, description, acceptance criteria) and returns the full plan, filling every section above. The header (title / source line) is rendered deterministically by the app, not the LLM.

## Behavioral rules

1. **Never invent content.** If summary, description, or acceptance criteria are missing, record them as `findings` — do not fabricate values.
2. **Deterministic output.** `temperature=0.0`; same input produces the same plan.
3. **Reliability over speed.** Validate the Jira connection and the ticket exists before calling the LLM.
4. **Traceability.** Every test case must link back to an acceptance criterion or requirement; untraceable cases are not emitted.
5. **Single input.** The agent accepts a Jira ID (free text or URL) and nothing else.
6. **No credentials in code.** Config is persisted (gitignored), never hardcoded.

## Architectural invariants

- **Layered separation:** fetch layer (Jira) → prompt/template layer → LLM layer → output/export layer. No cross-layer leakage.
- **Reuse over rebuild:** `jira_client.py` and `config_store.py` patterns are lifted from `chapter_03_TC_GENERATOR`; only the template, prompt, and output schema differ.
- **Prompt = schema.** The LLM is constrained by a structured system prompt + a markdown template with placeholders (same pattern as the existing templates).
- **No `tools/` code until Blueprint is approved** (BLAST Protocol 0 halt condition).
- **Config seeding:** `.env` seeds `config.json` on first run; `config.json` is gitignored.

## How we think about it

The Test Plan Agent is a thin orchestration layer, not a new subsystem. It reuses the proven fetch pipeline and swaps the *output contract*: instead of generating test cases, it generates a structured, traceable test plan. The hard part is the **output schema and the no-invention invariant** — everything else is already solved.
