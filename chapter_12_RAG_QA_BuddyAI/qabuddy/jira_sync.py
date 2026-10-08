"""JIRA -> data/01_JIRA_Tickets, via the REST API and a JQL query.

Why REST and not MCP for this step: MCP is the protocol an LLM client
(Copilot, Claude) uses to call tools interactively. A scheduled ingestion job
has no LLM in the loop; it needs every ticket matching a JQL, reliably,
every hour. That is exactly what the Jira MCP server itself calls under the
hood: GET /rest/api/3/search/jql. So the sync talks to it directly, writes
one Markdown file per ticket, and the normal ingest picks them up.

Configure in .env: JIRA_BASE_URL, JIRA_EMAIL, JIRA_API_TOKEN, JIRA_JQL.
"""

from __future__ import annotations

import re

import httpx
import yaml

from .config import settings, source_by_id

FIELDS = "summary,description,status,priority,issuetype,labels,components,created,updated,reporter,assignee,comment,project"


def adf_to_text(node, depth: int = 0) -> str:
    """Atlassian Document Format (Jira Cloud rich text) -> Markdown-ish text."""
    if node is None:
        return ""
    if isinstance(node, str):
        return node
    if isinstance(node, list):
        return "".join(adf_to_text(n, depth) for n in node)
    t = node.get("type")
    kids = node.get("content", [])
    if t == "text":
        return node.get("text", "")
    if t == "hardBreak":
        return "\n"
    if t in {"mention", "emoji"}:
        return node.get("attrs", {}).get("text", "")
    if t == "inlineCard":
        return node.get("attrs", {}).get("url", "")
    if t == "heading":
        return "#" * node.get("attrs", {}).get("level", 2) + " " + adf_to_text(kids, depth) + "\n\n"
    if t == "paragraph":
        return adf_to_text(kids, depth) + "\n\n"
    if t == "codeBlock":
        lang = node.get("attrs", {}).get("language", "") or ""
        return f"```{lang}\n{adf_to_text(kids, depth)}\n```\n\n"
    if t in {"bulletList", "orderedList"}:
        out = []
        for i, item in enumerate(kids, start=1):
            marker = f"{i}." if t == "orderedList" else "-"
            body = adf_to_text(item.get("content", []), depth + 1).strip().replace("\n\n", "\n")
            out.append("  " * depth + f"{marker} {body}")
        return "\n".join(out) + "\n\n"
    if t == "table":
        rows = []
        for row in kids:
            cells = [adf_to_text(c.get("content", []), depth).strip().replace("\n", " ") for c in row.get("content", [])]
            rows.append("| " + " | ".join(cells) + " |")
        if rows:
            rows.insert(1, "|" + "---|" * rows[0].count(" | ") + "---|")
        return "\n".join(rows) + "\n\n"
    return adf_to_text(kids, depth)


def _name(x) -> str:
    return (x or {}).get("displayName") or (x or {}).get("name") or ""


def ticket_markdown(issue: dict, base_url: str) -> str:
    f = issue.get("fields", {})
    meta = {
        "key": issue["key"],
        "summary": f.get("summary", ""),
        "issue_type": _name(f.get("issuetype")),
        "status": _name(f.get("status")),
        "priority": _name(f.get("priority")),
        "project": _name(f.get("project")),
        "reporter": _name(f.get("reporter")),
        "assignee": _name(f.get("assignee")) or "Unassigned",
        "labels": ", ".join(f.get("labels") or []),
        "components": ", ".join(_name(c) for c in f.get("components") or []),
        "created": (f.get("created") or "")[:10],
        "updated": (f.get("updated") or "")[:10],
        "url": f"{base_url}/browse/{issue['key']}",
    }
    desc = adf_to_text(f.get("description")).strip()
    parts = ["---", yaml.safe_dump(meta, sort_keys=False, allow_unicode=True).strip(), "---", "", "## Description", "", desc or "(no description)"]
    comments = ((f.get("comment") or {}).get("comments")) or []
    if comments:
        parts += ["", "## Comments", ""]
        for c in comments:
            parts += [f"### {_name(c.get('author'))} · {(c.get('created') or '')[:10]}", adf_to_text(c.get("body")).strip(), ""]
    return "\n".join(parts) + "\n"


def sync(jql: str | None = None, max_issues: int = 1000) -> dict:
    s = settings()
    if not s.jira_configured:
        raise RuntimeError("Jira is not configured. Set JIRA_BASE_URL, JIRA_EMAIL and JIRA_API_TOKEN in .env.")
    jql = jql or s.jira_jql
    src = source_by_id("jira")
    out_dir = src.path
    out_dir.mkdir(parents=True, exist_ok=True)
    written, token = [], None
    with httpx.Client(auth=(s.jira_email, s.jira_api_token), timeout=30, headers={"Accept": "application/json"}) as http:
        while len(written) < max_issues:
            params = {"jql": jql, "fields": FIELDS, "maxResults": 100}
            if token:
                params["nextPageToken"] = token
            r = http.get(f"{s.jira_base_url}/rest/api/3/search/jql", params=params)
            if r.status_code == 401:
                raise RuntimeError("Jira rejected the credentials (401). Check JIRA_EMAIL and JIRA_API_TOKEN.")
            r.raise_for_status()
            data = r.json()
            for issue in data.get("issues", []):
                safe = re.sub(r"[^A-Z0-9-]", "_", issue["key"])
                (out_dir / f"{safe}.md").write_text(ticket_markdown(issue, s.jira_base_url), encoding="utf-8")
                written.append(issue["key"])
            token = data.get("nextPageToken")
            if data.get("isLast", True) or not token:
                break
    return {"jql": jql, "written": len(written), "keys": written[:50]}
