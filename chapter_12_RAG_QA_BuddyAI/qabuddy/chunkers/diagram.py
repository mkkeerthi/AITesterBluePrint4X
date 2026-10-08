"""Lucid charts exported to text.

A diagram's meaning is in its edges ("Credentials valid? -> No -> show
error"), and pixels are useless to a text embedding. So exports are turned
into sentences:

* Lucid CSV shape data: shapes become a node list, lines become
  "A -> [label] -> B" flows, per page
* JSON exports with nodes/edges (or anything else: flattened to key paths)
* Text / Markdown exports: section chunking via docs.py
"""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path

from ..config import Source
from ..models import Chunk
from ..text import approx_tokens, normalize
from .docs import chunk_docs, clean_title

TARGET_TOKENS = 600  # one diagram per chunk where possible: flows reference their nodes


def _windows(lines: list[str], header: str) -> list[str]:
    out, cur = [], []
    for ln in lines:
        if cur and approx_tokens(header + "\n".join(cur + [ln])) > TARGET_TOKENS:
            out.append("\n".join(cur))
            cur = []
        cur.append(ln)
    if cur:
        out.append("\n".join(cur))
    return out


def _from_lucid_csv(path: Path) -> list[tuple[str, list[str], list[str]]]:
    with path.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows or "Name" not in rows[0]:
        return []
    text_cols = [c for c in rows[0] if c and c.lower().startswith("text area")]

    def label(r: dict) -> str:
        return " ".join((r.get(c) or "").strip() for c in text_cols if (r.get(c) or "").strip())

    pages = {r["Id"]: label(r) or f"Page {r['Id']}" for r in rows if (r.get("Name") or "").lower() == "page"}
    shapes = {r["Id"]: r for r in rows if (r.get("Name") or "").lower() not in {"page", "line"}}
    out = []
    for pid, ptitle in (pages or {"": path.stem}).items():
        nodes, flows = [], []
        for r in rows:
            if pages and r.get("Page ID") != pid:
                continue
            name = (r.get("Name") or "").lower()
            if name == "line":
                src, dst = shapes.get(r.get("Line Source", "")), shapes.get(r.get("Line Destination", ""))
                if src and dst:
                    edge = label(r)
                    flows.append(f"- {label(src)} -> {('[' + edge + '] -> ') if edge else ''}{label(dst)}")
            elif name != "page" and label(r):
                kind = (r.get("Name") or "shape").lower()
                note = (r.get("Comments") or "").strip()
                nodes.append(f"- ({kind}) {label(r)}" + (f"  Note: {note}" if note else ""))
        out.append((ptitle, nodes, flows))
    return out


def _from_json(path: Path) -> tuple[str, list[str], list[str]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    title = str(data.get("title") or clean_title(path.stem)) if isinstance(data, dict) else clean_title(path.stem)
    if isinstance(data, dict):
        nodes = data.get("nodes") or data.get("shapes") or data.get("items")
        edges = data.get("edges") or data.get("lines") or data.get("links")
        if isinstance(nodes, list) and isinstance(edges, list):
            label = {}
            for n in nodes:
                nid = str(n.get("id"))
                label[nid] = str(n.get("label") or n.get("text") or n.get("name") or nid)
            node_lines = [f"- {v}" for v in label.values()]
            flows = []
            for e in edges:
                a = label.get(str(e.get("from") or e.get("source")), str(e.get("from") or e.get("source")))
                b = label.get(str(e.get("to") or e.get("target")), str(e.get("to") or e.get("target")))
                lab = e.get("label") or e.get("text")
                flows.append(f"- {a} -> {('[' + str(lab) + '] -> ') if lab else ''}{b}")
            return title, node_lines, flows

    lines: list[str] = []

    def walk(x, prefix=""):
        if isinstance(x, dict):
            for k, v in x.items():
                walk(v, f"{prefix}.{k}" if prefix else str(k))
        elif isinstance(x, list):
            for i, v in enumerate(x):
                walk(v, f"{prefix}[{i}]")
        elif x not in (None, ""):
            lines.append(f"{prefix}: {x}")

    walk(data)
    return title, lines, []


def chunk_diagram(path: Path, source: Source, rel: str) -> list[Chunk]:
    suffix = path.suffix.lower()
    if suffix in {".md", ".markdown", ".txt", ".pdf"}:
        chunks = chunk_docs(path, source, rel)
        for c in chunks:
            c.meta["diagram_title"] = clean_title(path.stem)
        return chunks

    pages: list[tuple[str, list[str], list[str]]] = []
    if suffix == ".csv":
        pages = _from_lucid_csv(path)
    elif suffix == ".json":
        pages = [_from_json(path)]

    chunks: list[Chunk] = []
    for ptitle, nodes, flows in pages:
        header = f"Diagram: {ptitle} (Lucid export {path.name})"
        body_lines = (["Steps and decisions:"] + nodes if nodes else []) + (["Flows:"] + flows if flows else [])
        for i, body in enumerate(_windows(body_lines, header), start=1):
            body = normalize(body)
            chunks.append(
                Chunk(
                    text=f"{header}\n\n{body}",
                    body=body,
                    source_id=source.id,
                    source_kind=source.kind,
                    file_path=rel,
                    title=f"{ptitle}" + (f" (part {i})" if i > 1 else ""),
                    locator=f"page '{ptitle}'" + (f" part {i}" if i > 1 else ""),
                    meta={"diagram_title": ptitle, "nodes": len(nodes), "edges": len(flows)},
                )
            )
    return chunks
