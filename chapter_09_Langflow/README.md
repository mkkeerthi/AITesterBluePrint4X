# Chapter 9 — Langflow

[Langflow](https://github.com/langflow-ai/langflow) is a low-code, visual builder for
LLM and agent workflows. This chapter hosts a local Langflow instance used to explore
drag-and-drop AI pipelines.

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
└── .venv/                 # Local virtualenv (Python 3.13, gitignored)
                           #   langflow + all dependencies installed here
```

## Prerequisites

- Network access (the first setup downloads Python and the Langflow package tree).
- **Python 3.13.** The machine ships with Python 3.14, which Langflow does *not*
  support (`requires-python >=3.10,<3.14`), so `uv` is used to provision an isolated
  Python 3.13 runtime for this chapter.

## Setup (one-time)

From the repository root:

```powershell
# 1. Install uv (if not already present). It runs fine as a module, so PATH is optional.
pip install uv

# 2. Create a Python 3.13 virtualenv for this chapter (uv downloads Python 3.13).
python -m uv venv --python 3.13 chapter_09_Langflow/.venv

# 3. Install Langflow into that virtualenv.
python -m uv pip install langflow --python chapter_09_Langflow/.venv/Scripts/python.exe
```

## Run

```powershell
chapter_09_Langflow\.venv\Scripts\langflow.exe run --host 127.0.0.1 --port 7860
```

Then open <http://127.0.0.1:7860>.

To run it in the background from a shell, append `Start-Process` or use your agent's
background-task facility; the server keeps running until stopped.

## Step by Step Manual Invoke of Langflow

Use this when the packaged `langflow.exe` launcher is unavailable — for example when an
organization **Device Guard / Application Control** policy blocks it. The same policy can
also block compiled DLLs inside the virtualenv, so the module form below is the reliable
manual path.

1. **Open a terminal at the repository root** (PowerShell in this example):

   ```powershell
   cd <repo-root>
   ```

2. **Confirm the virtualenv and the Langflow package are present.** The chapter ships a
   pre-built Python 3.13 venv with Langflow already installed:

   ```powershell
   Test-Path chapter_09_Langflow\.venv\Scripts\python.exe   # -> True
   ```

3. **Check that port 7860 is free.** If something already listens on it, stop it first
   (or pick another port in step 5):

   ```powershell
   Get-NetTCPConnection -LocalPort 7860 -State Listen -ErrorAction SilentlyContinue
   # no output = port is free
   ```

4. **Confirm the environment can run Langflow** (a quick smoke test that also validates
   the venv before launching the long-running server):

   ```powershell
   chapter_09_Langflow\.venv\Scripts\python.exe -m langflow --version
   # -> langflow 1.12.1
   ```

   > If this fails with `An Application Control policy has blocked this file`, the policy
   > blocked a compiled DLL (e.g. `scipy`'s). This is usually a reputation check on first
   > execution — simply run the same command again and it typically succeeds. If it keeps
   > failing, the block is permanent and needs IT to allow the file.

5. **Start the Langflow server via the venv's Python module.** Running `python -m langflow`
   bypasses the blocked `langflow.exe` launcher:

   ```powershell
   chapter_09_Langflow\.venv\Scripts\python.exe -m langflow run --host 127.0.0.1 --port 7860
   ```

   > **Always name the venv's Python explicitly.** PowerShell (unlike `cmd.exe`) does **not**
   > search the current directory for executables, so a bare `python.exe` resolves to whatever
   > is first on `PATH` — often a different install such as `C:\Python314\python.exe` — and
   > fails with `No module named langflow`. From the repo root use the full
   > `chapter_09_Langflow\.venv\Scripts\python.exe` path; if you are already inside the
   > `.venv\Scripts` folder, prefix with `.\`:
   >
   > ```powershell
   > .\python.exe -m langflow run --host 127.0.0.1 --port 7860
   > ```
   >
   > Equivalently, activate the venv first (`.\.venv\Scripts\Activate.ps1`), after which a
   > bare `python` points at the venv.

   To keep it running in the background instead of blocking the terminal:

   ```powershell
   Start-Process -FilePath "chapter_09_Langflow\.venv\Scripts\python.exe" `
     -ArgumentList '-m','langflow','run','--host','127.0.0.1','--port','7860'
   ```

6. **Wait for startup.** The first run is slow (it initializes the database and builds the
   component catalog) and may print nothing for a minute or more. It is ready when it logs
   a banner with the access URL.

7. **Verify the server is healthy.**

   ```powershell
   Invoke-WebRequest http://127.0.0.1:7860/health_check -UseBasicParsing
   # -> {"status":"ok","chat":"ok","db":"ok"}
   ```

8. **Open the UI** in a browser: <http://127.0.0.1:7860>.

9. **Stop the server.** Press `Ctrl+C` in the terminal running it, or kill the process on
   port 7860:

   ```powershell
   Get-NetTCPConnection -LocalPort 7860 -State Listen |
     Select-Object -ExpandProperty OwningProcess |
     ForEach-Object { Stop-Process -Id $_ -Force }
   ```

> **Shortcut:** if the packaged launcher is *not* blocked on your machine, the single
> command `chapter_09_Langflow\.venv\Scripts\langflow.exe run --host 127.0.0.1 --port 7860`
> from the [Run](#run) section is equivalent to steps 5–6.

## Verify

```powershell
Invoke-WebRequest http://127.0.0.1:7860/health_check -UseBasicParsing
# -> {"status":"ok","chat":"ok","db":"ok"}
```

## Stop / restart

- Stop: `Ctrl+C` in the terminal running Langflow (or kill the process on port 7860).
- Restart: re-run the `langflow.exe run` command above.

## Notes

- The **first run is slow** — Langflow initializes its database and builds the
  component catalog before it starts serving.
- Flows and settings persist in a local SQLite database (`langflow.db`) created on
  first run. Deleting or recreating `.venv` wipes your saved flows; set
  `LANGFLOW_CONFIG_DIR` to keep data outside the venv if you want it preserved across
  rebuilds.
- **PyTorch is not installed**, so embedding/document components that require it will
  warn and be unavailable. Add it with
  `python -m uv pip install torch --python chapter_09_Langflow/.venv/Scripts/python.exe`
  if needed.
- `.venv/` is excluded via `.gitignore` and must never be committed.
