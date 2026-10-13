# Chapter 9 — Langflow

[Langflow](https://github.com/langflow-ai/langflow) is a low-code, visual builder for
LLM and agent workflows. This chapter hosts a local Langflow instance used to explore
drag-and-drop AI pipelines, including two example agents (Bug Triage and Edge Cases)
built from custom Python components.

## Structure

```
chapter_09_Langflow/
├── Agents/                # Agent definitions exported from Langflow
│   ├── BugTriage/         # Bug-triage agent write-up + screenshots
│   └── EdgeCase/          # Edge-case agent write-up + screenshots
├── Components/            # Custom Langflow components (Python)
│   ├── Groq.py            # Groq chat-completion component
│   └── Jira.py            # Fetches a Jira work item description by key
├── Flows/                 # Flow definitions exported from Langflow (JSON)
│   ├── Bug Triage Agent.json
│   └── Edge Cases Agent.json
├── langflow_data/         # Langflow runtime data (gitignored)
│   ├── langflow.db        # SQLite DB: flows, global variables, credentials, chat history
│   └── secret_key         # Encrypts the CREDENTIAL-type variables in the DB
├── scripts/
│   ├── install_langflow.ps1   # One-time install of Langflow into machine Python 3.13
│   ├── run_langflow.ps1       # Starts the server against langflow_data/
│   └── stop_langflow.ps1      # Stops the server
└── README.md
```

> `langflow_data/` and `.venv/` are excluded via the repository `.gitignore`.

## Prerequisites

- Windows with PowerShell.
- Network access to `api.groq.com`, `<your-site>.atlassian.net` and `openrouter.ai`.
- Python 3.13 installed machine-wide — available as `python` on PATH, or through the
  `py` launcher (`py -3.13`) — with Langflow installed into it (see [Setup](#setup-one-time)).

## Setup (one-time)

Install Langflow into the machine-level Python 3.13 (no project virtualenv is used):

```powershell
chapter_09_Langflow\scripts\install_langflow.ps1
```

Equivalent raw commands:

```powershell
python -m pip install --upgrade pip
python -m pip install langflow
```

Use `py -3.13` in place of `python` if the Windows launcher is installed. To pin a specific
Langflow release instead of the latest, run
`chapter_09_Langflow\scripts\install_langflow.ps1 -Requirement "langflow==1.12.1"`.

## Run

From the repository root:

```powershell
chapter_09_Langflow\scripts\run_langflow.ps1
```

The script points Langflow at this chapter's `langflow_data/` and `Components/` folder
automatically, so the saved flows and credentials load without re-configuration. Then open
<http://127.0.0.1:7860>.

To run it on another port, or in the background:

```powershell
chapter_09_Langflow\scripts\run_langflow.ps1 -Port 7861

Start-Process powershell -ArgumentList '-NoProfile','-ExecutionPolicy','Bypass','-File','chapter_09_Langflow\scripts\run_langflow.ps1'
```

Equivalent to the script, if you prefer the raw command:

```powershell
$env:LANGFLOW_CONFIG_DIR      = "$PWD\chapter_09_Langflow\langflow_data"
$env:LANGFLOW_DATABASE_URL    = "sqlite:///$($PWD.Path.Replace('\','/'))/chapter_09_Langflow/langflow_data/langflow.db"
$env:LANGFLOW_COMPONENTS_PATH = "$PWD\chapter_09_Langflow\Components"
python -m langflow run --host 127.0.0.1 --port 7860
```

> Run `python -m langflow` rather than the packaged `langflow.exe` launcher: some
> environments (for example an organization **Device Guard / Application Control** policy)
> block the launcher, while the module form is always available.

## Verify

```powershell
Invoke-WebRequest http://127.0.0.1:7860/health_check -UseBasicParsing
# -> {"status":"ok","chat":"ok","db":"ok"}
```

## Stop / restart

```powershell
chapter_09_Langflow\scripts\stop_langflow.ps1
# or, for a different port
chapter_09_Langflow\scripts\stop_langflow.ps1 -Port 7861
```

Restart by re-running the run script above.

## Notes

- The **first run is slow** — Langflow initializes its database and builds the
  component catalog before it starts serving.
- Flows, credentials, and chat history persist in `langflow_data/` (`langflow.db` +
  `secret_key`), which lives **outside** any Python environment, so reinstalling Langflow
  or switching interpreters never wipes them. **Keep `secret_key` with the database** — the
  `Credential` rows are Fernet-encrypted with it, so copying `langflow.db` without
  `secret_key` makes the stored API keys undecryptable.
- **No project virtualenv** — Langflow runs from the machine-level Python 3.13
  (`python` on PATH or `py -3.13`), so nothing is installed inside this folder.
- **PyTorch is not installed**, so embedding/document components that require it will
  warn and be unavailable.
- `langflow_data/` and `.venv/` are gitignored and must never be committed.
