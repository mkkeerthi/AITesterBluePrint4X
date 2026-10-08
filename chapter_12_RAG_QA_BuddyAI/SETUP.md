# QABuddy — Setup & Run Guide

Step-by-step instructions to stand up **QABuddy** (a multi-source hybrid RAG for QA teams)
on a local machine and run it end to end. Windows steps are primary; macOS/Linux/WSL notes
are given where they differ.

This project is a copy of the chapter_12 QABuddy build, retargeted to lightweight local
models:

| Component | Model / tech | Where it runs |
|---|---|---|
| Embeddings | `qwen3-embedding:0.6b` | Ollama, `http://localhost:11434` |
| Sparse retrieval | code-aware BM25 (no model) | in-process |
| Reranker | `cross-encoder/ms-marco-MiniLM-L-6-v2` | in-process (sentence-transformers) |
| Answer LLM | `openai/gpt-oss-120b` | **Groq remote API** (needs a key) |
| Vector DB | Qdrant `v1.19.1` (local) or **Qdrant Cloud** | `http://localhost:6333` or your cluster URL |
| API + UI | FastAPI + React (Vite) | one process on port `8300` |

Ports used: **8300** (app/UI), **6333** (local Qdrant only — Cloud is remote), **11434** (Ollama), **5300** (Vite dev server, optional).

---

## 0. Prerequisites

| Tool | Needed for | Status on this PC | Install |
|---|---|---|---|
| Python **3.13** | the app | **installed** — 3.13.15, machine-wide at `C:\Program Files\Python313` | https://www.python.org/downloads/ |
| Ollama | embeddings | installed (v0.33.3), no models pulled yet | https://ollama.com/download |
| Qdrant | vector DB | not installed — using **Qdrant Cloud** | Step 3 (local binary) or a Cloud cluster + `QDRANT_API_KEY` |
| Node.js 18+ / npm | building the UI | installed (Node v24, npm 11) | https://nodejs.org |
| Git | cloning source repos (optional) | installed | https://git-scm.com |
| Groq API key | the answer LLM | — | https://console.groq.com/keys |

**Python version note:** Python **3.13.15** is installed **machine-wide** (all users) at
`C:\Program Files\Python313` and is on `PATH`, so `python` resolves to it and `py -3.13`
works too. Python 3.14 was **removed** — `sentence-transformers`/PyTorch do not ship wheels
for it, so it could not run this project. All dependencies are **already installed globally**,
so Step 1 can be skipped (it is kept below for an optional isolated environment). The helper
script `run.sh` targets 3.13; the Docker image targets 3.12. Either is fine.

Hardware used for sizing here: Intel Core Ultra 7 258V (8 threads), Arc iGPU, 32 GB RAM —
CPU inference. The models above are chosen to run comfortably on CPU.

All commands below assume you are in the project root:

```powershell
cd C:\PramodAcademy\QABuddy
```

---

## 1. Python 3.13 + dependencies

Python **3.13.15** is installed machine-wide and every dependency this project needs is
**already installed globally** — no virtual environment is required. Just confirm:

```powershell
# from C:\PramodAcademy\QABuddy
python -V                 # Python 3.13.15
python -m pip check       # No broken requirements found.
python -m pip list        # torch (CPU), fastapi, sentence-transformers, qdrant-client, ...
```

You can now run `python -m qabuddy ...` directly (Steps 6–9).

> **Installing more packages.** The machine `site-packages` lives under `Program Files`, so a
> plain `pip install <pkg>` needs an **elevated** terminal. Without admin, use
> `pip install --user <pkg>` (installs into `%APPDATA%\Python\Python313\site-packages`).

**Optional — isolated virtual environment.** Only if you want one instead of the global install:

```powershell
# from C:\PramodAcademy\QABuddy
py -3.13 -m venv .venv

# if PowerShell blocks activation:
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

.\.venv\Scripts\Activate.ps1
python -V            # confirm 3.13

# CPU-only torch first, then the rest of the deps
pip install --index-url https://download.pytorch.org/whl/cpu torch
pip install -r requirements.txt
pip install pytest
```

> **Prefer `uv`?** If you install uv, use:
> `uv venv --python 3.13 .venv` then
> `uv pip install --python .venv\Scripts\python.exe -r requirements.txt pytest`
> (with CPU torch added the same way).

macOS/Linux/WSL: `python3.13 -m venv .venv && source .venv/bin/activate` then the same pip lines.

---

## 2. Ollama + the embedding model

Ollama must be running before you ingest or serve.

```powershell
# start the server if it is not already running (the desktop app usually keeps it up)
ollama serve

# in a second terminal, pull the local embedding model
ollama pull qwen3-embedding:0.6b
ollama list          # should now show qwen3-embedding:0.6b
```

`qwen3-embedding:0.6b` is 1024-dimensional natively, which matches the default
`EMBED_DIM=1024` — no truncation needed.

---

## 3. Qdrant (vector database)

**Using Qdrant Cloud?** Skip this step and go to Step 4 — just set `QDRANT_URL` and
`QDRANT_API_KEY`. Everything below is for a local server.

No Docker required. Qdrant publishes a native Windows binary. Download and run it in its
own folder (it stores data in `./storage`).

```powershell
# from C:\PramodAcademy\QABuddy
$env:QDRANT__TELEMETRY_DISABLED = "true"
New-Item -ItemType Directory -Force -Path .qdrant-win | Out-Null
Set-Location .qdrant-win

curl.exe -L -o qdrant.zip https://github.com/qdrant/qdrant/releases/download/v1.19.1/qdrant-x86_64-pc-windows-msvc.zip
Expand-Archive -Force qdrant.zip .
.\qdrant.exe
```

Leave this terminal running. Verify in another terminal:

```powershell
curl.exe -s http://localhost:6333/          # returns a small JSON version banner
curl.exe -s http://localhost:6333/collections
```

**Alternatives for Qdrant**
- **Qdrant Cloud (managed)** — skip the local install entirely: set `QDRANT_URL` to your
  cluster URL (e.g. `https://<id>.<region>.aws.cloud.qdrant.io:6333`) and `QDRANT_API_KEY`
  to its API key in `.env` (Step 4). No local server needed.
- Any OS with Docker: `docker run -p 6333:6333 qdrant/qdrant:v1.19.1`
- macOS/Linux/WSL: `run.sh` auto-downloads the right binary into `.bin/` on first run (local only).

---

## 4. Configure `.env`

```powershell
# from C:\PramodAcademy\QABuddy
Copy-Item .env.example .env
notepad .env
```

Set the Qdrant endpoint (Cloud or local) and the Groq key, and confirm the model choices:

```dotenv
# ---- vector DB (Qdrant) ----
# Cloud: the cluster URL + API key. Local: http://localhost:6333 with the key left blank.
QDRANT_URL=https://<id>.<region>.aws.cloud.qdrant.io:6333
QDRANT_API_KEY=your_qdrant_cloud_key
QDRANT_COLLECTION=qabuddy

# ---- embeddings (Ollama, open source) ----
OLLAMA_URL=http://localhost:11434
EMBED_MODEL=qwen3-embedding:0.6b
EMBED_DIM=1024

# ---- reranker (cross-encoder, runs inside the API process) ----
RERANK_ENABLED=true
RERANK_MODEL=cross-encoder/ms-marco-MiniLM-L-6-v2

# ---- answer LLM (Groq remote) ----
LLM_PROVIDER=groq
LLM_MODEL=openai/gpt-oss-120b
GROQ_API_KEY=your_groq_key_here
```

Notes
- Keep comments on their own lines (docker compose `env_file` keeps inline comments as part
  of the value).
- `.env` is git-ignored — never commit it.
- The Qdrant API key is a secret: keep it only in `.env` (git-ignored), never in `.env.example` or source.
- Other defaults you can leave alone: `PREFETCH_K=40`, `RERANK_CANDIDATES=24`, `FINAL_K=6`,
  `CONTEXT_TOKENS=3500`, `PORT=8300`. Trim `RERANK_CANDIDATES` (e.g. 12–16) if CPU reranking
  feels slow.

---

## 5. (Optional) Add the source-code corpus

The two framework repos under `data/07_Source_Codes/` shipped **empty** (they are git
submodules that were not checked out in this copy). Everything else in `data/` has sample
content, so you can skip this — but "framework coding help" questions need them.

```powershell
# from C:\PramodAcademy\QABuddy
git clone https://github.com/PramodDutta/ATB13xSeleniumAdvanceFramework.git   data\07_Source_Codes\ATB13xSeleniumAdvanceFramework
git clone https://github.com/PramodDutta/AdvancePlaywrightFramework1x.git     data\07_Source_Codes\AdvancePlaywrightFramework1x
```

Add your own content by dropping files into the matching `data/NN_*` folder and (if it is a
new source) adding an entry to `sources.yaml`. Files whose names start with `_` are ignored.

---

## 6. Build the web UI

```powershell
cd ui
npm install
npm run build      # emits ui/dist, which the Python server serves
cd ..
```

---

## 7. Ingest the corpus (build the index)

Make sure Ollama (Step 2) and Qdrant are both reachable — a local server (Step 3) or your Cloud cluster. The first run pulls the
reranker from Hugging Face and embeds every chunk, so it is the slow step.

```powershell
# from the project root (activate .venv first only if you made one)
python -m qabuddy ingest
```

- Incremental: re-running only re-embeds files whose bytes changed.
- `python -m qabuddy ingest --full` rebuilds everything.
- `python -m qabuddy ingest --source jira` (repeatable) indexes one source.
- **Changing `EMBED_MODEL` or `EMBED_DIM` forces a full rebuild automatically** — vectors
  from different models are not comparable.

---

## 8. Run the app

```powershell
python -m qabuddy serve
```

Open **http://localhost:8300**. The API and the built UI are served together on one port.

For UI development with hot reload (optional), keep the API running and in a second terminal:

```powershell
cd ui
npm run dev        # http://localhost:5300, proxies /api -> http://localhost:8300
```

---

## 9. Verify it works

```powershell
# dependency + index + model status
curl.exe -s http://localhost:8300/api/health

# retrieval hit-rate / MRR on the golden set
python -m qabuddy eval

# ask a question from the CLI
python -m qabuddy ask "Why did build #142 fail?" --mode rca
```

`/api/health` should show `"qdrant": true`, `"ollama": true`,
`"embed_model_ready": true`, `"llm_configured": true`, and a non-zero `"points"` count.

---

## Daily workflow (TL;DR)

1. Start Ollama (usually already running).
2. Start Qdrant: `.\.qdrant-win\qdrant.exe` (local), or point `QDRANT_URL` at your Cloud cluster.
3. `python -m qabuddy ingest` (only when `data/` changed).
4. `python -m qabuddy serve` → open http://localhost:8300.

---

## CLI reference (`python -m qabuddy <cmd>`)

| Command | What it does |
|---|---|
| `ingest [--full] [--source ID] [--force]` | Build/update the index |
| `serve` | Start the API + UI on `$PORT` |
| `ask "question" [--mode rca]` | Answer with citations |
| `search "question"` | Retrieval only, with the score trace |
| `eval` | Retrieval hit-rate/MRR on `eval/golden.yaml` |
| `sync-jira [--jql "..."]` | Pull Jira tickets, then ingest them |
| `export-demo` | Re-record the hosted demo data |

---

## Configuration reference (`.env`)

| Variable | Default | Meaning |
|---|---|---|
| `QDRANT_URL` | `http://localhost:6333` | Qdrant endpoint (Cloud: `https://<id>...cloud.qdrant.io:6333`) |
| `QDRANT_API_KEY` | — | Qdrant Cloud API key (blank for an unauthenticated local server) |
| `QDRANT_COLLECTION` | `qabuddy` | Collection name |
| `OLLAMA_URL` | `http://localhost:11434` | Ollama endpoint |
| `EMBED_MODEL` | `qwen3-embedding:0.6b` | Dense embedding model |
| `EMBED_DIM` | `1024` | Vector size (native width of the 0.6b model) |
| `RERANK_ENABLED` | `true` | Toggle cross-encoder reranking |
| `RERANK_MODEL` | `cross-encoder/ms-marco-MiniLM-L-6-v2` | Cross-encoder |
| `LLM_PROVIDER` | `groq` | `groq` / `ollama` / `openai` |
| `LLM_MODEL` | `openai/gpt-oss-120b` | Answer model |
| `GROQ_API_KEY` | — | Required for the Groq provider |
| `PREFETCH_K` | `40` | Candidates per retriever before fusion |
| `RERANK_CANDIDATES` | `24` | Fused candidates re-scored by the cross-encoder |
| `FINAL_K` | `6` | Sources handed to the LLM |
| `CONTEXT_TOKENS` | `3500` | Prompt source-text budget |
| `PORT` | `8300` | App port |
| `JIRA_BASE_URL` / `JIRA_EMAIL` / `JIRA_API_TOKEN` / `JIRA_JQL` | — | Optional Jira sync |

To go fully offline you can set `LLM_PROVIDER=ollama` and `LLM_MODEL=gpt-oss:20b` (or any
pulled chat model), but that is much heavier on CPU than the Groq path and is not required
for this lightweight setup.

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| `Ollama is not reachable` | Start Ollama; confirm `curl.exe http://localhost:11434/api/version`. |
| `Embedding model '...' is not pulled` | `ollama pull qwen3-embedding:0.6b`. |
| Qdrant connection refused / health `"qdrant": false` | Local: start `.\.qdrant-win\qdrant.exe`; confirm `curl.exe http://localhost:6333/`. Cloud: check `QDRANT_URL` (`…:6333`) and `QDRANT_API_KEY`. |
| `pip install <pkg>` fails with "Access is denied" | Machine `site-packages` is under `Program Files`. Run it from an **elevated** terminal, or use `pip install --user <pkg>`. |
| `pip install` fails building torch / sentence-transformers | You are on Python 3.14, which has no wheels. This project needs Python 3.13 (Step 1). |
| Reranker slow on first query | First load downloads `cross-encoder/ms-marco-MiniLM-L-6-v2` (~90 MB) from Hugging Face; later runs are cached. |
| Reranker shows as `disabled` | It is optional — retrieval still works (`RERANK_ENABLED=false`). Check the console error it printed. |
| Groq `429` / "waiting" | On-demand tier is ~8k tokens/min (≈2 answers/min). Wait, or upgrade the Groq tier, or switch `LLM_PROVIDER`. |
| UI says "QABuddy API is running. Build the UI…" | Run `cd ui && npm run build`. |
| `./run.sh` fails on Windows | It is a bash script and its Qdrant bootstrap has no Windows branch. Use Steps 1–8, or run it under WSL/Git Bash. |
| Relevant hits suddenly dropped after the reranker swap | The `RERANK_FLOOR` in `qabuddy/retrieve.py` (default `0.02`) was tuned for the previous reranker; lower it slightly if needed. |
| Port already in use (`8300`/`6333`/`11434`) | Change `PORT` in `.env`, or stop the conflicting process. |

---

## Appendix A — one-command path on macOS / Linux / WSL

`run.sh` starts Ollama (and a local Qdrant unless `QDRANT_URL` points at Cloud), ingests on first run, builds the UI, and serves:

```bash
./run.sh            # start everything and open http://localhost:8300
./run.sh ingest     # index changed files (--full rebuilds)
./run.sh eval       # retrieval ablation
./run.sh test       # regression tests (no services needed)
./run.sh ask "Why did build #142 fail?" --mode rca
```

It requires bash, `curl`, and network access to download the Qdrant binary into `.bin/`.

## Appendix B — Docker Compose deploy (VPS)

`deploy/docker-compose.yml` runs Ollama + the app + Caddy (HTTPS + team login) in
containers, against your external Qdrant (local or Cloud). See [`deploy/DEPLOY.md`](deploy/DEPLOY.md) for droplet sizing and the walkthrough.
