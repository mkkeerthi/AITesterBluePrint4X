"""Meeting notes and recording transcripts.

* Markdown notes with headings are split by section (agenda item) via docs.py
* Transcripts (TXT / VTT / SRT) are split into speaker turns, windowed to
  ~TARGET_TOKENS with one turn of overlap, so an answer that spans a
  hand-off between speakers is never cut in half
* Decisions and action items are also pulled into their own chunk: they are
  what people ask about ("who owns the allowlist fix?") and they get buried
  in the middle of a transcript otherwise
"""

from __future__ import annotations

import re
from pathlib import Path

from ..config import Source
from ..models import Chunk
from ..text import approx_tokens, normalize
from .docs import chunk_markdown_text, clean_title

TARGET_TOKENS = 400
OVERLAP_TURN_MAX = 80

_VTT_TIME = re.compile(r"^\d{2}:\d{2}(?::\d{2})?[.,]\d{3}\s*-->\s*\d{2}:\d{2}(?::\d{2})?[.,]\d{3}.*$")
_VTT_VOICE = re.compile(r"<v\s+([^>]+)>(.*?)(?:</v>)?$")
_TURN = re.compile(r"^\s*(?:\[?\(?(?P<ts>\d{1,2}:\d{2}(?::\d{2})?)\)?\]?\s*)?(?P<speaker>[A-Z][\w .'()-]{0,40}?):\s+(?P<text>.+)$")
_DATE = re.compile(r"(20\d{2})[-_/.](\d{2})[-_/.](\d{2})")
_ACTION_HEAD = re.compile(r"^\s*(decisions?|action items?|next steps|actions)\s*:?\s*$", re.I)
_META = re.compile(r"^\s*(meeting|date|attendees|participants)\s*:\s*(.+)$", re.I)


def _from_subtitles(text: str) -> str:
    out = []
    for line in text.split("\n"):
        s = line.strip()
        if not s or s == "WEBVTT" or s.isdigit() or _VTT_TIME.match(s) or s.startswith(("NOTE", "STYLE")):
            continue
        m = _VTT_VOICE.match(s)
        out.append(f"{m.group(1).strip()}: {m.group(2).strip()}" if m else s)
    return "\n".join(out)


def chunk_transcript(path: Path, source: Source, rel: str) -> list[Chunk]:
    raw = normalize(path.read_text(encoding="utf-8", errors="replace"))
    if path.suffix.lower() in {".vtt", ".srt"}:
        raw = _from_subtitles(raw)

    title = clean_title(path.stem)
    dm = _DATE.search(path.stem) or _DATE.search(raw)
    date = f"{dm.group(1)}-{dm.group(2)}-{dm.group(3)}" if dm else ""
    base_meta = {"meeting_title": title, "meeting_date": date}

    # structured notes: let the section chunker follow the agenda headings
    if re.search(r"^#{1,3}\s", raw, re.M):
        return chunk_markdown_text(raw, source=source, rel=rel, doc_title=f"Meeting notes: {title}", meta=base_meta)

    header_lines, turns, actions = [], [], []
    in_actions = False
    for line in raw.split("\n"):
        if not line.strip():
            continue
        if _ACTION_HEAD.match(line):
            in_actions = True
            actions.append(line.strip())
            continue
        if in_actions:
            actions.append(line.strip())
            continue
        mm = _META.match(line)
        if mm and not turns:
            header_lines.append(f"{mm.group(1).title()}: {mm.group(2).strip()}")
            continue
        m = _TURN.match(line)
        if m and len(m.group("speaker").split()) <= 5:
            speaker = m.group("speaker").strip()
            if turns and turns[-1]["speaker"] == speaker:
                turns[-1]["text"] += " " + m.group("text").strip()
            else:
                turns.append({"speaker": speaker, "ts": m.group("ts") or "", "text": m.group("text").strip()})
        elif turns:
            turns[-1]["text"] += " " + line.strip()
        else:
            header_lines.append(line.strip())

    speakers = sorted({t["speaker"] for t in turns})
    head = f"Meeting: {title}" + (f" ({date})" if date else "")
    if header_lines:
        head += "\n" + "\n".join(header_lines[:4])
    meta = {**base_meta, "speakers": speakers}

    chunks: list[Chunk] = []

    def emit(body: str, locator: str, label: str) -> None:
        chunks.append(
            Chunk(
                text=f"{head}\n\n{body}",
                body=body,
                source_id=source.id,
                source_kind=source.kind,
                file_path=rel,
                title=f"{title} · {label}",
                locator=locator,
                meta=meta,
            )
        )

    window: list[dict] = []
    for t in turns:
        line_tokens = approx_tokens(t["text"])
        if window and sum(approx_tokens(w["text"]) for w in window) + line_tokens > TARGET_TOKENS:
            first, last = window[0], window[-1]
            emit(
                "\n".join(f"[{w['ts']}] {w['speaker']}: {w['text']}" if w["ts"] else f"{w['speaker']}: {w['text']}" for w in window),
                f"{first['ts'] or 'start'}-{last['ts'] or 'end'}",
                f"turns {first['ts'] or ''}".strip(),
            )
            tail = window[-1]
            window = [tail] if approx_tokens(tail["text"]) <= OVERLAP_TURN_MAX else []
        window.append(t)
    if window:
        first, last = window[0], window[-1]
        emit(
            "\n".join(f"[{w['ts']}] {w['speaker']}: {w['text']}" if w["ts"] else f"{w['speaker']}: {w['text']}" for w in window),
            f"{first['ts'] or 'start'}-{last['ts'] or 'end'}",
            "discussion" if not first["ts"] else f"turns from {first['ts']}",
        )

    if actions:
        emit("\n".join(actions), "decisions and action items", "decisions and action items")
    if not chunks and raw.strip():
        emit(raw, "whole file", "notes")
    return chunks
