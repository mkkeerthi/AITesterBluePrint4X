"""Text normalisation shared by every chunker.

Normalisation is deliberately conservative: it removes things that only add
noise to an embedding (BOMs, zero-width characters, ANSI colour codes,
runs of blank lines) and never rewrites words. Terminology is handled at
query time by glossary.yaml, not by mutating the stored text.
"""

from __future__ import annotations

import re
import unicodedata

_ZERO_WIDTH = re.compile("[​‌‍⁠﻿]")
_ANSI = re.compile(r"\x1b\[[0-9;?]*[ -/]*[@-~]")
_TRAILING_WS = re.compile(r"[ \t]+\n")
_BLANKS = re.compile(r"\n{3,}")


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    text = _ZERO_WIDTH.sub("", text)
    text = text.replace("\r\n", "\n").replace("\r", "\n").replace(" ", " ")
    text = _TRAILING_WS.sub("\n", text)
    text = _BLANKS.sub("\n\n", text)
    return text.strip()


def strip_ansi(text: str) -> str:
    return _ANSI.sub("", text)


def approx_tokens(text: str) -> int:
    """~4 characters per token is close enough for budgeting English and code."""
    return max(1, len(text) // 4)


def rejoin_word_per_line(text: str) -> str:
    """Repair PDFs exported from Google Docs, where every word is its own line.

    Chapter 10 met this on its PRD. If most lines hold a single token, the
    line breaks carry no structure and the words are rejoined into prose.
    """
    lines = [ln.strip() for ln in text.split("\n")]
    lines = [ln for ln in lines if ln]
    if not lines:
        return text
    single = sum(1 for ln in lines if len(ln.split()) == 1)
    if single / len(lines) > 0.6:
        return " ".join(lines)
    return text


def truncate_tokens(text: str, max_tokens: int) -> str:
    limit = max_tokens * 4
    if len(text) <= limit:
        return text
    cut = text[:limit]
    nl = cut.rfind("\n")
    if nl > limit * 0.7:
        cut = cut[:nl]
    return cut + "\n…[truncated]"
