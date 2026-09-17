# from lfx.field_typing import Data
import base64

import httpx

from lfx.custom.custom_component.component import Component
from lfx.io import MessageTextInput, Output, SecretStrInput, StrInput
from lfx.schema.message import Message
from lfx.schema.data import Data


class CustomComponent(Component):
    display_name = "Jira Component"
    description = "Fetch a Jira work item description by key."
    documentation: str = "https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issues/"
    icon = "jira"
    name = "JiraComponent"

    inputs = [
        MessageTextInput(name="jira_work_key", display_name="Jira Work Item Key", required=True,
                info="The work item to read, e.g. SCRUM-1. Connect another component's Message output here, or type it.",
                value="SCRUM-1", tool_mode=True),
        StrInput(name="jira_url", display_name="Jira URL", required=True,
                info="Your Jira site URL, e.g. https://xyz.atlassian.net", value="https://xyz.atlassian.net"),
        StrInput(name="jira_email", display_name="Jira Email", required=True,
                info="Email address of the Atlassian account the API key belongs to."),
        SecretStrInput(name="jira_api_key", display_name="Jira API Key", required=True,
                info="Your Jira API token. Create one at https://id.atlassian.com/manage-profile/security/api-tokens"),
    ]

    outputs = [
        Output(display_name="Output", name="output", method="fetch_description")
    ]

    def _build_headers(self) -> dict:
        token = base64.b64encode(f"{self.jira_email}:{self.jira_api_key}".encode()).decode()
        return {
            "Authorization": f"Basic {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def _resolve_work_key(self) -> str:
        value = self.jira_work_key
        if isinstance(value, Data):
            value = value.data.get(value.text_key, "")
        return str(value).strip()

    def _build_api_url(self) -> str:
        return f"{self.jira_url.rstrip('/')}/rest/api/3/issue/{self._resolve_work_key()}"

    def _adf_to_text(self, node) -> str:
        if isinstance(node, str):
            return node
        if isinstance(node, list):
            return " ".join(self._adf_to_text(child) for child in node)
        if isinstance(node, dict):
            if node.get("type") == "text":
                return node.get("text", "")
            if node.get("type") == "hardBreak":
                return "\n"
            return self._adf_to_text(node.get("content", []))
        return ""

    def _extract_description(self, issue_data: dict) -> str:
        fields = issue_data.get("fields", {})
        description = fields.get("description")
        if isinstance(description, dict):
            description = self._adf_to_text(description)
        return (description or "").strip() or fields.get("summary", "No description available")

    def fetch_description(self) -> Message:
        try:
            response = httpx.get(
                self._build_api_url(),
                headers=self._build_headers(),
                params={"fields": "summary,description"},
                timeout=60.0,
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise ValueError(f"Jira API error {exc.response.status_code}: {exc.response.text}") from exc
        except httpx.HTTPError as exc:
            raise ValueError(f"Could not reach the Jira API: {exc}") from exc

        description = self._extract_description(response.json())
        self.status = description
        return Message(text=description)
