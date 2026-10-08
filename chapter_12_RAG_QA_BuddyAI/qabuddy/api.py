"""HTTP API + the built web UI, one process, one port.

    GET  /api/health            dependencies, index size, models
    GET  /api/sources           the knowledge sources with chunk counts
    GET  /api/modes             task modes and example questions
    POST /api/chat              streamed answer (Server-Sent Events)
    POST /api/search            retrieval only, with the full trace
    GET  /api/chunk/{id}        one chunk, for the source viewer
    POST /api/ingest            start (re)indexing in the background
    GET  /api/ingest/status     progress of the current run
    POST /api/jira/sync         pull tickets by JQL, then ingest them
"""

from __future__ import annotations

import json
import threading
import time
from dataclasses import asdict
from pathlib import Path

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from . import __version__, llm, rerank, store
from .answer import MODES, answer_stream
from .chunkers import iter_files
from .config import ROOT, settings, sources
from .ingest import ingest, load_manifest, source_counts
from .retrieve import retrieve

app = FastAPI(title="QABuddy.ai", version=__version__)
UI_DIST = ROOT / "ui" / "dist"

_job = {"running": False, "stage": "idle", "done": 0, "total": 0, "started": None, "finished": None, "report": None, "error": None}


@app.on_event("startup")
def _startup() -> None:
    try:
        store.create_collection(recreate=False)
    except Exception as e:  # Qdrant down: health will say so
        print(f"[startup] qdrant not ready: {e}")
    threading.Thread(target=rerank.load, daemon=True).start()  # first query should not pay the model load


@app.get("/api/health")
def health() -> dict:
    s = settings()
    out = {"version": __version__, "qdrant": False, "ollama": False, "embed_model_ready": False, "points": 0}
    try:
        out["points"] = store.count()
        out["qdrant"] = True
    except Exception as e:
        out["qdrant_error"] = str(e)
    try:
        tags = httpx.get(f"{s.ollama_url}/api/tags", timeout=3).json()
        out["ollama"] = True
        out["embed_model_ready"] = any(m.get("name", "").startswith(s.embed_model) for m in tags.get("models", []))
    except Exception:
        pass
    m = load_manifest()
    out.update(
        {
            "embed_model": s.embed_model,
            "embed_dim": s.embed_dim,
            "vector_db": f"Qdrant ({s.collection})",
            "llm_provider": s.llm_provider,
            "llm_model": s.llm_model,
            "llm_configured": llm.configured(),
            "reranker": rerank.status(),
            "jira_configured": s.jira_configured,
            "indexed_at": m.get("updated_at"),
            "index_model": m.get("embed_model"),
        }
    )
    return out


@app.get("/api/sources")
def list_sources() -> list[dict]:
    counts = source_counts()
    out = []
    for src in sources():
        files_on_disk = sum(1 for _ in iter_files(src)) if src.phase == 1 else 0
        c = counts.get(src.id, {})
        out.append(
            {
                "id": src.id,
                "label": src.label,
                "kind": src.kind,
                "path": src.rel_path,
                "description": src.description,
                "phase": src.phase,
                "files_on_disk": files_on_disk,
                "files_indexed": c.get("files", 0),
                "chunks": c.get("chunks", 0),
                "indexed_at": c.get("indexed_at"),
            }
        )
    return out


@app.get("/api/modes")
def list_modes() -> list[dict]:
    return [asdict(m) for m in MODES.values()]


class ChatReq(BaseModel):
    question: str
    mode: str = "ask"
    sources: list[str] | None = None
    history: list[dict] | None = None


@app.post("/api/chat")
def chat(req: ChatReq):
    if not req.question.strip():
        raise HTTPException(400, "Empty question.")
    if not llm.configured():
        raise HTTPException(503, f"The answer LLM is not configured. Set the API key for LLM_PROVIDER={settings().llm_provider} in .env.")

    def events():
        try:
            for evt in answer_stream(req.question.strip()[:2000], req.mode, req.sources or None, (req.history or [])[-6:]):
                yield f"data: {json.dumps(evt, default=str)}\n\n"
        except Exception as e:  # surface the failure in the stream, the UI shows it
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

    return StreamingResponse(events(), media_type="text/event-stream", headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


class SearchReq(BaseModel):
    question: str
    sources: list[str] | None = None
    k: int | None = None


@app.post("/api/search")
def search(req: SearchReq) -> dict:
    return retrieve(req.question, source_ids=req.sources or None, k=req.k).public()


@app.get("/api/chunk/{point_id}")
def chunk(point_id: str) -> dict:
    p = store.get(point_id)
    if not p:
        raise HTTPException(404, "Chunk not found.")
    return p


class IngestReq(BaseModel):
    sources: list[str] | None = None
    full: bool = False


def _run_ingest(source_ids, full) -> None:
    def progress(stage, done, total):
        _job.update(stage=stage, done=done, total=total)

    try:
        _job["report"] = ingest(source_ids, full, progress)
    except Exception as e:
        _job["error"] = str(e)
    finally:
        _job.update(running=False, finished=time.time())


@app.post("/api/ingest")
def start_ingest(req: IngestReq) -> dict:
    if _job["running"]:
        raise HTTPException(409, "An ingestion is already running.")
    _job.update(running=True, stage="starting", done=0, total=0, started=time.time(), finished=None, report=None, error=None)
    threading.Thread(target=_run_ingest, args=(req.sources, req.full), daemon=True).start()
    return {"started": True}


@app.get("/api/ingest/status")
def ingest_status() -> dict:
    return _job


class JiraReq(BaseModel):
    jql: str | None = None


@app.post("/api/jira/sync")
def jira_sync(req: JiraReq) -> dict:
    from .jira_sync import sync

    try:
        out = sync(req.jql)
    except RuntimeError as e:
        raise HTTPException(400, str(e))
    if not _job["running"]:
        _job.update(running=True, stage="starting", done=0, total=0, started=time.time(), finished=None, report=None, error=None)
        threading.Thread(target=_run_ingest, args=(["jira"], False), daemon=True).start()
    return out


# ---- web UI (built by `npm run build` in ui/) ----
if (UI_DIST / "assets").exists():
    app.mount("/assets", StaticFiles(directory=UI_DIST / "assets"), name="assets")


@app.get("/{path:path}", include_in_schema=False)
def spa(path: str):
    target = UI_DIST / path
    if path and target.is_file() and UI_DIST in target.resolve().parents:
        return FileResponse(target)
    index = UI_DIST / "index.html"
    if index.exists():
        return FileResponse(index)
    return JSONResponse({"message": "QABuddy API is running. Build the UI with `cd ui && npm run build`."})
