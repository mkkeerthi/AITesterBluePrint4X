"""Ingestion: discover -> hash -> chunk -> BM25 + dense -> upsert.

Incremental by design: a manifest records the sha256 of every file indexed,
so a re-run only re-chunks and re-embeds files that changed, and deletes the
points of files that disappeared. Phase 2's hourly auto-ingest is just this
function on a schedule (plus `git pull` and `sync-jira` before it).

Changing EMBED_MODEL or EMBED_DIM forces a full rebuild, because vectors from
two different models are not comparable.
"""

from __future__ import annotations

import hashlib
import json
import time
from datetime import datetime, timezone
from typing import Callable

from . import store
from .chunkers import chunk_file, iter_files
from .config import ROOT, settings, sources
from .embed import embed_documents
from .sparse import encode_document, terms

Progress = Callable[[str, int, int], None]

# Bump when a chunker changes: files are re-chunked even if their bytes did not.
PIPELINE_VERSION = "2026-10-03.3"


def manifest_path():
    return settings().index_dir / "manifest.json"


def load_manifest() -> dict:
    p = manifest_path()
    if p.exists():
        return json.loads(p.read_text())
    return {"files": {}}


def save_manifest(m: dict) -> None:
    settings().index_dir.mkdir(parents=True, exist_ok=True)
    manifest_path().write_text(json.dumps(m, indent=1))


def _sha(path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ingest(source_ids: list[str] | None = None, full: bool = False, progress: Progress | None = None, force: bool = False) -> dict:
    s = settings()
    say = progress or (lambda stage, done, total: None)
    t_start = time.perf_counter()
    m = load_manifest()

    dim = store.collection_dim() if store.collection_exists() else None
    model_changed = m.get("embed_model") not in (None, s.embed_model) or m.get("embed_dim") not in (None, s.embed_dim)
    if full or model_changed or dim not in (None, s.embed_dim) or not store.collection_exists():
        store.create_collection(recreate=True)
        m = {"files": {}}
        full = True

    if m.get("pipeline_version") not in (None, PIPELINE_VERSION):
        force = True  # chunking logic changed since the last run
    report: dict = {"full_rebuild": full, "forced": force, "sources": {}, "removed_files": [], "skipped_sources": []}
    plan = []  # (source, path, rel, sha)
    on_disk: set[str] = set()
    for src in sources():
        if source_ids and src.id not in source_ids:
            continue
        if src.phase > 1:
            report["skipped_sources"].append({"id": src.id, "reason": f"phase {src.phase}"})
            continue
        stats = {"label": src.label, "files": 0, "changed": 0, "unchanged": 0, "chunks": 0, "errors": []}
        for f in iter_files(src):
            rel = f.resolve().relative_to(ROOT).as_posix()
            on_disk.add(rel)
            stats["files"] += 1
            sha = _sha(f)
            prev = m["files"].get(rel)
            if prev and prev.get("sha") == sha and not full and not force:
                stats["unchanged"] += 1
                stats["chunks"] += prev.get("chunks", 0)
                continue
            plan.append((src, f, rel, sha))
            stats["changed"] += 1
        report["sources"][src.id] = stats

    # files that vanished from a source we just scanned
    scanned = set(report["sources"])
    for rel, info in list(m["files"].items()):
        if info.get("source_id") in scanned and rel not in on_disk:
            store.delete_file(rel)
            m["files"].pop(rel)
            report["removed_files"].append(rel)

    # chunk
    t0 = time.perf_counter()
    file_chunks: list[tuple[str, str, str, list]] = []  # (rel, sha, source_id, chunks)
    for i, (src, f, rel, sha) in enumerate(plan, start=1):
        say("chunking", i, len(plan))
        try:
            chunks = chunk_file(f, src)
        except Exception as e:  # one bad file must not stop the run
            report["sources"][src.id]["errors"].append(f"{rel}: {e}")
            continue
        file_chunks.append((rel, sha, src.id, chunks))
        report["sources"][src.id]["chunks"] += len(chunks)
    chunk_ms = (time.perf_counter() - t0) * 1000
    all_new = [c for _, _, _, cs in file_chunks for c in cs]

    # BM25 needs the corpus-wide average document length
    lengths = [len(terms(c.text)) for c in all_new]
    kept_terms = sum(v.get("terms", 0) for rel, v in m["files"].items() if rel not in {r for r, *_ in file_chunks})
    kept_chunks = sum(v.get("chunks", 0) for rel, v in m["files"].items() if rel not in {r for r, *_ in file_chunks})
    avg_len = (kept_terms + sum(lengths)) / max(1, kept_chunks + len(all_new))

    t0 = time.perf_counter()
    sparse = [encode_document(c.text, avg_len)[0] for c in all_new]
    sparse_ms = (time.perf_counter() - t0) * 1000

    t0 = time.perf_counter()
    dense = embed_documents([c.text for c in all_new], progress=lambda n: say("embedding", n, len(all_new))) if all_new else []
    embed_ms = (time.perf_counter() - t0) * 1000

    t0 = time.perf_counter()
    offset = 0
    for i, (rel, sha, sid, chunks) in enumerate(file_chunks, start=1):
        say("indexing", i, len(file_chunks))
        n = len(chunks)
        if not full:
            store.delete_file(rel)
        if n:
            store.upsert(chunks, dense[offset: offset + n], sparse[offset: offset + n])
        file_terms = sum(lengths[offset: offset + n])
        offset += n
        m["files"][rel] = {"sha": sha, "source_id": sid, "chunks": n, "terms": file_terms,
                           "indexed_at": datetime.now(timezone.utc).isoformat(timespec="seconds")}
    upsert_ms = (time.perf_counter() - t0) * 1000

    m.update(
        {
            "embed_model": s.embed_model,
            "embed_dim": s.embed_dim,
            "pipeline_version": PIPELINE_VERSION,
            "avg_len": round(avg_len, 2),
            "collection": s.collection,
            "updated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        }
    )
    save_manifest(m)
    report.update(
        {
            "new_chunks": len(all_new),
            "total_points": store.count(),
            "avg_doc_terms": round(avg_len, 1),
            "embed_model": s.embed_model,
            "embed_dim": s.embed_dim,
            "timings_ms": {
                "chunk": round(chunk_ms),
                "bm25": round(sparse_ms),
                "embed": round(embed_ms),
                "upsert": round(upsert_ms),
                "total": round((time.perf_counter() - t_start) * 1000),
            },
            "embed_chunks_per_s": round(len(all_new) / (embed_ms / 1000), 1) if embed_ms > 0 and all_new else None,
        }
    )
    say("done", 1, 1)
    return report


def source_counts() -> dict[str, dict]:
    m = load_manifest()
    out: dict[str, dict] = {}
    for rel, info in m.get("files", {}).items():
        d = out.setdefault(info["source_id"], {"files": 0, "chunks": 0, "indexed_at": None})
        d["files"] += 1
        d["chunks"] += info.get("chunks", 0)
        d["indexed_at"] = max(filter(None, [d["indexed_at"], info.get("indexed_at")]), default=None)
    return out
