"""Screen 2 — Settings: configure and persist Jira + Groq credentials."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st

import config_store

st.set_page_config(page_title="Settings", page_icon="⚙️")
st.title("⚙️ Settings")

config = config_store.get_config()

with st.form("settings_form"):
    jira_url = st.text_input("Jira URL", value=config["jira_url"], placeholder="https://yourcompany.atlassian.net")
    jira_email = st.text_input("Jira email ID", value=config["jira_email"])
    jira_token = st.text_input("Jira API token", value=config["jira_api_token"], type="password")
    groq_key = st.text_input("Groq API key", value=config["groq_api_key"], type="password")
    submitted = st.form_submit_button("Save settings")

if submitted:
    saved = config_store.save_config(
        {
            "jira_url": jira_url,
            "jira_email": jira_email,
            "jira_api_token": jira_token,
            "groq_api_key": groq_key,
        }
    )
    st.session_state["config"] = saved
    st.success("Settings saved to config.json.")
