# Test Plan Agent — Task Plan

> BLAST Protocol 0 — Initialization. Phase plan, goals, and checklists.
> Objective: build a **Test Plan Creator** that takes a Jira issue ID and produces a structured test plan.

## Phases

| Phase | Goal | Exit criteria |
|-------|------|---------------|
| 0 | Initialize project memory | `task_plan.md`, `findings.md`, `progress.md`, `LLM.md` all present |
| 1 | Resolve Discovery Questions | All questions answered and recorded in `findings.md` |
| 2 | Define data schema | Schema + rules + invariants locked in `LLM.md` |
| 3 | Fetch Jira issue | A Jira ID returns summary, description, acceptance criteria |
| 4 | Generate test plan | LLM turns fetched ticket into a structured test plan |
| 5 | Present / export | Test plan surfaced to user and exportable (markdown) |

## Goals

1. Accept a **Jira issue ID** as the single input (e.g. `PROJ-123`).
2. Fetch the issue from Jira using the REST API (Basic Auth with email + API token).
3. Extract the fields that matter for testing: summary, description, acceptance criteria.
4. Send those fields to an LLM (Groq) with a strict test-plan schema.
5. Return a deterministic, traceable test plan — **never invent content**; a missing field is a finding, not a blank to fill.

## Checklists

### Protocol 0 — Initialization
- [x] Create `task_plan.md` (this file)
- [x] Create `findings.md`
- [x] Create `progress.md`
- [x] Create `LLM.md`
- [ ] Halt execution (no `tools/` scripts) until discovery + schema are done

### Discovery Questions
- [x] What Jira issue fields do we need for a test plan?
- [x] How is acceptance criteria stored (custom field vs. description)?
- [x] Which LLM and model do we use?
- [x] What does the output test-plan schema look like?

### Data Schema
- [x] Define the Jira ticket shape
- [x] Define the test-plan output shape
- [x] Define behavioral rules and invariants

### Phase 2 — Link
- [x] Verify Jira connectivity
- [x] Verify Groq connectivity

### Phase 3 — Architect
- [x] `config_store.py`
- [x] `jira_client.py`
- [x] `llm_client.py`
- [x] `test_plan_template.md`
- [x] `app.py` + `pages/settings.py`
- [x] `requirements.txt` + `src/.env`

### Phase 4 — Stylize
- [x] Verify end-to-end generation
- [x] Launch app locally and confirm health
- [ ] Confirm with real Jira key in-browser (pending user run)

## Non-negotiables (BLAST invariants)

- Reliability over speed.
- Never guess business logic.
- Deterministic output; zero fabricated content.
- No code in `tools/` until the Blueprint is approved.
