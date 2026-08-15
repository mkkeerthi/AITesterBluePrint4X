"""Groq-backed test case generation for the Jira Test Case Generator.

Loads the template from templates/, merges the fetched ticket content into
the {{PLACEHOLDERS}}, and asks Groq to produce the test cases.
"""

import os

from groq import Groq

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(BASE_DIR, "templates", "test_cases_template.md")

DEFAULT_MODEL = "llama-3.3-70b-versatile"


def _load_template() -> str:
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
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


def generate_test_cases(ticket: dict, config: dict, model: str = DEFAULT_MODEL) -> str:
    """Return test cases (markdown) for the given ticket via Groq."""
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
