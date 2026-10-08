"""Jenkins console logs and JUnit/TestNG XML results.

Raw logs are never embedded whole: 95% of a console log is noise, and two
failed builds differ only in timestamps, build numbers and IPs. Instead:

1. strip ANSI codes, timestamp prefixes and Jenkins pipeline chatter
2. one *summary* chunk per build: job, build #, result, stages, commit,
   test counts, failed and flaky tests (this answers "what failed in #142?")
3. one chunk per *failure window*: the error line plus its stack trace and a
   few lines of context, tagged with the pipeline stage it happened in
4. Drain-style templating (numbers, hex, IPs, durations -> <*>) so the same
   failure repeated 40 times becomes one chunk that says "seen 40x"

Test names, error templates and the build number go into the payload, so
"has testLoginPositiveVWO failed before?" is a filterable question.
"""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from pathlib import Path

from ..config import Source
from ..models import Chunk
from ..text import normalize, strip_ansi

_TS = re.compile(
    r"^\s*\[?(?:\d{4}-\d{2}-\d{2}[T ])?\d{2}:\d{2}:\d{2}(?:[.,]\d+)?(?:Z|[+-]\d{2}:?\d{2})?\]?\s+"
)
_PIPE_NOISE = re.compile(r"^\[Pipeline\]\s*(?:\{|\}|//.*|stage|node|sh|echo|withEnv|dir|script|checkout|Start of Pipeline|End of Pipeline)?\s*$")
_STAGE = re.compile(r"^\[Pipeline\] \{ \((?P<stage>.+)\)\s*$")
_RESULT = re.compile(r"^Finished:\s*(?P<result>SUCCESS|FAILURE|UNSTABLE|ABORTED|NOT_BUILT)")
_WORKSPACE = re.compile(r"workspace[/\\](?P<job>[\w.-]+)")
_SHA = re.compile(r"Checking out Revision (?P<sha>[0-9a-f]{7,40})")
_COMMIT = re.compile(r'Commit message:\s*"(?P<msg>.*)"')
_STARTED = re.compile(r"^Started by (?P<by>.+)$")
# `\w*Exception\b` (not `\bException`): there is no word boundary inside
# "TimeoutException", and `Error:` sits outside `\b...\b` because a word
# boundary never follows a colon.
_ERROR = re.compile(
    r"\b(?:ERROR|FATAL|FAILED|FAILURE|Caused by)\b|\w*Exception\b|\w*Error\b(?![s])|\bError:|timed out"
    r"|<<< FAILURE!|^\s*[✘×]\s|BUILD FAILURE|Tests run:.*Failures: [1-9]|\b\d+ failed\b"
)
_STACK = re.compile(r"^\s+at\s|^\s*\.\.\. \d+ more|^Caused by:|^\s{4,}\S|^\s*>?\s*\d+\s*\||^\s*\|\s*\^")
_PASS_SUMMARY = re.compile(r"Tests run:\s*\d+,\s*Failures:\s*0,\s*Errors:\s*0")
_TEST_FAILED = [
    re.compile(r"^FAILED:\s+(?:[\w.]+\.)?(?P<cls>\w+)\.(?P<name>\w+)\s*$"),
    re.compile(r"\[ERROR\]\s+(?P<cls>\w+)\.(?P<name>\w+)(?::\d+)?\s+»"),
    re.compile(r"^\s*[✘×]\s+\d+\s+\[\w+\]\s+›\s+(?P<file>[\w./-]+):\d+:\d+\s+›\s+(?:.+?\s+›\s+)?(?P<name>[^(›]+?)\s*(?:\(retry #\d+\))?\s*\(\d"),
]
_TEST_SKIPPED_RETRY = re.compile(r"^SKIPPED:\s+(?:[\w.]+\.)?(?P<cls>\w+)\.(?P<name>\w+)\s*$")
_PW_RETRY_PASS = re.compile(r"^\s*✓\s+\d+\s+\[\w+\]\s+›\s+(?P<file>[\w./-]+):\d+:\d+\s+›\s+(?:.+?\s+›\s+)?(?P<name>[^(›]+?)\s*\(retry #\d+\)")
_COUNTS = [
    re.compile(r"Tests run:\s*(?P<run>\d+),\s*Failures:\s*(?P<failed>\d+)(?:,\s*Errors:\s*(?P<errors>\d+))?,\s*Skip(?:ped|s):\s*(?P<skipped>\d+)"),
    re.compile(r"^\s*(?P<failed>\d+) failed\s*$"),
    re.compile(r"^\s*(?P<flaky>\d+) flaky\s*$"),
    re.compile(r"^\s*(?P<passed>\d+) passed"),
]
_TEMPLATE_SUBS = [
    (re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I), "<UUID>"),
    (re.compile(r"\b\d{1,3}(?:\.\d{1,3}){3}(?::\d+)?\b"), "<IP>"),
    (re.compile(r"\b0x[0-9a-f]+\b|\b[0-9a-f]{12,40}\b", re.I), "<HEX>"),
    (re.compile(r"\b\d+(?:\.\d+)?\s?(?:ms|s|sec|seconds?|m|min)\b"), "<DUR>"),
    (re.compile(r"\b\d+\b"), "<N>"),
]
MAX_WINDOW_LINES = 40


def template(line: str) -> str:
    t = line.strip()
    for rx, rep in _TEMPLATE_SUBS:
        t = rx.sub(rep, t)
    return t[:200]


def _build_number(path: Path, text: str) -> str:
    m = re.search(r"(?:build|#)[\s_-]*(\d{1,6})", text[:4000], re.I) or re.search(r"[_#-](\d{1,6})(?:\D*)$", path.stem)
    return m.group(1) if m else ""


def _console(path: Path, source: Source, rel: str) -> list[Chunk]:
    raw = strip_ansi(path.read_text(encoding="utf-8", errors="replace")).replace("\r\n", "\n")
    lines: list[tuple[int, str, str]] = []  # (original line no, text, stage)
    stage = ""
    job = result = sha = commit = started = ""
    for lno, line in enumerate(raw.split("\n"), start=1):
        line = _TS.sub("", line, count=1).rstrip()
        sm = _STAGE.match(line)
        if sm:
            stage = sm.group("stage")
            continue
        if not line.strip() or _PIPE_NOISE.match(line):
            continue
        if not job and (m := _WORKSPACE.search(line)):
            job = m.group("job")
        if not sha and (m := _SHA.search(line)):
            sha = m.group("sha")
        if not commit and (m := _COMMIT.search(line)):
            commit = m.group("msg")
        if not started and (m := _STARTED.match(line)):
            started = m.group("by")
        if m := _RESULT.match(line):
            result = m.group("result")
        lines.append((lno, line, stage))

    job = job or re.sub(r"[_#-]?\d+$", "", path.stem)
    build = re.search(r"[_#-](\d{1,6})$", path.stem)
    build_no = build.group(1) if build else _build_number(path, raw)
    stages = list(dict.fromkeys(s for _, _, s in lines if s))

    failed: list[str] = []
    retried: list[str] = []
    counts: dict[str, str] = {}
    def test_key(m: re.Match) -> str:
        g = m.groupdict()
        # Java: Class.method   Playwright: file › title (one key for a failure and its retry)
        return f"{g['cls']}.{g['name'].strip()}" if g.get("cls") else f"{g['file']} › {g['name'].strip()}"

    for _, line, _s in lines:
        for rx in _TEST_FAILED:
            if m := rx.search(line):
                name = test_key(m)
                if name not in failed:
                    failed.append(name)
        if m := _TEST_SKIPPED_RETRY.match(line):
            retried.append(test_key(m))
        if m := _PW_RETRY_PASS.match(line):
            retried.append(test_key(m))
        for rx in _COUNTS:
            if m := rx.search(line):
                for k, v in m.groupdict().items():
                    if v is not None:
                        counts[k] = v
    # a test that failed, was retried and then passed is flaky, not failed
    flaky = list(dict.fromkeys(t for t in retried))
    passed_after_retry = {t for t in flaky}
    hard_failed = [t for t in failed if t not in passed_after_retry]
    if result == "SUCCESS":
        hard_failed = []
    failed_stage = next((s for _, l, s in lines if _ERROR.search(l) and not _PASS_SUMMARY.search(l) and s), "")

    title_base = f"{job} #{build_no}" if build_no else job
    head = f"Jenkins build {title_base}: {result or 'UNKNOWN'}"
    summary = [head]
    if started:
        summary.append(f"Started by: {started}")
    if stages:
        summary.append("Stages: " + " -> ".join(stages))
    if failed_stage and result not in {"SUCCESS", ""}:
        summary.append(f"Failed in stage: {failed_stage}")
    if sha:
        summary.append(f"Commit: {sha[:12]}" + (f' "{commit}"' if commit else ""))
    if counts:
        summary.append("Test counts: " + ", ".join(f"{k} {v}" for k, v in counts.items()))
    if hard_failed:
        summary.append("Failed tests:\n" + "\n".join(f"- {t}" for t in hard_failed))
    if flaky:
        summary.append("Flaky (failed, then passed on retry):\n" + "\n".join(f"- {t}" for t in flaky))

    meta = {
        "job": job,
        "build": build_no,
        "result": result,
        "stages": stages,
        "failed_tests": hard_failed,
        "flaky_tests": flaky,
        "commit": sha[:12],
    }
    chunks = [
        Chunk(
            text="\n".join(summary),
            source_id=source.id,
            source_kind=source.kind,
            file_path=rel,
            title=f"{title_base} · build summary ({result or 'unknown'})",
            locator=f"#{build_no} summary" if build_no else "summary",
            meta={**meta, "log_part": "summary"},
        )
    ]

    # failure windows
    idx = [i for i, (_, l, _s) in enumerate(lines) if _ERROR.search(l) and not _PASS_SUMMARY.search(l)]
    windows: list[tuple[int, int]] = []
    for i in idx:
        start, end = max(0, i - 3), i + 1
        while end < len(lines) and end - start < MAX_WINDOW_LINES and (_STACK.match(lines[end][1]) or _ERROR.search(lines[end][1])):
            end += 1
        end = min(len(lines), end + 2)
        if windows and start <= windows[-1][1]:
            windows[-1] = (windows[-1][0], max(windows[-1][1], end))
        else:
            windows.append((start, end))

    seen: dict[str, int] = {}
    for start, end in windows:
        block = lines[start:end]
        first_err = next((l for _, l, _s in block if _ERROR.search(l)), block[0][1])
        sig = template(first_err)
        if sig in seen:
            chunks[seen[sig]].meta["repeat_count"] = chunks[seen[sig]].meta.get("repeat_count", 1) + 1
            continue
        body = "\n".join(l for _, l, _s in block)
        if len(block) >= MAX_WINDOW_LINES:
            body += "\n…"
        stage_here = next((s for _, _, s in block if s), "")
        a, b = block[0][0], block[-1][0]
        tests_here = list(dict.fromkeys(t for t in failed + flaky if t.split("›")[-1].split(".")[-1].strip() in body))
        seen[sig] = len(chunks)
        chunks.append(
            Chunk(
                text=f"{head}\nStage: {stage_here or 'n/a'} | log lines {a}-{b}\n\n{body}",
                body=body,
                source_id=source.id,
                source_kind=source.kind,
                file_path=rel,
                title=f"{title_base} · {stage_here or 'log'} failure at L{a}",
                locator=f"#{build_no} L{a}-L{b}" if build_no else f"L{a}-L{b}",
                meta={
                    **meta,
                    "log_part": "failure",
                    "stage": stage_here,
                    "error_template": sig,
                    "tests_in_window": tests_here,
                    "line_start": a,
                    "line_end": b,
                },
            )
        )
    for c in chunks[1:]:
        if c.meta.get("repeat_count", 1) > 1:
            c.text = c.text.replace("\n\n", f"\nSeen {c.meta['repeat_count']}x in this log\n\n", 1)
    return chunks


def _junit(path: Path, source: Source, rel: str) -> list[Chunk]:
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError:
        return []
    suites = [root] if root.tag == "testsuite" else root.findall(".//testsuite")
    props = {p.get("name"): p.get("value") for p in root.iter("property")}
    build_label = props.get("jenkins.build", "")
    chunks: list[Chunk] = []
    for suite in suites:
        name = suite.get("name", path.stem)
        cases = suite.findall("testcase")
        failures, flaky = [], []
        for tc in cases:
            cls = (tc.get("classname") or "").split(".")[-1]
            test = f"{cls}.{tc.get('name')}"
            bad = tc.find("failure") if tc.find("failure") is not None else tc.find("error")
            if tc.find("flakyFailure") is not None or tc.find("rerunFailure") is not None:
                flaky.append(test)
            if bad is not None:
                failures.append((test, tc, bad))
        head = f"Test results {name}" + (f" ({build_label})" if build_label else "") + f" from {path.name}"
        counts = ", ".join(f"{k} {suite.get(k)}" for k in ("tests", "failures", "errors", "skipped", "time") if suite.get(k))
        summary = [head, f"Counts: {counts}"]
        if failures:
            summary.append("Failed tests:\n" + "\n".join(f"- {t}" for t, _, _ in failures))
        if flaky:
            summary.append("Flaky:\n" + "\n".join(f"- {t}" for t in flaky))
        meta = {"suite": name, "build": build_label, "failed_tests": [t for t, _, _ in failures], "flaky_tests": flaky}
        chunks.append(
            Chunk(
                text="\n".join(summary),
                source_id=source.id,
                source_kind=source.kind,
                file_path=rel,
                title=f"{name} results summary",
                locator="summary",
                meta={**meta, "log_part": "summary"},
            )
        )
        for test, tc, bad in failures:
            stack = normalize(bad.text or "")
            stack_lines = stack.split("\n")
            if len(stack_lines) > 15:
                stack = "\n".join(stack_lines[:15]) + "\n…"
            body = f"Test failed: {test}\nType: {bad.get('type', '')}\nMessage: {bad.get('message', '')}\nTime: {tc.get('time', '?')} s\n{stack}"
            chunks.append(
                Chunk(
                    text=f"{head}\n\n{body}",
                    body=body,
                    source_id=source.id,
                    source_kind=source.kind,
                    file_path=rel,
                    title=f"{test} failed",
                    locator=test,
                    meta={**meta, "log_part": "failure", "test_name": test, "error_template": template(bad.get("message", ""))},
                )
            )
    return chunks


def chunk_logs(path: Path, source: Source, rel: str) -> list[Chunk]:
    if path.suffix.lower() == ".xml":
        return _junit(path, source, rel)
    return _console(path, source, rel)
