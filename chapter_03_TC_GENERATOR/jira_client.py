"""Jira REST API client for the Jira Test Case Generator.

Fetches ticket details (summary, description, acceptance criteria) using
the credentials persisted via config_store. The acceptance criteria field
varies between Jira projects, so we look it up across all custom fields.
"""

import re

import requests

TICKET_KEY_RE = re.compile(r"\b([A-Z][A-Z0-9]+-\d+)\b")


def extract_ticket_key(text: str) -> str | None:
    """Return the first Jira ticket key found in the text, or None."""
    match = TICKET_KEY_RE.search(text or "")
    return match.group(1) if match else None


def _acceptance_criteria(fields: dict) -> str:
    """Best-effort acceptance criteria lookup across Jira custom fields."""
    candidates = []
    for key, value in fields.items():
        if not isinstance(key, str) or not key.startswith("customfield_"):
            continue
        if isinstance(value, list):  # Atlassian checklists / multi-text fields
            parts = [item.get("text") or item.get("value") for item in value if isinstance(item, dict)]
            if parts:
                candidates.append("\n".join(str(p) for p in parts if p))
        elif isinstance(value, dict):  # Atlassian document format
            adf = value.get("content")
            if isinstance(adf, list):
                text = _adf_to_text(adf)
                if text:
                    candidates.append(text)
        elif isinstance(value, str) and value.strip():
            candidates.append(value.strip())
    return "\n\n".join(candidates)


def _adf_to_text(content: list) -> str:
    """Flatten an Atlassian Document Format node list to plain text."""
    parts = []
    for node in content:
        node_type = node.get("type")
        if node_type == "text":
            parts.append(node.get("text", ""))
        elif node_type == "hardBreak":
            parts.append("\n")
        else:
            child = node.get("content")
            if isinstance(child, list):
                parts.append(_adf_to_text(child))
    return "\n".join("".join(parts).splitlines())


def check_connection(config: dict) -> str:
    """Verify Jira connectivity/auth with the given config.

    Calls /rest/api/3/myself so it validates URL, email and API token in
    one shot. Returns a human-readable result string for the UI.
    """
    url = f"{config['jira_url']}/rest/api/3/myself"
    try:
        resp = requests.get(
            url,
            auth=(config["jira_email"], config["jira_api_token"]),
            timeout=15,
        )
        resp.raise_for_status()
        data = resp.json()
        who = data.get("displayName") or data.get("emailAddress") or "the account"
        return f"✅ Connected to Jira as **{who}**."
    except requests.HTTPError as e:
        status = e.response.status_code if e.response is not None else "error"
        if status == 401:
            return "❌ Jira returned **401 Unauthorized** — check your email and API token."
        if status == 403:
            return "❌ Jira returned **403 Forbidden** — your account lacks permission."
        return f"❌ Jira request failed (HTTP {status}): {e}"
    except requests.RequestException as e:
        return f"❌ Could not reach Jira at `{config['jira_url']}`: {e}"


def fetch_ticket(key: str, config: dict) -> dict:
    """Fetch a Jira ticket and return {key, summary, description, acceptance_criteria}.

    Raises requests.HTTPError (or requests.RequestException) with a readable
    message on failure; callers render the error in the chat pane.
    """
    url = f"{config['jira_url']}/rest/api/3/issue/{key}"
    resp = requests.get(
        url,
        params={"fields": "summary,description"},
        auth=(config["jira_email"], config["jira_api_token"]),
        timeout=30,
    )
    resp.raise_for_status()

    data = resp.json()
    fields = data.get("fields") or {}
    return {
        "key": key,
        "summary": fields.get("summary") or "",
        "description": _adf_to_text(fields.get("description", {}).get("content") or []),
        "acceptance_criteria": _acceptance_criteria(fields),
    }
