"""Chunker registry: `kind` in sources.yaml -> which files and which chunker."""

from __future__ import annotations

from pathlib import Path
from typing import Callable, Iterator

from ..config import ROOT, Source
from ..models import Chunk
from .code import chunk_code, iter_repo_files
from .diagram import chunk_diagram
from .docs import chunk_docs
from .jira import chunk_jira
from .logs import chunk_logs
from .testcases import chunk_testcases
from .transcript import chunk_transcript

Chunker = Callable[[Path, Source, str], list[Chunk]]

KINDS: dict[str, tuple[set[str], Chunker]] = {
    "testcases": ({".csv", ".xlsx", ".xlsm"}, chunk_testcases),
    "jira": ({".md", ".txt", ".html", ".htm", ".doc"}, chunk_jira),
    "docs": ({".pdf", ".md", ".markdown", ".txt"}, chunk_docs),
    "transcript": ({".txt", ".md", ".vtt", ".srt"}, chunk_transcript),
    "diagram": ({".csv", ".json", ".txt", ".md"}, chunk_diagram),
    "logs": ({".log", ".txt", ".xml", ".out"}, chunk_logs),
}


def iter_files(source: Source) -> Iterator[Path]:
    """Files a source contributes. `_`-prefixed and hidden files are notes, not content."""
    if source.phase > 1 or not source.path.exists():
        return
    if source.kind == "code":
        yield from iter_repo_files(source.path)
        return
    exts, _ = KINDS.get(source.kind, (set(), None))
    for p in sorted(source.path.rglob("*")):
        if p.is_file() and p.suffix.lower() in exts and not p.name.startswith(("_", ".")):
            yield p


def chunk_file(path: Path, source: Source) -> list[Chunk]:
    path = path.resolve()
    rel = path.relative_to(ROOT).as_posix()
    if source.kind == "code":
        chunks = chunk_code(path, source, rel)
    else:
        _, fn = KINDS[source.kind]
        chunks = fn(path, source, rel)
    for i, c in enumerate(chunks):
        c.ordinal = i
    return chunks
