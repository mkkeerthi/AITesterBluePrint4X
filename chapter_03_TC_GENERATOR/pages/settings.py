"""Screen 2 — Settings: configure and persist Jira + Groq credentials."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st

import config_store
import jira_client
import llm_client

st.set_page_config(page_title="Settings", page_icon="⚙️", layout="wide")
st.title("⚙️ Settings")

# Narrow the sidebar so the form gets more room, and style buttons orange.
st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 200px !important;
        }
        .stButton > button,
        .stDownloadButton > button,
        [data-testid="stFormSubmitButton"] > button {
            background-color: #FF6B00;
            color: white;
            border: none;
        }
        .stButton > button:hover,
        .stDownloadButton > button:hover,
        [data-testid="stFormSubmitButton"] > button:hover {
            background-color: #E05E00;
            color: white;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

config = config_store.get_config()

# The model list comes from Groq; a key is mandatory, so with no key the
# dropdown stays empty (disabled) instead of showing a static fallback list.
saved_model = config.get("groq_model") or ""
available_models = llm_client.list_models({"groq_api_key": config.get("groq_api_key", "")})
model_index = available_models.index(saved_model) if saved_model in available_models else 0

with st.form("settings_form"):
    jira_url = st.text_input("Jira URL", value=config["jira_url"], placeholder="https://yourcompany.atlassian.net")
    jira_email = st.text_input("Jira email ID", value=config["jira_email"])
    jira_token = st.text_input("Jira API token", value=config["jira_api_token"], type="password")
    groq_key = st.text_input("Groq API key", value=config["groq_api_key"], type="password")
    groq_model = st.selectbox(
        "Groq model",
        options=available_models or ["— enter your API key to load models —"],
        index=0 if not available_models else model_index,
        disabled=not available_models,
        help="Models are fetched from your Groq account. Save your API key, then save settings.",
    )
    submitted = st.form_submit_button("Save settings")

if submitted:
    saved = config_store.save_config(
        {
            "jira_url": jira_url,
            "jira_email": jira_email,
            "jira_api_token": jira_token,
            "groq_api_key": groq_key,
            "groq_model": groq_model if groq_model != "— enter your API key to load models —" else "",
        }
    )
    st.session_state["config"] = saved
    st.success("Settings saved to config.json.")

# Connectivity checks use whatever is typed in the fields (saved or not).
st.subheader("Connectivity checks")
col1, col2 = st.columns(2)
with col1:
    check_jira = st.button("🔌 Check Jira Connectivity")
with col2:
    check_groq = st.button("🔌 Check Groq Connectivity")

if check_jira:
    with st.spinner("Checking Jira..."):
        st.info(
            jira_client.check_connection(
                {
                    "jira_url": config_store._normalize_jira_url(jira_url),
                    "jira_email": jira_email,
                    "jira_api_token": jira_token,
                }
            )
        )
if check_groq:
    with st.spinner("Checking Groq..."):
        st.info(llm_client.check_connection({"groq_api_key": groq_key}))
