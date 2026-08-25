"""Screen 1 — Chat: Jira ticket key in, test case draft out."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import csv
import io
import re

import streamlit as st
import requests

import config_store
import jira_client
import llm_client

st.set_page_config(page_title="Jira AI Agent", page_icon="🎯", layout="wide")
st.title("🛡️ Jira AI Agent")

# Narrow the sidebar so the chat area gets more room, and style buttons orange.
st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 200px !important;
        }
        .stButton > button,
        .stDownloadButton > button {
            background-color: #FF6B00;
            color: white;
            border: none;
        }
        .stButton > button:hover,
        .stDownloadButton > button:hover {
            background-color: #E05E00;
            color: white;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Tool mode: existing test case generation, or the new requirement analyser.
MODE_TEST_CASES = "Generate Test Cases"
MODE_ANALYSE = "Analyse Requirement"
mode = st.selectbox(
    "Mode",
    options=[MODE_TEST_CASES, MODE_ANALYSE],
    help="Generate Test Cases: turn a Jira ticket into a test case draft. "
    "Analyse Requirement: judge whether a ticket is ready to test.",
)
st.session_state["mode"] = mode

# Keep a separate chat history per mode so they don't bleed into each other.
history_key = "messages_generate" if mode == MODE_TEST_CASES else "messages_analyse"
if history_key not in st.session_state:
    st.session_state[history_key] = []


def _parse_test_cases(markdown: str) -> list[dict]:
    """Extract rows from the markdown table the LLM returns.

    Returns a list of dicts keyed by the table header (TID, Test Case
    Description, ...) or an empty list if no table can be found.
    """
    # Find the first markdown table: header row, separator row, data rows.
    lines = [line.strip() for line in markdown.splitlines()]
    header_idx = None
    for i, line in enumerate(lines):
        if line.startswith("|") and "-" in line and re.search(r"^\|[\s:|-]+\|?$", line):
            header_idx = i - 1
            break

    if header_idx is None or header_idx < 0:
        return []

    header = [c.strip() for c in lines[header_idx].strip("|").split("|")]
    rows = []
    for line in lines[header_idx + 2 :]:
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) != len(header):
            continue
        rows.append(dict(zip(header, cells)))
    return rows


def _cases_to_csv(rows: list[dict]) -> str:
    if not rows:
        return ""
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue()


def _test_case_actions(markdown: str, key: str) -> None:
    """Render the Export-to-CSV button for a generated markdown reply."""
    rows = _parse_test_cases(markdown)
    if not rows:
        return

    st.download_button(
        "⬇️ Export to CSV",
        data=_cases_to_csv(rows),
        file_name=f"test_cases_{key}.csv",
        mime="text/csv",
        key=f"csv_{key}",
    )


def _is_configured(config: dict) -> bool:
    return all(config.get(key) for key in ("jira_url", "jira_email", "jira_api_token", "groq_api_key"))


def _handle_request(user_text: str) -> str:
    config = st.session_state.get("config") or config_store.get_config()
    if not _is_configured(config):
        return "Please open the **Settings** page and save your Jira and Groq credentials first."

    key = jira_client.extract_ticket_key(user_text)
    if not key:
        return "I couldn't find a Jira ticket key in your message. Try uppercase letters like `QA-102`."

    try:
        ticket = jira_client.fetch_ticket(key, config)
    except requests.HTTPError as e:
        if e.response is not None and e.response.status_code == 401:
            return "Jira returned **401 Unauthorized** — please check your credentials in **Settings**."
        if e.response is not None and e.response.status_code == 404:
            return f"Ticket **{key}** was not found in Jira. Check the key and try again."
        return f"Jira request failed ({e.response.status_code if e.response is not None else 'error'}): {e}"
    except requests.RequestException as e:
        return f"Could not reach Jira: {e}"

    try:
        return llm_client.generate_test_cases(ticket, config)
    except Exception as e:  # Groq SDK raises APIStatusError etc.
        return f"Test case generation failed: {e}"


def _analyse_ticket(ticket: dict) -> str:
    """Run the requirement analysis for a ticket dict; returns the report markdown."""
    config = st.session_state.get("config") or config_store.get_config()
    try:
        return llm_client.analyze_requirement(ticket, config)
    except Exception as e:  # Groq SDK raises APIStatusError etc.
        return f"Requirement analysis failed: {e}"


def _handle_analyse(user_text: str) -> str:
    """Analyse a requirement from a Jira key, falling back to a pasted ticket body."""
    config = st.session_state.get("config") or config_store.get_config()
    if not _is_configured(config):
        return "Please open the **Settings** page and save your Jira and Groq credentials first."
    if not config.get("groq_api_key"):
        return "Please add your **Groq API key** in **Settings** first."

    key = jira_client.extract_ticket_key(user_text)
    if not key:
        return "I couldn't find a Jira ticket key in your message. Try uppercase letters like `QA-102`."

    try:
        ticket = jira_client.fetch_ticket(key, config)
    except requests.HTTPError as e:
        if e.response is not None and e.response.status_code == 401:
            return "Jira returned **401 Unauthorized** — please check your credentials in **Settings**."
        if e.response is not None and e.response.status_code == 404:
            return f"Ticket **{key}** was not found in Jira. Check the key and try again."
        return f"Jira request failed ({e.response.status_code if e.response is not None else 'error'}): {e}"
    except requests.RequestException as e:
        # Jira unreachable — remember the key so the paste box is shown on the
        # next rerun (Streamlit buttons only show their effect on a fresh run).
        st.session_state["pending_analyse_key"] = key
        st.session_state["pending_analyse_error"] = str(e)
        return ""

    return _analyse_ticket(ticket)


for i, message in enumerate(st.session_state[history_key]):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant" and mode == MODE_TEST_CASES:
            _test_case_actions(message["content"], f"msg_{i}")

# If Jira was unreachable for an analysis request, offer a paste-ticket fallback.
if (
    mode == MODE_ANALYSE
    and st.session_state.get("pending_analyse_key")
    and st.session_state.get("pending_analyse_error")
):
    pending_key = st.session_state["pending_analyse_key"]
    st.warning(
        f"Could not reach Jira for **{pending_key}**: "
        f"{st.session_state['pending_analyse_error']}. Paste the ticket content to analyse it."
    )
    pasted = st.text_area(
        "Paste the ticket body (summary, description, acceptance criteria)",
        key="pasted_ticket",
        height=200,
    )
    if st.button("Analyse pasted ticket"):
        if pasted.strip():
            del st.session_state["pending_analyse_key"]
            del st.session_state["pending_analyse_error"]
            pseudo_ticket = {
                "key": pending_key,
                "summary": "",
                "description": pasted.strip(),
                "acceptance_criteria": "",
            }
            with st.chat_message("assistant"):
                with st.spinner("Analysing pasted requirement..."):
                    reply = _analyse_ticket(pseudo_ticket)
                st.markdown(reply)
                st.session_state[history_key].append({"role": "assistant", "content": reply})
        else:
            st.error("Nothing was pasted to analyse.")

prompt = st.chat_input("Enter Jira ticket key (example: QA-102)")
if prompt:
    st.session_state[history_key].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if mode == MODE_TEST_CASES:
            with st.spinner("Fetching ticket and generating test cases..."):
                reply = _handle_request(prompt)
        else:
            with st.spinner("Fetching ticket and analysing requirement..."):
                reply = _handle_analyse(prompt)
        if reply:
            st.markdown(reply)
            if mode == MODE_TEST_CASES:
                _test_case_actions(reply, "latest")
            st.session_state[history_key].append({"role": "assistant", "content": reply})
