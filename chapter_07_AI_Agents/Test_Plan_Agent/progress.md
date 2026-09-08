# Test Plan Agent — Progress Log

> Running log of what was done, errors hit, and results. Updated every 10–30 minutes of active work.

## Format

Each entry: `[timestamp] — what was done / error / result`.

## Log

- **[init] Protocol 0 start** — Read `Prompt.md` and `BLAST.md`. Confirmed the objective: build a **Test Plan Creator from a Jira ID**, starting with protocol 0 (initialize project memory, then halt).
- **[init] Explored existing code** — Found `chapter_03_TC_GENERATOR` already solves Jira-fetch + LLM-generation. Identified the reusable pieces: `jira_client.py`, `config_store.py`, `llm_client.py`.
- **[init] Created `task_plan.md`** — phases, goals, checklists, and BLAST invariants. Result: OK.
- **[init] Created `findings.md`** — documented the Jira REST calls (curl + Python), the acceptance-criteria custom-field discovery, constraints, and open discovery questions. Result: OK.
- **[init] Created `progress.md`** — this file. Result: OK.
- **[init] Created `LLM.md`** — data schemas, behavioral rules, and architectural invariants. Result: OK.

## Errors / issues

- None so far. No code has been written (correct — Protocol 0 halts before `tools/`).

## Phase 1 — Blueprint (discovery resolved via Prompt2.md)

- **[phase1] Answered discovery questions** — schema from `test_plan_template.md`, only summary/description/AC needed, default model `openai/gpt-oss-120`, Streamlit app. Result: OK.
- **[phase1] Locked schema in LLM.md** — 14-section output, placeholders mapped. Result: OK.
- **[phase1] Model correction** — Prompt2.md said `openai/gpt-oss-120`, but Groq's real model ID is `openai/gpt-oss-120b` (verified via `list_models`). Source files updated to `120b`; `.env` left as-is at user's instruction. Result: documented.

## Phase 2 — Link (connectivity)

- **[phase2] Jira check** — `/rest/api/3/myself` returned ✅ Connected as **Keerthi Kumar**. Result: OK.
- **[phase2] Groq check** — `models.list()` succeeded; `openai/gpt-oss-120b` present. Result: OK.

## Phase 3 — Architect (build)

- **[phase3] config_store.py** — persisted config, `.env` seed, `DEFAULT_MODEL = openai/gpt-oss-120b`. Result: OK.
- **[phase3] jira_client.py** — `extract_ticket_key`, `check_connection`, `fetch_ticket`, ADF flatten + custom-field AC scan. Result: OK.
- **[phase3] llm_client.py** — `list_models`, `check_connection`, `generate_test_plan`. Fixed template path from `templates/` to repo root. Result: OK.
- **[phase3] test_plan_template.md** — extended header/ToC into a full prompt (ticket injection + 14-section rules). Result: OK.
- **[phase3] app.py + pages/settings.py** — Streamlit chat UI + settings page, mirroring chapter 03. Result: OK.
- **[phase3] requirements.txt + src/.env** — deps + seeded credentials. Result: OK.

## Phase 4 — Stylize + Verify

- **[phase4] End-to-end generation** — fed a synthetic ticket to `generate_test_plan`, got a full 14-section plan with proper grounding/inference markers. Result: OK.
- **[phase4] App launch** — `streamlit run app.py` bound to port 8509, `/health` returned 200. Result: OK.

## Errors / issues

- `FileNotFoundError` on template — `llm_client.py` pointed at `templates/test_plan_template.md` but the file is at repo root. Fixed.
- UnicodeEncodeError printing ✅ on Windows cp1252 console — resolved by setting `PYTHONIOENCODING=utf-8` (test-only; no code change needed).
- Model-name mismatch — `openai/gpt-oss-120` vs actual `openai/gpt-oss-120b`. Corrected in source; `.env` left untouched per user.

## Next

- Run `streamlit run app.py` locally and enter a real Jira key to confirm the full flow in-browser.
- Optional: move `test_plan_template.md` into `templates/` for consistency with chapter 03.
