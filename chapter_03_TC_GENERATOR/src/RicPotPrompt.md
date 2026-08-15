# RICE-POT Prompt — Jira Test Case Generator App

## Role
You are a senior Python full-stack engineer and AI application architect, experienced in building lightweight internal tools with Streamlit, integrating REST APIs (Jira Cloud/Server) and orchestrating hosted Groq providers.

## Instructions
[Mandatory] Build a **two-screen Streamlit application**:
- **Screen 1 — Chat**: A ChatGPT-style interface with a text input box and a Send button. The user types natural-language requests such as "create test cases for JIRA-102" and clicks Send.
- **Screen 2 — Settings**: A configuration screen to input and persist: Jira URL, Jira email ID, Jira API token and Groq API key.

[Mandatory] End-to-end flow when the user requests test cases for a Jira ID:
1. Parse the Jira ticket key from the chat message.
2. Fetch ticket details (summary, description, acceptance criteria) via the Jira REST API using the stored credentials.
3. Load the test case template from a local `/templates` folder.
4. Generate test cases with Groq, using the fetched ticket content merged into the template structure.
5. Render the generated test cases back in the chat pane.

[Don't] Don't hardcode any credentials (Jira token, Groq key) in source code — persist them via a local config layer (e.g. JSON file or SQLite), excluded from version control.

[Output] **Plan first.** Before writing any code, output the proposed file structure, the two screens, and the data flow between them. Wait for my approval. Only then build step by step, one module at a time.

## Context
This is an internal QA productivity tool, not a production SaaS product. It exists to take a single Jira ticket and turn it into a test case draft using Groq with minimal setup and no unnecessary abstraction.

## Example
Sample interaction:
> User types: `create test cases for QA-102` → clicks Send
> App fetches ticket QA-102 from Jira → merges its description/acceptance criteria into the template from `/templates` → sends the combined prompt to Groq → renders the structured test cases in the chat pane, the same way a ChatGPT response would appear.

## Parameters
- Jira base URL, Jira email ID, Jira API token — provided separately, entered/saved via the Settings screen
- Groq API key — provided separately, entered/saved via the Settings screen

## Output
Deliver exactly:
- `app.py` — main chat screen
- `pages/settings.py` (or equivalent Streamlit multipage settings screen)
- `config_store.py` — handles reading/writing persisted settings (Jira + Groq credentials, provider choice)
- `jira_client.py` — fetches ticket details from Jira REST API
- `llm_client.py` — handles Groq calls
- `templates/` — folder with at least one sample test case template
- `requirements.txt`

## Tone
Technical, precise, minimal dependencies, no over-engineered abstractions — working code only, structured clearly enough that each module can be reviewed independently before moving to the next.