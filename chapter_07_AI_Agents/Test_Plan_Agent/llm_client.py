"""Groq-backed test plan generation for the Test Plan Agent.

Loads the template from templates/, merges the fetched ticket content into
the {{PLACEHOLDERS}}, and asks Groq to produce the test plan.
"""

import datetime
import os

from groq import Groq

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(BASE_DIR, "test_plan_template.md")

DEFAULT_MODEL = "openai/gpt-oss-120b"


def list_models(config: dict) -> list[str]:
    """Return sorted Groq model ids, or [] when the key is missing/invalid."""
    api_key = (config.get("groq_api_key") or "").strip()
    if not api_key:
        return []
    try:
        client = Groq(api_key=api_key)
        models = client.models.list()
        return sorted(m.id for m in models.data)
    except Exception:
        return []


def check_connection(config: dict) -> str:
    """Verify Groq connectivity/auth with the given API key."""
    api_key = (config.get("groq_api_key") or "").strip()
    if not api_key:
        return "❌ Groq API key is empty — enter it and try again."
    try:
        client = Groq(api_key=api_key)
        models = client.models.list()
        names = ", ".join(sorted(m.id for m in models.data)[:5])
        return f"✅ Connected to Groq. Available models include: `{names}`."
    except Exception as e:
        return f"❌ Groq connection failed: {e}"


def _load_template() -> str:
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        return f.read()


def _fill_placeholders(template: str, ticket: dict, config: dict, model: str) -> str:
    jira_url = (config.get("jira_url") or "").rstrip("/")
    return (
        template.replace("{{FEATURE}}", ticket.get("summary", "Untitled Feature"))
        .replace("{{KEY}}", ticket.get("key", ""))
        .replace("{{URL}}", f"{jira_url}/browse/{ticket.get('key', '')}")
        .replace("{{TITLE}}", ticket.get("summary", ""))
        .replace("{{DATE}}", datetime.date.today().isoformat())
        .replace("{{MODEL}}", model)
        .replace("{{DESCRIPTION}}", ticket.get("description", "Not provided."))
        .replace(
            "{{ACCEPTANCE_CRITERIA}}",
            ticket.get("acceptance_criteria", "Not provided."),
        )
    )


def generate_test_plan(ticket: dict, config: dict, model: str | None = None) -> str:
    """Return a test plan (markdown) for the given ticket via Groq."""
    model = model or config.get("groq_model") or DEFAULT_MODEL
    prompt = _fill_placeholders(_load_template(), ticket, config, model)
    client = Groq(api_key=config["groq_api_key"])
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert QA lead with 15+ years of experience. "
                    "You write enterprise-grade, traceable test plans with zero invented content. "
                    "Every section must be grounded strictly in the ticket details provided; "
                    "missing or unclear information is stated as such, never fabricated."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.0,
    )
    return response.choices[0].message.content
