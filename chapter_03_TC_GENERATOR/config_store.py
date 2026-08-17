"""Persisted settings for the Jira Test Case Generator.

Reads/writes a local config.json (gitignored). On first run, when no
config.json exists, seeds values from the .env file in this folder.
Never hardcodes credentials in source code.
"""

import json
import os
import re

from dotenv import load_dotenv

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIG_PATH = os.path.join(_BASE_DIR, "config.json")
# The provided .env lives in the src/ folder next to the prompt.
ENV_PATH = os.path.join(_BASE_DIR, "src", ".env")

REQUIRED_KEYS = (
    "jira_url",
    "jira_email",
    "jira_api_token",
    "groq_api_key",
    "groq_model",
)


def _normalize_jira_url(url: str) -> str:
    """Ensure the Jira URL has a scheme (defaults to https://)."""
    url = (url or "").strip().rstrip("/")
    if url and not re.match(r"^https?://", url, re.IGNORECASE):
        url = "https://" + url
    return url


def _load_env_values() -> dict:
    """Return config values found in .env (empty strings when absent)."""
    load_dotenv(ENV_PATH)
    values = {
        "jira_url": os.getenv("JIRA_URL", ""),
        "jira_email": os.getenv("JIRA_EMAIL", ""),
        "jira_api_token": os.getenv("JIRA_API_TOKEN", ""),
        "groq_api_key": os.getenv("GROQ_API_KEY", ""),
        "groq_model": os.getenv("GROQ_MODEL", ""),
    }
    values["jira_url"] = _normalize_jira_url(values["jira_url"])
    return values


def get_config() -> dict:
    """Return the persisted config, seeding from .env on first run."""
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        # Backfill any keys missing from an older config file.
        env_values = _load_env_values()
        for key in REQUIRED_KEYS:
            data.setdefault(key, env_values.get(key, ""))
        data["jira_url"] = _normalize_jira_url(data.get("jira_url", ""))
        return data
    return _load_env_values()


def save_config(values: dict) -> dict:
    """Persist the given config to config.json and return the saved dict."""
    clean = {key: (values.get(key) or "").strip() for key in REQUIRED_KEYS}
    clean["jira_url"] = _normalize_jira_url(clean["jira_url"])
    if clean["groq_model"] == "":
        clean["groq_model"] = "llama-3.3-70b-versatile"
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(clean, f, indent=2)
    return clean
