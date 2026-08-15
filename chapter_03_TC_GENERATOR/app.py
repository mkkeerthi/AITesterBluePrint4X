"""Screen 1 — Chat: Jira ticket key in, test case draft out."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import requests

import config_store
import jira_client
import llm_client

st.set_page_config(page_title="Jira Test Case Generator", page_icon="🧪")
st.title("🧪 Jira Test Case Generator")

if "messages" not in st.session_state:
    st.session_state["messages"] = []


def _is_configured(config: dict) -> bool:
    return all(config.get(key) for key in ("jira_url", "jira_email", "jira_api_token", "groq_api_key"))


def _handle_request(user_text: str) -> str:
    config = st.session_state.get("config") or config_store.get_config()
    if not _is_configured(config):
        return "Please open the **Settings** page and save your Jira and Groq credentials first."

    key = jira_client.extract_ticket_key(user_text)
    if not key:
        return "I couldn't find a Jira ticket key in your message. Try something like: `create test cases for QA-102`"

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


for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("e.g. create test cases for QA-102")
if prompt:
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Fetching ticket and generating test cases..."):
            reply = _handle_request(prompt)
        st.markdown(reply)
    st.session_state["messages"].append({"role": "assistant", "content": reply})
