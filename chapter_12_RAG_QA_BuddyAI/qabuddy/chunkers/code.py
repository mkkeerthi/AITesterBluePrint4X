"""Source code repositories: AST-aware chunks.

Splitting code every N lines cuts methods in half and glues the tail of one
to the head of the next. This chunker parses Java / TypeScript / JavaScript
with tree-sitter and applies cAST-style split-then-merge:

* a node that fits the budget (MAX_NWS non-whitespace chars) becomes a span
* a node that is too big is split into its children, recursively
* adjacent small spans are merged back up to the budget, so getters and
  imports do not become 30-character chunks

Every chunk gets a contextual header (repo, path, lines, enclosing scope,
symbols) and a GitHub permalink to the exact lines. Test-runner blocks
(`test.describe(...)`, `test('...')`) count as scopes, because in a spec
file they are the unit a QA engineer asks about.

Non-AST files: Markdown and AI rule files go through docs.py; configs
(pom.xml, testng.xml, .properties, .json, .yml) are kept whole when small
or split into overlapping line windows. Secrets are redacted on the way in.
"""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

from ..config import Source
from ..models import Chunk
from ..text import normalize
from .docs import chunk_markdown_text

MAX_NWS = 1500  # non-whitespace chars, roughly 450-550 tokens of real code
LINE_OVERLAP = 3

AST_EXT = {".java": "java", ".ts": "typescript", ".mts": "typescript", ".cts": "typescript",
           ".tsx": "tsx", ".jsx": "tsx", ".js": "typescript", ".mjs": "typescript", ".cjs": "typescript"}
DOC_EXT = {".md", ".mdc", ".markdown", ".rst"}
DOC_NAMES = {".cursorrules", ".windsurfrules", "readme", "readme.txt"}
CONFIG_EXT = {".xml", ".properties", ".yml", ".yaml", ".json", ".toml", ".ini", ".cfg", ".conf",
              ".feature", ".gradle", ".sh", ".example", ".txt", ".py", ".kt", ".groovy", ".cs", ".go", ".rb"}
EXCLUDE_DIRS = {".git", "node_modules", ".idea", ".vscode", "target", "build", "out", "dist", "bin",
                ".gradle", ".mvn", "test-results", "playwright-report", "blob-report", "allure-results",
                "allure-report", "coverage", "__pycache__", ".venv", "venv", ".next", ".cache",
                "screenshots", "logs", "reports"}
EXCLUDE_FILES = {"package-lock.json", "yarn.lock", "pnpm-lock.yaml", ".gitignore", ".DS_Store",
                 "license", "license.md", "license.txt"}
MAX_FILE_BYTES = 400_000

_SECRET_WORDS = r"(?:password|passwd|pwd|secret|token|api[_-]?key|apikey|access[_-]?key|private[_-]?key|client[_-]?secret)"
# config files: `db.password = hunter2`
_SECRET_KV = re.compile(rf"(?im)^(\s*[\w.-]*{_SECRET_WORDS}[\w.-]*\s*[=:]\s*)([^\s#].*)$")
# code: only string literals assigned to secret-named keys, never expressions,
# so `By password = By.id("login-password")` keeps its locator
_SECRET_LIT = re.compile(rf"(?i)({_SECRET_WORDS}\w*['\"]?\s*[:=]\s*)(['\"`])([^'\"`\n]{{3,}})\2")
_CONFIG_LIKE = {".properties", ".env", ".example", ".yml", ".yaml", ".ini", ".cfg", ".conf", ".toml"}


def redact(text: str, suffix: str) -> tuple[str, int]:
    n = 0
    if suffix in _CONFIG_LIKE:
        text, n = _SECRET_KV.subn(lambda m: m.group(1) + "<redacted>", text)
    text, k = _SECRET_LIT.subn(lambda m: f"{m.group(1)}{m.group(2)}<redacted>{m.group(2)}", text)
    return text, n + k


def wanted(path: Path, root: Path) -> bool:
    rel_parts = path.relative_to(root).parts
    if any(p in EXCLUDE_DIRS or (p.startswith(".") and p != ".github") for p in rel_parts[:-1]):
        return False
    name = path.name.lower()
    if name in EXCLUDE_FILES or path.stat().st_size > MAX_FILE_BYTES:
        return False
    if name in DOC_NAMES:
        return True
    if path.name.startswith("."):
        return False
    return path.suffix.lower() in AST_EXT or path.suffix.lower() in DOC_EXT or path.suffix.lower() in CONFIG_EXT


@lru_cache
def _parser(lang: str):
    from tree_sitter import Language, Parser

    if lang == "java":
        import tree_sitter_java as m

        language = Language(m.language())
    else:
        import tree_sitter_typescript as m

        language = Language(m.language_tsx() if lang == "tsx" else m.language_typescript())
    return Parser(language)


@lru_cache
def git_info(repo: str) -> tuple[str, str] | None:
    try:
        url = subprocess.run(["git", "-C", repo, "config", "--get", "remote.origin.url"], capture_output=True, text=True, timeout=5).stdout.strip()
        sha = subprocess.run(["git", "-C", repo, "rev-parse", "HEAD"], capture_output=True, text=True, timeout=5).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return None
    if url.startswith("git@github.com:"):
        url = "https://github.com/" + url.split(":", 1)[1]
    url = url.removesuffix(".git")
    return (url, sha) if url.startswith("https://github.com/") and sha else None


# ------------------------------------------------------------------- spans


@dataclass
class Span:
    start_byte: int
    end_byte: int
    start_row: int
    end_row: int
    scope: tuple[str, ...]
    symbols: list[str] = field(default_factory=list)
    nws: int = 0
    lines_only: bool = False  # produced by the line-window fallback: rows are valid, bytes are not


_SCOPE_TYPES = {
    "class_declaration": "class", "abstract_class_declaration": "class", "interface_declaration": "interface",
    "enum_declaration": "enum", "record_declaration": "record", "method_declaration": "method",
    "constructor_declaration": "constructor", "function_declaration": "function",
    "generator_function_declaration": "function", "method_definition": "method",
}
_TEST_CALLS = {"describe", "test.describe", "test.describe.serial", "test.describe.parallel", "test", "it",
               "test.step", "test.beforeEach", "test.afterEach", "test.beforeAll", "test.afterAll", "test.only",
               "beforeEach", "afterEach"}


def _nws(src: bytes, a: int, b: int) -> int:
    return len(re.sub(rb"\s+", b"", src[a:b]))


def _string_arg(node) -> str:
    args = node.child_by_field_name("arguments")
    if args is None:
        return ""
    for ch in args.named_children:
        if ch.type in {"string", "template_string"}:
            return ch.text.decode(errors="replace").strip("'\"`")
        break
    return ""


def _label(node) -> str | None:
    kind = _SCOPE_TYPES.get(node.type)
    if kind:
        name = node.child_by_field_name("name")
        if name is not None:
            n = name.text.decode(errors="replace")
            return f"{kind} {n}" if kind in {"class", "interface", "enum", "record"} else f"{n}()"
    if node.type == "call_expression":
        fn = node.child_by_field_name("function")
        fname = fn.text.decode(errors="replace") if fn is not None else ""
        if fname in _TEST_CALLS:
            title = _string_arg(node)
            word = "describe" if "describe" in fname else ("hook" if "each" in fname.lower() or "all" in fname.lower() else ("step" if fname.endswith("step") else "test"))
            return f'{word} "{title}"' if title else fname
    return None


def _symbols(node, limit: int = 12) -> list[str]:
    out: list[str] = []
    stack = [node]
    while stack and len(out) < limit:
        n = stack.pop()
        lab = _label(n)
        if lab and lab not in out:
            out.append(lab)
        stack.extend(reversed(n.children))
    return out


def _line_spans(src: bytes, a: int, b: int, row0: int, scope: tuple[str, ...]) -> list[Span]:
    text = src[a:b].decode(errors="replace")
    lines = text.split("\n")
    spans, cur, cur_nws, start = [], [], 0, 0
    for i, ln in enumerate(lines):
        n = len(re.sub(r"\s+", "", ln))
        if cur and cur_nws + n > MAX_NWS:
            spans.append(Span(0, 0, row0 + start, row0 + start + len(cur) - 1, scope, nws=cur_nws, lines_only=True))
            start = max(start + len(cur) - LINE_OVERLAP, start + 1)
            cur = lines[start: i]
            cur_nws = sum(len(re.sub(r"\s+", "", x)) for x in cur)
        cur.append(ln)
        cur_nws += n
    if cur:
        spans.append(Span(0, 0, row0 + start, row0 + start + len(cur) - 1, scope, nws=cur_nws, lines_only=True))
    return spans


def _split(node, src: bytes, scope: tuple[str, ...]) -> list[Span]:
    size = _nws(src, node.start_byte, node.end_byte)
    if size <= MAX_NWS:
        return [Span(node.start_byte, node.end_byte, node.start_point[0], node.end_point[0], scope, _symbols(node), size)]
    label = _label(node)
    inner = scope + (label,) if label else scope
    if not node.children:
        return _line_spans(src, node.start_byte, node.end_byte, node.start_point[0], inner)
    spans: list[Span] = []
    for ch in node.children:
        spans.extend(_split(ch, src, inner))
    return _merge(spans)


def _merge(spans: list[Span]) -> list[Span]:
    out: list[Span] = []
    for s in spans:
        prev = out[-1] if out else None
        if s.lines_only or prev is None or prev.lines_only:
            out.append(s)
            continue
        if prev.nws + s.nws <= MAX_NWS:
            dominant = prev if prev.nws >= s.nws else s
            out[-1] = Span(prev.start_byte, s.end_byte, prev.start_row, s.end_row, dominant.scope,
                           list(dict.fromkeys(prev.symbols + s.symbols)), prev.nws + s.nws)
        else:
            out.append(s)
    return out


_IMPORT_ONLY = re.compile(r"^\s*(?:(?:import|package|export \* from|export \{[^}]*\} from)\b[^\n]*\n?|\s*)+$")


def _ast_chunks(path: Path, text: str, lang: str) -> list[Span]:
    src = text.encode()
    tree = _parser(lang).parse(src)
    spans = _split(tree.root_node, src, ())
    return [s for s in spans if s.lines_only or not _IMPORT_ONLY.match(src[s.start_byte:s.end_byte].decode(errors="replace"))]


# ------------------------------------------------------------------ public


def chunk_code(path: Path, source: Source, rel: str) -> list[Chunk]:
    repo = source.path
    in_repo = path.relative_to(repo).as_posix()
    suffix = path.suffix.lower()
    gi = git_info(str(repo))

    def url(a: int, b: int, plain: bool = False) -> str | None:
        if not gi:
            return None
        base, sha = gi
        return f"{base}/blob/{sha}/{in_repo}{'?plain=1' if plain else ''}#L{a}-L{b}"

    raw = path.read_text(encoding="utf-8", errors="replace")

    # Markdown, README and AI rule files: prose, so section chunking
    if suffix in DOC_EXT or path.name.lower() in DOC_NAMES:
        chunks = chunk_markdown_text(
            raw,
            source=source,
            rel=rel,
            doc_title=f"{source.label}: {in_repo}",
            meta={"repo": source.label, "path_in_repo": in_repo, "language": "markdown", "code_kind": "doc"},
            url_for=lambda a, b: url(a, b, plain=True),
        )
        return chunks

    text, redactions = redact(raw.replace("\r\n", "\n"), suffix)
    lines = text.split("\n")
    lang = AST_EXT.get(suffix)
    if lang:
        try:
            spans = _ast_chunks(path, text, lang)
        except Exception:  # an unparseable file still gets indexed, by lines
            spans = _line_spans(text.encode(), 0, len(text.encode()), 0, ())
    else:
        spans = _line_spans(text.encode(), 0, len(text.encode()), 0, ())

    chunks: list[Chunk] = []
    for s in spans:
        a, b = s.start_row + 1, s.end_row + 1
        body = "\n".join(lines[a - 1: b]).strip("\n")
        if not body.strip():
            continue
        scope = " > ".join(s.scope)
        header = [f"{source.label}: {in_repo} (lines {a}-{b})", f"Language: {lang or suffix.lstrip('.') or 'text'}"]
        if scope:
            header.append(f"Scope: {scope}")
        if s.symbols:
            header.append("Defines: " + ", ".join(s.symbols[:8]))
        main = s.symbols[0] if s.symbols else (s.scope[-1] if s.scope else "")
        chunks.append(
            Chunk(
                text="\n".join(header) + "\n\n" + body,
                body=body,
                source_id=source.id,
                source_kind=source.kind,
                file_path=rel,
                title=f"{path.name} · {main}" if main else path.name,
                locator=f"L{a}-L{b}",
                meta={
                    "repo": source.label,
                    "path_in_repo": in_repo,
                    "language": lang or suffix.lstrip("."),
                    "code_kind": "code" if lang else "config",
                    "symbols": s.symbols[:12],
                    "scope": scope,
                    "line_start": a,
                    "line_end": b,
                    "url": url(a, b),
                    "redactions": redactions or None,
                },
            )
        )
    return chunks


def iter_repo_files(root: Path):
    for p in sorted(root.rglob("*")):
        if p.is_file() and wanted(p, root):
            yield p
