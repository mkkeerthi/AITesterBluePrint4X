"""JIRA tickets: the ticket body is one chunk, each comment is its own chunk.

Two input formats are understood:

1. Jira's "printable view" export (what is in data/01_JIRA_Tickets today):
       [VWO-26] Login failure ... Created: 04/Apr/26  Updated: 04/Apr/26
       Status:\tTo Do
       Type:\tBug\tPriority:\tMedium
        Description
       ...
2. Markdown with YAML front matter, written by `python -m qabuddy sync-jira`.

The ticket key always comes from the content, never the filename: in this
repo `Bug_VWO_32.md` actually contains VWO-33.
"""

from __future__ import annotations

import html
import re
from pathlib import Path

import yaml

from ..config import Source, settings
from ..models import Chunk
from ..text import approx_tokens, normalize

_TITLE = re.compile(
    r"^\[(?P<key>[A-Z][A-Z0-9_]+-\d+)\]\s*(?P<summary>.+?)"
    r"(?:\s+Created:\s*(?P<created>\S+))?(?:\s+Updated:\s*(?P<updated>\S+))?\s*$",
    re.M,
)
_DESC_MARK = re.compile(r"^[ \t]*Description[ \t]*$", re.M)
_COMMENTS_MARK = re.compile(r"^[ \t]*Comments?[ \t]*$", re.M)
_COMMENT = re.compile(r"^Comment by (?P<author>.+?)\s*\[\s*(?P<date>[^\]]+?)\s*\]\s*$", re.M)
_FOOTER = re.compile(r"^Generated at .+$", re.M)
_NOISE_VALUES = {"none", "not specified", "", "0"}
_FIELD_KEYS = {
    "status": "status",
    "project": "project",
    "components": "components",
    "type": "issue_type",
    "priority": "priority",
    "reporter": "reporter",
    "assignee": "assignee",
    "resolution": "resolution",
    "labels": "labels",
    "affects versions": "affects_versions",
    "fix versions": "fix_versions",
    "sprint": "sprint",
}


def _html_to_text(raw: str) -> str:
    raw = re.sub(r"(?is)<(script|style).*?</\1>", " ", raw)
    raw = re.sub(r"(?i)<br\s*/?>|</(p|div|tr|li|h\d)>", "\n", raw)
    raw = re.sub(r"(?i)</t[dh]>", "\t", raw)
    raw = re.sub(r"<[^>]+>", " ", raw)
    return html.unescape(raw)


def _parse_printable(text: str) -> dict | None:
    m = _TITLE.search(text)
    if not m:
        return None
    t = {
        "key": m.group("key"),
        "summary": m.group("summary").strip(),
        "created": m.group("created") or "",
        "updated": m.group("updated") or "",
        "fields": {},
        "description": "",
        "comments": [],
    }
    head_end = _DESC_MARK.search(text, m.end())
    head = text[m.end(): head_end.start() if head_end else len(text)]
    for line in head.splitlines():
        cells = [c.strip() for c in line.split("\t")]
        i = 0
        while i < len(cells):
            if cells[i].endswith(":"):
                key = cells[i][:-1].strip().lower()
                value = cells[i + 1] if i + 1 < len(cells) else ""
                if key in _FIELD_KEYS and value.lower() not in _NOISE_VALUES:
                    t["fields"][_FIELD_KEYS[key]] = value
                i += 2
            else:
                i += 1

    if head_end:
        body = text[head_end.end():]
        body = _FOOTER.split(body)[0]
        comments_at = _COMMENTS_MARK.search(body)
        desc = body[: comments_at.start()] if comments_at else body
        t["description"] = normalize(desc)
        if comments_at:
            blocks = list(_COMMENT.finditer(body, comments_at.end()))
            for j, c in enumerate(blocks):
                end = blocks[j + 1].start() if j + 1 < len(blocks) else len(body)
                t["comments"].append(
                    {"author": c.group("author"), "date": c.group("date"), "body": normalize(body[c.end(): end])}
                )
    return t


def _parse_front_matter(text: str) -> dict | None:
    if not text.startswith("---"):
        return None
    parts = text.split("\n---", 2)
    if len(parts) < 2:
        return None
    meta = yaml.safe_load(parts[0].lstrip("-\n")) or {}
    body = parts[1].lstrip("-\n") if len(parts) == 2 else parts[1] + parts[2]
    if not meta.get("key"):
        return None
    desc, _, comments_raw = body.partition("## Comments")
    desc = re.sub(r"^\s*## Description\s*", "", desc.strip())
    comments = []
    for c in re.finditer(r"^### (?P<author>.+?) · (?P<date>.+?)\n(?P<body>.*?)(?=^### |\Z)", comments_raw, re.M | re.S):
        comments.append({"author": c.group("author"), "date": c.group("date"), "body": normalize(c.group("body"))})
    fields = {k: str(v) for k, v in meta.items() if k not in {"key", "summary", "created", "updated", "url"} and v}
    return {
        "key": meta["key"],
        "summary": str(meta.get("summary", "")),
        "created": str(meta.get("created", "")),
        "updated": str(meta.get("updated", "")),
        "url": meta.get("url"),
        "fields": fields,
        "description": normalize(desc),
        "comments": comments,
    }


def parse_ticket(text: str) -> dict | None:
    text = text.replace("\r\n", "\n")
    if re.search(r"(?i)<html|<body|<table", text[:2000]):
        text = _html_to_text(text)
    return _parse_front_matter(text) or _parse_printable(text)


def _split(text: str, max_tokens: int = 500) -> list[str]:
    if approx_tokens(text) <= max_tokens:
        return [text]
    paras = [p for p in re.split(r"\n\s*\n", text) if p.strip()]
    out, cur = [], ""
    for p in paras:
        if cur and approx_tokens(cur + "\n\n" + p) > max_tokens:
            out.append(cur)
            cur = out[-1].split("\n\n")[-1] + "\n\n" + p  # one-paragraph overlap
        else:
            cur = f"{cur}\n\n{p}" if cur else p
    if cur:
        out.append(cur)
    return out


def chunk_jira(path: Path, source: Source, rel: str) -> list[Chunk]:
    t = parse_ticket(path.read_text(encoding="utf-8", errors="replace"))
    if not t:
        return []
    key, f = t["key"], t["fields"]
    url = t.get("url") or (f"{settings().jira_base_url}/browse/{key}" if settings().jira_configured else None)

    facts = [f"Type: {f.get('issue_type', 'Unknown')}", f"Status: {f.get('status', 'Unknown')}"]
    for k, label in (("priority", "Priority"), ("project", "Project"), ("resolution", "Resolution")):
        if f.get(k):
            facts.append(f"{label}: {f[k]}")
    people = [f"{label}: {f[k]}" for k, label in (("reporter", "Reporter"), ("assignee", "Assignee")) if f.get(k)]
    dates = [f"{label}: {t[k]}" for k, label in (("created", "Created"), ("updated", "Updated")) if t.get(k)]
    tags = [f"{label}: {f[k]}" for k, label in (("labels", "Labels"), ("components", "Components"), ("sprint", "Sprint")) if f.get(k)]

    header = "\n".join(
        [f"Jira {key}: {t['summary']}", " | ".join(facts), " | ".join(people + dates)] + ([" | ".join(tags)] if tags else [])
    )
    meta = {
        "jira_key": key,
        "summary": t["summary"],
        "issue_type": f.get("issue_type"),
        "status": f.get("status"),
        "priority": f.get("priority"),
        "reporter": f.get("reporter"),
        "assignee": f.get("assignee"),
        "labels": f.get("labels"),
        "created": t.get("created"),
        "updated": t.get("updated"),
        "url": url,
    }

    chunks: list[Chunk] = []
    parts = _split(t["description"] or "(no description)")
    for i, part in enumerate(parts, start=1):
        label = f" (part {i}/{len(parts)})" if len(parts) > 1 else ""
        chunks.append(
            Chunk(
                text=f"{header}\n\nDescription{label}:\n{part}",
                source_id=source.id,
                source_kind=source.kind,
                file_path=rel,
                title=f"{key} · {t['summary']}",
                locator=key if len(parts) == 1 else f"{key} part {i}",
                meta=meta,
            )
        )
    for n, c in enumerate(t["comments"], start=1):
        chunks.append(
            Chunk(
                text=f"Jira {key}: {t['summary']}\nComment by {c['author']} on {c['date']}:\n{c['body']}",
                source_id=source.id,
                source_kind=source.kind,
                file_path=rel,
                title=f"{key} · comment by {c['author']}",
                locator=f"{key} comment {n}",
                meta={**meta, "comment_author": c["author"], "comment_date": c["date"]},
            )
        )
    return chunks
