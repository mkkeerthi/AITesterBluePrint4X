"""The one data shape every chunker produces."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Any

# Deterministic ids: the same file + ordinal always maps to the same point, so
# re-ingesting a file overwrites its points instead of duplicating them.
_NS = uuid.UUID("6f1c3a52-9d0e-4c5b-8a77-2b9a1d3e4f60")


def point_id(file_path: str, ordinal: int) -> str:
    return str(uuid.uuid5(_NS, f"{file_path}#{ordinal}"))


@dataclass
class Chunk:
    text: str  # exactly what gets embedded: contextual header + body
    source_id: str  # "test_cases", "selenium", ...
    source_kind: str  # "testcases", "code", ...
    file_path: str  # project-relative, posix
    title: str  # human label used in citations
    locator: str  # "row 3", "L12-L40", "p.2 §4.1", "VWO-26"
    meta: dict[str, Any] = field(default_factory=dict)
    body: str | None = None  # text shown in the source viewer (defaults to text)
    ordinal: int = 0  # position within the file, set by the ingester

    @property
    def id(self) -> str:
        return point_id(self.file_path, self.ordinal)

    def payload(self) -> dict[str, Any]:
        p = {
            "text": self.text,
            "body": self.body if self.body is not None else self.text,
            "source_id": self.source_id,
            "source_kind": self.source_kind,
            "file_path": self.file_path,
            "title": self.title,
            "locator": self.locator,
            "ordinal": self.ordinal,
        }
        # meta keys are flattened into the payload so they can be filtered on
        for k, v in self.meta.items():
            if v not in (None, "", [], {}):
                p[k] = v
        return p
