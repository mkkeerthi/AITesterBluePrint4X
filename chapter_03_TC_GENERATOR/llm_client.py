"""Groq-backed test case generation for the Jira Test Case Generator.

Loads the template from templates/, merges the fetched ticket content into
the {{PLACEHOLDERS}}, and asks Groq to produce the test cases.
"""

import os

from groq import Groq

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(BASE_DIR, "templates", "test_cases_template.md")
REQUIREMENT_TEMPLATE_PATH = os.path.join(BASE_DIR, "templates", "requirement_analyse_template.md")

DEFAULT_MODEL = "llama-3.3-70b-versatile"


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
    """Verify Groq connectivity/auth with the given API key.

    Lists models — a cheap authenticated call. Returns a human-readable
    result string for the UI.
    """
    api_key = (config.get("groq_api_key") or "").strip()
    if not api_key:
        return "❌ Groq API key is empty — enter it and try again."
    try:
        client = Groq(api_key=api_key)
        models = client.models.list()
        names = ", ".join(sorted(m.id for m in models.data)[:5])
        return f"✅ Connected to Groq. Available models include: `{names}`."
    except Exception as e:  # Groq SDK raises APIStatusError etc.
        return f"❌ Groq connection failed: {e}"


def _load_template(path: str = TEMPLATE_PATH) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def _fill_placeholders(template: str, ticket: dict) -> str:
    return (
        template.replace("{{TICKET_KEY}}", ticket.get("key", ""))
        .replace("{{SUMMARY}}", ticket.get("summary", "Not provided."))
        .replace("{{DESCRIPTION}}", ticket.get("description", "Not provided."))
        .replace(
            "{{ACCEPTANCE_CRITERIA}}",
            ticket.get("acceptance_criteria", "Not provided."),
        )
    )


def generate_test_cases(ticket: dict, config: dict, model: str | None = None) -> str:
    """Return test cases (markdown) for the given ticket via Groq."""
    model = model or config.get("groq_model") or DEFAULT_MODEL
    prompt = _fill_placeholders(_load_template(), ticket)
    client = Groq(api_key=config["groq_api_key"])
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert QA functional tester with 15+ years of experience. "
                    "You write enterprise-grade, traceable test cases with zero invented content."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.0,
    )
    return response.choices[0].message.content


def analyze_requirement(ticket: dict, config: dict, model: str | None = None) -> str:
    """Return a requirement readiness report (markdown) for the given ticket via Groq."""
    model = model or config.get("groq_model") or DEFAULT_MODEL
    prompt = _fill_placeholders(_load_template(REQUIREMENT_TEMPLATE_PATH), ticket)
    client = Groq(api_key=config["groq_api_key"])
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert QA lead who pressure-tests whether a JIRA story is "
                    "ready to test. Follow the user's workflow exactly, surface gaps, "
                    "ambiguities and risks, and never fabricate content — a missing item "
                    "is a finding, not a blank to fill."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.0,
    )
    return response.choices[0].message.content
