"""Prose documents (PDF, Markdown, text): heading-aware sections.

The unit of meaning in a PRD is a section ("4.1 Experimentation & Testing"),
not a page and not N characters. So documents are parsed into blocks
(heading / paragraph / list / table / code), the heading hierarchy is
rebuilt, and chunks follow section boundaries:

* sections up to MAX_TOKENS stay whole
* tiny sibling sections under the same parent are merged (no 20-token chunks)
* only sections longer than MAX_TOKENS are split, at block boundaries, with
  one block (~15%) of overlap so a sentence is never cut away from its context
* every chunk carries a contextual header: document title + section path
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from ..config import Source
from ..models import Chunk
from ..text import approx_tokens, normalize, rejoin_word_per_line

TARGET_TOKENS = 500
MAX_TOKENS = 700
MIN_TOKENS = 120
OVERLAP_TOKENS = 90

_BULLET = re.compile(r"^(?:[●•◦▪■◆➢➤►\-\*\+–]|o(?=\s{2,}))\s+")
_NUM_ITEM = re.compile(r"^(?:\d{1,2}|[a-z])[.)]\s+")
_NUM_HEAD = re.compile(r"^(?P<num>\d{1,2}(?:\.\d{1,2}){0,3})\.?\s+(?P<title>\S.{0,100})$")
_MD_HEAD = re.compile(r"^(?P<hashes>#{1,6})\s+(?P<title>.+?)\s*#*\s*$")
_TABLE_GAP = re.compile(r"\S {3,}\S")
# link placeholders left behind by web-generated docs: "(Website)", "(geteppo.com)"
_LINK_NOISE = re.compile(r"\s*\((?:Website|Link|Source|[a-z0-9-]+\.(?:com|org|io|net|co|ai))\)", re.I)
_SMALL_WORDS = {"a", "an", "and", "as", "at", "by", "for", "in", "of", "on", "or", "the", "to", "via", "vs", "with", "&", "/"}


@dataclass
class Block:
    kind: str  # heading | para | list | table | code
    text: str
    level: int = 0
    number: str = ""
    page: int | None = None
    line_start: int = 0
    line_end: int = 0


@dataclass
class Section:
    path: list[str]
    numbers: list[str]
    blocks: list[Block] = field(default_factory=list)
    merged: list[str] = field(default_factory=list)  # labels of sibling sections folded in

    @property
    def text(self) -> str:
        return "\n\n".join(b.text for b in self.blocks)

    @property
    def tokens(self) -> int:
        return approx_tokens(self.text)


# ----------------------------------------------------------------- parsing


def _is_title_case(text: str) -> bool:
    words = [w for w in re.findall(r"[A-Za-z][\w'/&-]*", text)]
    if not words:
        return False
    big = [w for w in words if w.lower() not in _SMALL_WORDS]
    return bool(big) and sum(w[0].isupper() for w in big) / len(big) >= 0.75


def _heading(line: str, indent: int, prev_blank: bool, next_blank: bool) -> tuple[int, str, str] | None:
    """Return (level, number, title) when a plain-text line is a heading.

    Layout-mode PDFs put real headings at column 0; a table cell that happens
    to start with a number (" 4      Recordings") is indented and has wide
    column gaps, so both disqualify a line.
    """
    if indent > 0 or len(line) > 110 or re.search(r"\S {3,}\S", line):
        return None
    m = _NUM_HEAD.match(line)
    if m:
        title = m.group("title").strip()
        words = title.split()
        if (
            len(words) <= 10
            and title[0].isupper()
            and not re.search(r"[.:;,]$", title)
            and (_is_title_case(title) or len(words) <= 4)
        ):
            return m.group("num").count(".") + 1, m.group("num"), title
        return None
    words = line.split()
    if (
        1 <= len(words) <= 7
        and prev_blank
        and next_blank
        and line[0].isupper()
        and ": " not in line
        and not re.search(r"[.:;,!?]$", line)
        and not _BULLET.match(line)
        and _is_title_case(line)
    ):
        return 0, "", line  # level resolved later (child of the last numbered heading)
    return None


_CELL = re.compile(r"\S+(?: \S+)*")  # a cell: words separated by single spaces


def _join_fragment(prev: str, frag: str) -> str:
    """Rejoin text a PDF table wrapped mid-cell: 'Priorit'+'y', 'Mediu'+'m', 'FR'+'1'."""
    if not prev:
        return frag
    glue = (len(frag) <= 2 and (frag.isdigit() or frag.islower()) and prev[-1].isalnum())
    return prev + ("" if glue else " ") + frag


def _table_block(rows: list[list[list[tuple[int, str]]]], page: int | None, start: int, end: int) -> Block:
    """Rebuild a layout-mode table.

    rows = groups of physical lines (a group is one table row, wrapped over
    several lines); each line is a list of (char_position, cell_text). Column
    starts come from the line shape most lines share: headers are often
    centred differently from the data, so the header alone is a bad guide.
    """
    from collections import Counter

    all_lines = [ln for g in rows for ln in g]
    widest = max(len(ln) for ln in all_lines)
    shapes = Counter(tuple(p for p, _ in ln) for ln in all_lines if len(ln) == widest)
    col_starts = list(shapes.most_common(1)[0][0])
    cols: list[list[str]] = []
    for group in rows:
        cells = [""] * len(col_starts)
        for ln in group:
            for pos, text in ln:
                k = min(range(len(col_starts)), key=lambda j: abs(col_starts[j] - pos))
                cells[k] = _join_fragment(cells[k], text)
        cols.append(cells)
    head, body = cols[0], cols[1:]
    md = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    md += ["| " + " | ".join(r) + " |" for r in body]
    return Block("table", "\n".join(md), page=page, line_start=start, line_end=end)


def _lines_to_blocks(lines: list[tuple[str, int | None, int]]) -> list[Block]:
    """Plain-text / PDF lines -> blocks. lines = (raw_line, page, line_no)."""
    blocks: list[Block] = []
    n = len(lines)
    last_numbered_level = 0

    def clean(i: int) -> str:
        return _LINK_NOISE.sub("", lines[i][0]).rstrip()

    def heading_at(i: int) -> tuple[int, str, str] | None:
        line = clean(i)
        s = line.strip()
        if not s:
            return None
        indent = len(line) - len(line.lstrip(" "))
        prev_blank = i == 0 or not lines[i - 1][0].strip()
        next_blank = i + 1 >= n or not lines[i + 1][0].strip()
        return _heading(s, indent, prev_blank, next_blank)

    def is_item(s: str) -> bool:
        return bool(_BULLET.match(s) or _NUM_ITEM.match(s))

    def has_gap(s: str) -> bool:
        return bool(_TABLE_GAP.search(s)) and not _BULLET.match(s)

    i = 0
    while i < n:
        raw, page, lno = lines[i]
        line = clean(i)
        stripped = line.strip()
        if not stripped:
            i += 1
            continue

        h = heading_at(i)
        if h:
            level, number, title = h
            if number:
                last_numbered_level = level
            else:
                level = last_numbered_level + 1
            blocks.append(Block("heading", title, level=level, number=number, page=page, line_start=lno, line_end=lno))
            i += 1
            continue

        # table region: lines with wide column gaps, rows separated by single
        # blank lines, ended by a double blank, a heading, a bullet or a page break
        if has_gap(stripped):
            j, rows, group, gap_lines, blanks = i, [], [], 0, 0
            while j < n and lines[j][1] == page:
                cur = clean(j)
                if not cur.strip():
                    blanks += 1
                    if blanks >= 2:
                        break
                    if group:
                        rows.append(group)
                        group = []
                    j += 1
                    continue
                if (j > i and heading_at(j)) or _BULLET.match(cur.strip()):
                    break
                blanks = 0
                gap_lines += has_gap(cur.strip())
                group.append([(m.start(), m.group()) for m in _CELL.finditer(cur)])
                j += 1
            if group:
                rows.append(group)
            if gap_lines >= 2 and len(rows) >= 2:
                blocks.append(_table_block(rows, page, lno, lines[j - 1][2]))
                i = j
                continue

        # lists: a run of bullet / numbered items with wrapped continuation lines.
        # A numbered heading ("4. Core Features") also looks like item 4, so the
        # heading check runs first or the list swallows the next section.
        if is_item(stripped):
            items: list[str] = []
            while i < n:
                cs = clean(i).strip()
                if not cs:
                    if i + 1 < n and is_item(clean(i + 1).strip()) and not heading_at(i + 1):
                        i += 1
                        continue
                    break
                if heading_at(i):
                    break
                if _BULLET.match(cs):
                    items.append("- " + _BULLET.sub("", cs))
                elif _NUM_ITEM.match(cs):
                    items.append(re.sub(r"\s+", " ", cs))
                elif items and len(clean(i)) - len(clean(i).lstrip(" ")) > 0:
                    items[-1] += " " + cs
                else:
                    break
                i += 1
            blocks.append(Block("list", "\n".join(items), page=page, line_start=lno, line_end=lines[i - 1][2]))
            continue

        # paragraph: consecutive lines until a blank, an item or a heading
        parts = [stripped]
        i += 1
        while i < n:
            nxt = clean(i).strip()
            if not nxt or is_item(nxt) or heading_at(i) or lines[i][1] != page:
                break
            parts.append(nxt)
            i += 1
        blocks.append(Block("para", " ".join(parts), page=page, line_start=lno, line_end=lines[i - 1][2]))
    return blocks


def _markdown_to_blocks(text: str) -> list[Block]:
    lines = text.split("\n")
    blocks: list[Block] = []
    i = 0
    # front matter (e.g. .mdc rule files) is kept as a small block, not lost
    if lines and lines[0].strip() == "---":
        end = next((j for j in range(1, len(lines)) if lines[j].strip() == "---"), None)
        if end:
            fm = "\n".join(lines[1:end]).strip()
            if fm:
                blocks.append(Block("para", fm, line_start=2, line_end=end))
            i = end + 1
    para: list[str] = []
    para_start = 0

    def flush_para(end_line: int) -> None:
        nonlocal para
        if para:
            blocks.append(Block("para", " ".join(p.strip() for p in para), line_start=para_start, line_end=end_line))
            para = []

    while i < len(lines):
        line = lines[i]
        s = line.strip()
        lno = i + 1
        if s.startswith("```") or s.startswith("~~~"):
            flush_para(lno - 1)
            fence = s[:3]
            body = [line]
            i += 1
            while i < len(lines) and not lines[i].strip().startswith(fence):
                body.append(lines[i])
                i += 1
            if i < len(lines):
                body.append(lines[i])
            blocks.append(Block("code", "\n".join(body), line_start=lno, line_end=i + 1))
            i += 1
            continue
        m = _MD_HEAD.match(s)
        if m:
            flush_para(lno - 1)
            title = m.group("title").strip()
            nm = _NUM_HEAD.match(title)
            blocks.append(
                Block(
                    "heading",
                    nm.group("title").strip() if nm else title,  # "2.1 Structure" -> number 2.1, title Structure
                    level=len(m.group("hashes")),
                    number=nm.group("num") if nm else "",
                    line_start=lno,
                    line_end=lno,
                )
            )
            i += 1
            continue
        if s.startswith("|"):
            flush_para(lno - 1)
            rows, start = [], lno
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(lines[i].strip())
                i += 1
            blocks.append(Block("table", "\n".join(rows), line_start=start, line_end=i))
            continue
        if _BULLET.match(s) or _NUM_ITEM.match(s):
            flush_para(lno - 1)
            items, start = [], lno
            while i < len(lines):
                cur = lines[i]
                cs = cur.strip()
                if not cs:
                    if i + 1 < len(lines) and (_BULLET.match(lines[i + 1].strip()) or _NUM_ITEM.match(lines[i + 1].strip())):
                        i += 1
                        continue
                    break
                if _BULLET.match(cs) or _NUM_ITEM.match(cs):
                    items.append(cs)
                elif items and cur.startswith((" ", "\t")):
                    items[-1] += " " + cs
                else:
                    break
                i += 1
            blocks.append(Block("list", "\n".join(items), line_start=start, line_end=i))
            continue
        if not s:
            flush_para(lno - 1)
            i += 1
            continue
        if not para:
            para_start = lno
        para.append(s)
        i += 1
    flush_para(len(lines))
    return blocks


# --------------------------------------------------------------- sections


def _sections(blocks: list[Block]) -> list[Section]:
    sections: list[Section] = [Section(path=[], numbers=[])]
    stack: list[tuple[int, str, str]] = []
    for b in blocks:
        if b.kind == "heading":
            while stack and stack[-1][0] >= b.level:
                stack.pop()
            stack.append((b.level, b.text, b.number))
            label = f"{b.number} {b.text}".strip() if b.number else b.text
            md = "#" * min(max(b.level, 1) + 1, 6)
            sec = Section(path=[(f"{n} {t}".strip() if n else t) for _, t, n in stack], numbers=[n for _, _, n in stack if n])
            sec.blocks.append(Block("heading", f"{md} {label}", page=b.page, line_start=b.line_start, line_end=b.line_end))
            sections.append(sec)
        else:
            sections[-1].blocks.append(b)
    return [s for s in sections if any(b.kind != "heading" for b in s.blocks)]


def _display_path(path: list[str], doc_title: str) -> list[str]:
    """Section path without a leading H1 that just names the document.

    `doc_title` may hold several names separated by "\x00" (filename title
    and the document's own single H1)."""
    titles = {t.strip().lower() for t in doc_title.split("\x00") if t.strip()}
    if path and path[0].strip().lower() in titles:
        return path[1:]
    return list(path)


def _merge_small(sections: list[Section], doc_title: str) -> list[Section]:
    """Fold tiny sections into a neighbour so no chunk is a lonely heading.

    Allowed merges:
      * siblings under the same (non-root) parent  -> "Waits" + "Locators"
      * a parent whose own text is tiny, with its first child
      * an untitled intro with whatever follows
    Top-level sections stay separate unless both are tiny: "6 Functional
    Requirements" and "8 Success Metrics" are different questions. Merging by
    top-level heading alone would also glue "Selenium > Waits" to
    "Playwright > Structure" in any Markdown file with a single H1.
    """
    out: list[Section] = []
    for s in sections:
        prev = out[-1] if out else None
        if prev is not None:
            pd, sd = _display_path(prev.path, doc_title), _display_path(s.path, doc_title)
            tiny = MIN_TOKENS // 2
            siblings = pd[:-1] == sd[:-1] and (bool(pd[:-1]) or (prev.tokens < tiny and s.tokens < tiny))
            parent_child = sd[: len(pd)] == pd and prev.tokens < tiny
            intro = not pd
            small = prev.tokens < MIN_TOKENS or s.tokens < MIN_TOKENS
            if (siblings or parent_child or intro) and small and prev.tokens + s.tokens <= TARGET_TOKENS:
                prev.blocks.extend(s.blocks)
                if parent_child or intro:  # the tiny parent / intro takes the child's name
                    prev.path, prev.numbers = list(s.path), list(s.numbers)
                else:
                    prev.merged.append(s.path[-1])
                continue
        out.append(Section(path=list(s.path), numbers=list(s.numbers), blocks=list(s.blocks)))
    return out


def _split_block(b: Block) -> list[Block]:
    if approx_tokens(b.text) <= MAX_TOKENS:
        return [b]
    sep = "\n" if b.kind in {"list", "table", "code"} else None
    units = b.text.split("\n") if sep else re.split(r"(?<=[.!?])\s+", b.text)
    out, cur = [], ""
    for u in units:
        if cur and approx_tokens(cur + " " + u) > TARGET_TOKENS:
            out.append(Block(b.kind, cur, page=b.page, line_start=b.line_start, line_end=b.line_end))
            cur = u
        else:
            cur = f"{cur}{sep or ' '}{u}" if cur else u
    if cur:
        out.append(Block(b.kind, cur, page=b.page, line_start=b.line_start, line_end=b.line_end))
    return out


def _windows(section: Section) -> list[list[Block]]:
    if section.tokens <= MAX_TOKENS:
        return [section.blocks]
    blocks = [p for b in section.blocks for p in _split_block(b)]
    heading = blocks[0] if blocks and blocks[0].kind == "heading" else None
    body = blocks[1:] if heading else blocks
    wins: list[list[Block]] = []
    cur: list[Block] = []
    for b in body:
        cur_tokens = sum(approx_tokens(x.text) for x in cur)
        if cur and cur_tokens + approx_tokens(b.text) > TARGET_TOKENS:
            wins.append(cur)
            tail = cur[-1]
            cur = [tail] if approx_tokens(tail.text) <= OVERLAP_TOKENS else []
        cur.append(b)
    if cur:
        wins.append(cur)
    return [([heading] if heading else []) + w for w in wins]


# ------------------------------------------------------------------ public


def doc_type_of(name: str) -> str:
    for t in ("PRD", "SRS", "BRD", "FRD"):
        if re.search(rf"\b{t}\b", name, re.I):
            return t
    return "Doc"


def clean_title(stem: str) -> str:
    stem = re.sub(r"\s*\(\d+\)\s*$", "", stem)
    return re.sub(r"[_]+", " ", stem).strip()


def blocks_to_chunks(
    blocks: list[Block],
    *,
    source: Source,
    rel: str,
    doc_title: str,
    meta: dict,
    url_for: Callable[[int, int], str | None] | None = None,
) -> list[Chunk]:
    chunks: list[Chunk] = []
    # a single leading H1 is the document's title, not a section
    h1 = [b for b in blocks if b.kind == "heading" and b.level == 1]
    first_heading = next((b for b in blocks if b.kind == "heading"), None)
    names = doc_title + ("\x00" + h1[0].text if len(h1) == 1 and first_heading is h1[0] else "")
    for sec in _merge_small(_sections(blocks), names):
        disp = _display_path(sec.path, names)
        parent, siblings = disp[:-1], sec.merged
        if not disp:
            section_label, last = "Introduction", "Introduction"
        elif siblings and parent:
            # a chunk holding several sibling sections is named after their parent
            section_label = " > ".join(parent) + " > " + ", ".join([disp[-1]] + siblings)
            last = parent[-1]
        elif siblings:
            section_label = ", ".join([disp[-1]] + siblings)
            last = f"{disp[-1]} (+{len(siblings)} more)"
        else:
            section_label = " > ".join(disp)
            # an unnumbered sub-heading ("Use Cases") needs its parent to mean anything
            last = disp[-1] if len(disp) < 2 or re.match(r"\d", disp[-1]) else f"{disp[-2]} > {disp[-1]}"
        for wi, win in enumerate(_windows(sec)):
            body = "\n\n".join(b.text for b in win)
            pages = sorted({b.page for b in win if b.page})
            lines = [b.line_start for b in win if b.line_start] + [b.line_end for b in win if b.line_end]
            loc = []
            if pages:
                loc.append(f"p.{pages[0]}" if len(pages) == 1 else f"pp.{pages[0]}-{pages[-1]}")
            elif lines:
                loc.append(f"L{min(lines)}-L{max(lines)}")
            if sec.numbers:
                loc.append(f"§{sec.numbers[-1]}")
            part = f" (part {wi + 1})" if wi else ""
            chunks.append(
                Chunk(
                    text=f"{doc_title}\nSection: {section_label}{part}\n\n{body}",
                    body=body,
                    source_id=source.id,
                    source_kind=source.kind,
                    file_path=rel,
                    title=f"{doc_title} · {last}{part}",
                    locator=" ".join(loc) or "whole document",
                    meta={
                        **meta,
                        "section": section_label,
                        "page_start": pages[0] if pages else None,
                        "page_end": pages[-1] if pages else None,
                        "line_start": min(lines) if lines and not pages else None,
                        "line_end": max(lines) if lines and not pages else None,
                        "url": url_for(min(lines), max(lines)) if url_for and lines and not pages else meta.get("url"),
                    },
                )
            )
    return chunks


def outline_chunk(chunks: list[Chunk], *, source: Source, rel: str, doc_title: str, meta: dict) -> list[Chunk]:
    """One table-of-contents chunk per long document.

    Corpus-level questions ("which PRD features have no test cases?", "what
    does the SRS cover?") need the whole document's shape, but top-k only
    ever returns a few sections. The outline lists every section with a
    one-line gist, so the answer can enumerate features it never retrieved.
    """
    sections = [c for c in chunks if c.meta.get("section")]
    if len(sections) < 4:
        return []
    lines = [f"Outline of {doc_title} ({meta.get('doc_type', 'Doc')}): every section with its opening words."]
    for c in sections:
        gist = re.sub(r"^#{1,6} .*\n+", "", (c.body or c.text).strip(), count=1)  # the section's own heading
        gist = re.sub(r"#{1,6}\s+", "", gist)  # merged sub-headings
        gist = re.sub(r"\|?(?:-{3,}\|)+-*", " ", gist)  # table separator rows
        gist = re.sub(r"\s*\|\s*", " | ", gist)
        words = re.sub(r"\s+", " ", gist).strip(" |").split()
        lines.append(f"- {c.meta['section']} ({c.locator}): {' '.join(words[:18])}{'…' if len(words) > 18 else ''}")
    return [
        Chunk(
            text="\n".join(lines),
            source_id=source.id,
            source_kind=source.kind,
            file_path=rel,
            title=f"{doc_title} · outline ({len(sections)} sections)",
            locator="outline",
            meta={**meta, "summary": "outline"},
        )
    ]


def pdf_lines(path: Path) -> list[tuple[str, int | None, int]]:
    from pypdf import PdfReader

    reader = PdfReader(str(path))
    out: list[tuple[str, int | None, int]] = []
    for pno, page in enumerate(reader.pages, start=1):
        try:
            raw = page.extract_text(extraction_mode="layout") or ""
        except Exception:  # some PDFs break layout mode; plain mode is the fallback
            raw = page.extract_text() or ""
        raw = normalize(raw)
        if raw and sum(1 for ln in raw.split("\n") if len(ln.split()) == 1) > 0.6 * max(1, len(raw.split("\n"))):
            raw = rejoin_word_per_line(raw)
        for lno, line in enumerate(raw.split("\n"), start=1):
            out.append((line, pno, lno))
        out.append(("", pno, 0))  # page break acts as a blank line
    return out


def chunk_docs(path: Path, source: Source, rel: str) -> list[Chunk]:
    suffix = path.suffix.lower()
    title = clean_title(path.stem)
    meta = {"doc_title": title, "doc_type": doc_type_of(path.name)}
    if suffix == ".pdf":
        lines = pdf_lines(path)
        blocks = _lines_to_blocks(lines)
        # the first unnumbered heading on page 1 is the document's own title
        if blocks and blocks[0].kind == "heading" and not blocks[0].number:
            title = blocks[0].text
            meta["doc_title"] = title
            blocks = blocks[1:]
    elif suffix in {".md", ".markdown", ".mdc"}:
        blocks = _markdown_to_blocks(normalize(path.read_text(encoding="utf-8", errors="replace")))
    else:
        text = normalize(path.read_text(encoding="utf-8", errors="replace"))
        blocks = _lines_to_blocks([(ln, None, i) for i, ln in enumerate(text.split("\n"), start=1)])
    chunks = blocks_to_chunks(blocks, source=source, rel=rel, doc_title=title, meta=meta)
    return chunks + outline_chunk(chunks, source=source, rel=rel, doc_title=title, meta=meta)


def chunk_markdown_text(text: str, *, source: Source, rel: str, doc_title: str, meta: dict, url_for=None) -> list[Chunk]:
    return blocks_to_chunks(_markdown_to_blocks(normalize(text)), source=source, rel=rel, doc_title=doc_title, meta=meta, url_for=url_for)
