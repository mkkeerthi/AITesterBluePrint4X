# Test Plan Agent — Findings

> Research, discoveries, and constraints gathered during initialization.
> Everything here is derived from the existing `chapter_03_TC_GENERATOR` implementation, which already solves "fetch a Jira ticket and feed it to an LLM".

## What we already know (reuse, don't reinvent)

The existing Jira Test Case Generator (`chapter_03_TC_GENERATOR`) already implements the exact fetch pipeline we need:

- `jira_client.py` — fetches a ticket and extracts summary / description / acceptance criteria.
- `config_store.py` — persists `jira_url`, `jira_email`, `jira_api_token`, `groq_api_key`, `groq_model`.
- `llm_client.py` — sends the ticket to Groq and returns generated markdown.

The Test Plan Agent is the same shape: **fetch ticket → LLM → structured output**, except the output is a *test plan* instead of *test cases* or a *requirement analysis*.

## How we fetch from Jira

Authentication is **HTTP Basic Auth** using the Jira account email + an **API token** (not the password). Token is created at https://id.atlassian.com/manage-profile/security/api-tokens.

### Connectivity check (validates URL + email + token in one call)

```bash
curl -u "you@example.com:YOUR_API_TOKEN" \
  "https://your-domain.atlassian.net/rest/api/3/myself"
```

Expected `200`; a `401` means bad credentials, `403` means the account lacks permission.

### Fetch the issue (the core call)

```bash
curl -u "you@example.com:YOUR_API_TOKEN" \
  -G "https://your-domain.atlassian.net/rest/api/3/issue/PROJ-123" \
  --data-urlencode "fields=summary,description"
```

- `summary` — plain string, used as the ticket title.
- `description` — Atlassian Document Format (ADF); we flatten `fields.description.content` to plain text.
- **Acceptance criteria** is a project-specific custom field, so we cannot hardcode it. We scan all `customfield_*` entries and pull text out of:
  - plain strings,
  - ADF nodes (`content`),
  - Atlassian checklist items (list of `{text|value}`).

### Python equivalent (production path, copied from jira_client.py)

```python
import requests

def fetch_ticket(key, config):
    url = f"{config['jira_url']}/rest/api/3/issue/{key}"
    resp = requests.get(
        url,
        params={"fields": "summary,description"},
        auth=(config["jira_email"], config["jira_api_token"]),
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    fields = data.get("fields") or {}
    return {
        "key": key,
        "summary": fields.get("summary") or "",
        "description": _adf_to_text(fields.get("description", {}).get("content") or []),
        "acceptance_criteria": _acceptance_criteria(fields),
    }
```

## Key findings / constraints

1. **Ticket key regex**: `\b([A-Z][A-Z0-9]+-\d+)\b` — matches any `PROJ-123` style key, so the input can be pasted as free text or a URL.
2. **Acceptance criteria is a custom field** — field name differs per Jira project, so we do a best-effort scan across `customfield_*` rather than assuming a fixed key.
3. **No credentials in source** — config lives in `config.json` (gitignored), seeded from `.env` on first run. Same pattern must carry over to the Test Plan Agent.
4. **LLM is Groq**, default model `llama-3.3-70b-versatile`, `temperature=0.0` for deterministic output.
5. **Deterministic / no-invention rule** — the LLM must treat missing fields as *findings*, not fill them with guesses. This is a hard invariant.
6. **Reuse > rebuild** — the fetch layer (`jira_client.py`) and config layer (`config_store.py`) can be lifted almost verbatim; only the template + prompt + output schema change.

## Discovery Questions — ANSWERED (Prompt2.md)

1. **Test-plan output schema** → defined in `test_plan_template.md` (14 sections: Objective, Scope, Inclusions, Test Environments, Defect Reporting Procedure, Test Strategy, Test Schedule, Test Deliverables, Entry/Exit Criteria, Test Execution, Test Closure, Tools, Risks & Mitigations, Approvals).
2. **Extra Jira fields?** → No. Only summary / description / acceptance criteria.
3. **Groq model** → `openai/gpt-oss-120` is the default.
4. **UI** → Streamlit app, mirroring chapter 03 (main chat page + Settings page).

All discovery questions are resolved. Phase 1's remaining Discovery prompts (North Star, Integrations, Source of Truth, Delivery Payload, Behavioral Rules) are answered implicitly by the objective and are captured below.

## Build output (Phases 2–4)

| File | Purpose |
|------|---------|
| `config_store.py` | Persist/seed Jira + Groq config |
| `jira_client.py` | Fetch ticket + extract key + connectivity check |
| `llm_client.py` | Groq `generate_test_plan` (default `openai/gpt-oss-120b`) |
| `test_plan_template.md` | 14-section output prompt (header + rules) |
| `app.py` | Main Streamlit chat page |
| `pages/settings.py` | Settings + connectivity checks |
| `requirements.txt` | streamlit / requests / groq / python-dotenv |
| `src/.env` | Credential seed (gitignored) |

## Important correction — model ID

Prompt2.md specifies the default model as **`openai/gpt-oss-120`**, but Groq's real model ID is **`openai/gpt-oss-120b`** (confirmed via `models.list()`). `config_store.py` and `llm_client.py` default to `120b` so the app works out of the box. The `.env` seed still reads `openai/gpt-oss-120` and should be updated to `120b` before first run (or the Settings page will select the correct model once the API key is loaded).
