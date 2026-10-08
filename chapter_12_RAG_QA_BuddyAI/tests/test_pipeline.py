"""Regression tests for the ingestion and grounding logic.

Each test pins a real bug found while building QABuddy, so it cannot quietly
come back. No Qdrant, Ollama or LLM needed: run with `pytest -q`.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest

from qabuddy.answer import citations, normalize_citations
from qabuddy.chunkers.code import chunk_code, redact
from qabuddy.chunkers.docs import _lines_to_blocks, chunk_markdown_text
from qabuddy.chunkers.jira import chunk_jira, parse_ticket
from qabuddy.chunkers.logs import chunk_logs
from qabuddy.chunkers.testcases import chunk_testcases
from qabuddy.chunkers.transcript import chunk_transcript
from qabuddy.config import ROOT, Source
from qabuddy.jira_sync import adf_to_text
from qabuddy.sparse import stem, terms


def src(kind: str, path: Path | None = None, sid: str = "t") -> Source:
    return Source(id=sid, label="Test source", path=path or ROOT, kind=kind)


# ------------------------------------------------------------- tokenizer


def test_terms_split_identifiers_and_keep_ids_whole():
    t = terms("loginToVWOLoginValidCreds failed on VWO-26 in e2e-checkout.spec.ts")
    assert "logintovwologinvalidcreds" in t  # whole identifier
    assert {"login", "vwo", "valid", "cred"} <= set(t)  # camelCase parts, stemmed
    assert "vwo-26" in t and "26" in t  # ticket id whole and split
    assert "e2e-checkout.spec.ts" in t


def test_light_stemmer():
    assert [stem(w) for w in ["failures", "failed", "failing", "tests", "boxes", "status", "running"]] == [
        "failure", "fail", "fail", "test", "box", "status", "run",
    ]


@pytest.mark.skipif(shutil.which("node") is None, reason="node not installed")
def test_python_and_browser_tokenizers_agree():
    """The hosted demo runs BM25 in the browser; it must tokenize like the server."""
    samples = [
        "Why did vwo-selenium-regression #142 fail with TimeoutException at WaitHelpers.java:76?",
        "Is testLoginPositiveVWO flaky? QAB-102, RetryAnalyzer maxRetryCount =3",
        "FR4 Heatmaps & Session Recordings | Must | Capture user interactions for insights.",
    ]
    script = (
        "import('./ui/src/bm25.js').then(m => console.log(JSON.stringify("
        + json.dumps(samples)
        + ".map(s => m.terms(s)))))"
    )
    out = subprocess.run(["node", "--input-type=module", "-e", script], cwd=ROOT, capture_output=True, text=True, timeout=30)
    assert out.returncode == 0, out.stderr
    assert json.loads(out.stdout) == [terms(s) for s in samples]


# ------------------------------------------------------------- citations


def test_citations_count_word_attached_and_adjacent_markers():
    c = citations("Marked failed[1]. Retry limit is 3 [2][3]. Code `args[0]` and ```java\nx[4]\n``` stay code. Bad [9].", 4)
    assert c["used"] == [1, 2, 3]
    assert c["invalid"] == [9]
    assert c["grounded"]


def test_gpt_oss_browsing_citations_are_normalized():
    assert normalize_citations("blocked by IP【3†L51-L82】 and【5†L00:52-L01:20】") == "blocked by IP[3] and[5]"
    assert citations("See【2†L1-L4】", 3)["used"] == [2]


def test_refusal_counts_as_grounded():
    c = citations("I couldn't find this in the knowledge base.", 3)
    assert c["grounded"] and c["said_not_found"]


# ------------------------------------------------------------- test cases


def test_testcases_bom_duplicate_and_empty_columns(tmp_path):
    p = tmp_path / "tc.csv"
    p.write_text(
        "﻿Scenario TID,TestCase Description,TestSteps,Steps to Execute,Actual Result,Priority\n"
        "LOGIN-001,Verify Login - page load,1. Open | 2. Check,1. Open | 2. Check,,High\n"
        "SUPPORT-002,Verify Support - block other-user ticket access,1. Open,1. Open,,Critical\n",
        encoding="utf-8",
    )
    chunks = chunk_testcases(p, src("testcases", tmp_path), "tc.csv")
    rows = [c for c in chunks if not c.meta.get("summary")]
    assert [c.meta["tc_id"] for c in rows] == ["LOGIN-001", "SUPPORT-002"]  # BOM did not break the id column
    assert rows[0].meta["module"] == "Login" and rows[1].meta["module"] == "Support"
    assert "Steps to Execute" not in rows[0].text  # duplicate column dropped
    assert rows[0].text.count("1. Open") == 1
    assert any("Actual Result (always empty)" in d for d in rows[0].meta["dropped_columns"])
    summary = next(c for c in chunks if c.meta.get("summary") == "repository")
    assert "2 test cases across 2 modules" in summary.text


# ------------------------------------------------------------------ jira


PRINTABLE = (
    "Back to previous view\n[VWO-33] Login failure despite correct credentials Created: 04/Apr/26  Updated: 04/Apr/26\n"
    "Status:\tTo Do\nType:\tBug\tPriority:\tMedium\nReporter:\tPramod\tAssignee:\tUnassigned\n\n"
    " Description \t \nLogin fails with valid credentials.\n\nComments\nComment by Rahul [ 07/Apr/26 ]\nIP allowlist issue.\n\n"
    "Generated at Sun May 10 04:47:53 UTC 2026 by Pramod using Jira.\n"
)


def test_jira_key_comes_from_content_not_filename(tmp_path):
    p = tmp_path / "Bug_VWO_32.md"  # the real export is misnamed: it contains VWO-33
    p.write_text(PRINTABLE)
    chunks = chunk_jira(p, src("jira", tmp_path), "Bug_VWO_32.md")
    assert chunks[0].meta["jira_key"] == "VWO-33"
    assert chunks[0].meta["issue_type"] == "Bug" and chunks[0].meta["priority"] == "Medium"
    assert "Generated at" not in chunks[0].text  # export footer stripped
    assert chunks[1].locator == "VWO-33 comment 1" and "IP allowlist" in chunks[1].text


def test_jira_front_matter_format_from_sync():
    t = parse_ticket("---\nkey: QAB-1\nsummary: Cart shows 2 rows\nstatus: To Do\n---\n\n## Description\n\nBody text\n\n## Comments\n\n### Ana · 2026-04-10\nUse a worker user\n")
    assert t["key"] == "QAB-1" and t["description"] == "Body text"
    assert t["comments"][0]["author"] == "Ana"


def test_adf_to_text():
    adf = {"type": "doc", "content": [
        {"type": "paragraph", "content": [{"type": "text", "text": "Steps:"}]},
        {"type": "orderedList", "content": [
            {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Open login"}]}]},
            {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Submit"}]}]},
        ]},
    ]}
    out = adf_to_text(adf)
    assert "1. Open login" in out and "2. Submit" in out


# ------------------------------------------------------------------ docs


def test_numbered_heading_is_not_swallowed_by_the_list_before_it():
    lines = ["Stakeholders", "", "    ●   Product Managers", "    ●   Analysts", "", "", "", "4. Core Features & Capabilities", "",
             "4.1. Experimentation & Testing", "", "VWO Testing enables experiments.", ""]
    blocks = _lines_to_blocks([(l, 1, i) for i, l in enumerate(lines, 1)])
    heads = [(b.number, b.text) for b in blocks if b.kind == "heading"]
    assert ("4", "Core Features & Capabilities") in heads
    assert ("4.1", "Experimentation & Testing") in heads


def test_layout_table_rows_are_rebuilt_not_read_as_headings():
    lines = [
        "  ID                 Feature                  Priorit                     Description",
        "                                                 y",
        "",
        " FR     Heatmaps & Session                    Must       Capture user interactions for insights.",
        " 4      Recordings",
        "",
        " FR     Collaboration & Workflow              Mediu      Tools for planning and team tasks.",
        " 9      Management                            m",
        "",
        "",
    ]
    blocks = _lines_to_blocks([(l, 4, i) for i, l in enumerate(lines, 1)])
    assert not [b for b in blocks if b.kind == "heading"]  # " 4      Recordings" is a cell, not a heading
    table = next(b for b in blocks if b.kind == "table").text
    assert "| ID | Feature | Priority | Description |" in table
    assert "| FR4 | Heatmaps & Session Recordings | Must |" in table
    assert "| FR9 | Collaboration & Workflow Management | Medium |" in table


def test_markdown_sections_keep_siblings_apart_and_drop_h1_from_titles():
    md = ("# Coding Standards\n\nIntro.\n\n## 1. Selenium\n\n### 1.1 Waits\n\nUse WaitHelpers.\n\n### 1.2 Locators\n\nUse By.id.\n\n"
          "## 2. Playwright\n\n### 2.1 Structure\n\nPages extend BasePage.\n")
    chunks = chunk_markdown_text(md, source=src("docs"), rel="x.md", doc_title="Coding Standards", meta={})
    sel = [c for c in chunks if "WaitHelpers" in c.text][0]
    assert "BasePage" not in sel.text  # Selenium and Playwright never share a chunk
    assert "Coding Standards · Coding Standards" not in sel.title


# ------------------------------------------------------------------ logs


def test_testng_retry_is_detected_as_flaky(tmp_path):
    p = tmp_path / "vwo-selenium-regression_143.log"
    p.write_text(
        "Building in workspace /var/lib/jenkins/workspace/vwo-selenium-regression\n[Pipeline] { (Selenium Regression)\n"
        "SKIPPED: com.x.TestVWOLogin_05.testLoginPositiveVWO\n"
        "org.openqa.selenium.TimeoutException: waiting for visibility of //h6\n"
        "\tat com.x.WaitHelpers.visibilityOfElement(WaitHelpers.java:76)\n"
        "PASSED: com.x.TestVWOLogin_05.testLoginPositiveVWO\n"
        "[WARNING] Tests run: 3, Failures: 0, Errors: 0, Skipped: 1\n[Pipeline] }\nFinished: SUCCESS\n"
    )
    chunks = chunk_logs(p, src("logs", tmp_path), "b143.log")
    summary = chunks[0]
    assert summary.meta["result"] == "SUCCESS" and summary.meta["build"] == "143"
    assert summary.meta["flaky_tests"] == ["TestVWOLogin_05.testLoginPositiveVWO"]
    assert not summary.meta["failed_tests"]
    assert any("TimeoutException" in c.text for c in chunks[1:])  # \w*Exception, not \bException


def test_playwright_failure_vs_flaky(tmp_path):
    p = tmp_path / "playwright-e2e_88.log"
    p.write_text(
        "  ✘   3 [chromium] › tests/a.spec.ts:22:5 › suite › create a booking (5.0s)\n"
        "  ✓   4 [chromium] › tests/a.spec.ts:22:5 › suite › create a booking (retry #1) (1.9s)\n"
        "  ✘   9 [chromium] › tests/b.spec.ts:30:5 › suite › checkout (12.3s)\n"
        "    Error: expect(received).toBe(expected)\n  1 failed\n  1 flaky\n  14 passed (50.2s)\nFinished: UNSTABLE\n"
    )
    s = chunk_logs(p, src("logs", tmp_path), "pw.log")[0].meta
    assert s["failed_tests"] == ["tests/b.spec.ts › checkout"]
    assert s["flaky_tests"] == ["tests/a.spec.ts › create a booking"]


# ------------------------------------------------------------------ code


def test_redaction_hides_secrets_but_keeps_locators():
    props, n = redact("username=qa@x.com\npassword=Fake@Pass99\napi_key = abc123\n", ".properties")
    assert "Fake@Pass99" not in props and "abc123" not in props and "qa@x.com" in props and n == 2
    java, _ = redact('private By password = By.id("login-password");\nString token = "s3cr3t-value";', ".java")
    assert 'By.id("login-password")' in java and "s3cr3t-value" not in java


def test_java_ast_split_keeps_methods_whole(tmp_path):
    methods = "\n".join(
        f"    public void method{i}() {{\n" + "".join(f"        doSomething{i}_{j}(\"value\");\n" for j in range(14)) + "    }\n"
        for i in range(8)
    )
    p = tmp_path / "Big.java"
    p.write_text(f"package a;\n\nimport b.C;\n\npublic class Big {{\n{methods}}}\n")
    chunks = chunk_code(p, src("code", tmp_path, sid="selenium"), "Big.java")
    assert len(chunks) > 1
    for c in chunks:
        assert c.text.count("{") >= c.text.count("}") - 1  # no chunk starts mid-method
        assert "class Big" in c.meta["scope"] or "class Big" in c.meta["symbols"]


# ------------------------------------------------------------ transcripts


def test_vtt_speaker_turns(tmp_path):
    p = tmp_path / "2026-04-14_Standup.vtt"
    p.write_text("WEBVTT\n\n1\n00:00:01.000 --> 00:00:05.000\n<v Ananya>Build 143 is green.\n\n2\n00:00:05.100 --> 00:00:09.000\n<v Rahul>Health check in review.\n")
    chunks = chunk_transcript(p, src("transcript", tmp_path), "s.vtt")
    assert chunks[0].meta["meeting_date"] == "2026-04-14"
    assert "Ananya: Build 143 is green." in chunks[0].text and "Rahul:" in chunks[0].text
