"""Export the hosted demo: recorded full-pipeline runs + the chunk corpus.

A public Vercel page cannot reach your private Qdrant (local or Qdrant Cloud),
Ollama or a GPU reranker. So the demo ships three things:

  ui/public/demo/demo.json    health snapshot, sources, modes, glossary, and
                              every example question answered by the FULL
                              pipeline (dense + BM25 + RRF + rerank + LLM),
                              recorded with its complete retrieval trace
  ui/public/demo/corpus.json  every chunk, for the source viewer and for the
                              browser-side BM25 that answers new questions
  api/_prompt.js              the system prompt and mode instructions, so the
                              serverless answer function matches the real one
"""

from __future__ import annotations

import json
import time
from dataclasses import asdict
from datetime import datetime, timezone

from . import store
from .answer import MODES, SYSTEM, answer_stream
from .api import health, list_sources
from .config import ROOT, glossary, settings, source_by_id
from .retrieve import META_KEYS

OUT = ROOT / "ui" / "public" / "demo"
PACE_S = 32
EXTRA_META = ("summary", "modules", "repo", "code_kind", "scenario", "test_name", "error_template")


def _key(question: str, mode: str) -> str:
    q = " ".join(question.strip().lower().split()).rstrip("?.!")
    return f"{mode}::{q}"


def _corpus() -> list[dict]:
    out, offset = [], None
    while True:
        pts, offset = store.client().scroll(settings().collection, limit=256, offset=offset, with_payload=True, with_vectors=False)
        for p in pts:
            pl = p.payload or {}
            src = source_by_id(pl.get("source_id", ""))
            body = pl.get("body")
            out.append(
                {
                    "id": str(p.id),
                    "source_id": pl.get("source_id"),
                    "source_label": src.label if src else pl.get("source_id"),
                    "source_kind": pl.get("source_kind"),
                    "title": pl.get("title"),
                    "locator": pl.get("locator"),
                    "file_path": pl.get("file_path"),
                    "text": pl.get("text", ""),
                    **({"body": body} if body and body != pl.get("text") else {}),
                    "meta": {k: pl[k] for k in (*META_KEYS, *EXTRA_META) if k in pl},
                }
            )
        if offset is None:
            break
    out.sort(key=lambda c: (c["source_id"] or "", c["file_path"] or "", c["title"] or ""))
    return out


def export(only: list[str] | None = None) -> None:
    """Record every example question; with `only`, re-record just the matching ones."""
    OUT.mkdir(parents=True, exist_ok=True)
    recorded: dict[str, dict] = {}
    if only and (OUT / "demo.json").exists():
        recorded = json.loads((OUT / "demo.json").read_text())["recorded"]
    current = {_key(q, m.id) for m in MODES.values() for q in m.examples}
    recorded = {k: v for k, v in recorded.items() if k in current}  # drop retired examples
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    questions = [(q, m.id) for m in MODES.values() for q in m.examples]
    recorded_now = 0
    for i, (q, mode_id) in enumerate(questions, start=1):
        if only and not any(o.lower() in q.lower() for o in only):
            continue
        if recorded_now:
            # stay under Groq's on-demand 8k tokens/minute so recordings show real
            # latency, not time spent queued behind the rate limit
            time.sleep(PACE_S)
        recorded_now += 1
        events = list(answer_stream(q, mode_id))
        retrieval = next(e for e in events if e["type"] == "retrieval")
        done = next(e for e in events if e["type"] == "done")
        recorded[_key(q, mode_id)] = {"retrieval_event": retrieval, "done": done, "recorded_at": now}
        cites = done["citations"]
        print(f"  [{i:2d}/{len(questions)}] {mode_id:11s} cited={cites['used']} grounded={cites['grounded']}  {q[:70]}", flush=True)

    h = health()
    h.update({"demo": True})
    eval_path = ROOT / "eval" / "last_run.json"
    demo = {
        "recorded_at": now,
        "health": h,
        "sources": list_sources(),
        "modes": [asdict(m) for m in MODES.values()],
        "glossary": glossary(),
        "recorded": recorded,
        "eval": json.loads(eval_path.read_text())["summary"] if eval_path.exists() else None,
    }
    corpus = _corpus()
    (OUT / "demo.json").write_text(json.dumps(demo, default=str))
    (OUT / "corpus.json").write_text(json.dumps(corpus, default=str))

    prompt = {
        "system": SYSTEM,
        "model": settings().llm_model,
        "modes": {m.id: {"label": m.label, "instruction": m.instruction, "max_tokens": m.max_tokens} for m in MODES.values()},
    }
    api_dir = ROOT / "api"
    api_dir.mkdir(exist_ok=True)
    (api_dir / "_prompt.js").write_text(
        "// Generated by `python -m qabuddy export-demo`. Do not edit by hand.\n"
        f"export default {json.dumps(prompt, indent=1)};\n"
    )
    size = lambda p: f"{p.stat().st_size / 1e6:.2f} MB"  # noqa: E731
    print(f"wrote {OUT / 'demo.json'} ({size(OUT / 'demo.json')}), {len(recorded)} recorded runs")
    print(f"wrote {OUT / 'corpus.json'} ({size(OUT / 'corpus.json')}), {len(corpus)} chunks")
    print(f"wrote {api_dir / '_prompt.js'}")
