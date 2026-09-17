# AI Tester Blueprint 4X

Hands-on learning path for AI-assisted testers — learn how to prompt LLMs for
enterprise-grade QA work using deterministic, anti-hallucination guardrails.

## Project Structure

```
├── chapter_01_LLM_BASICS/
│   └── AntiHallucinationRequirement.md     # Strict rules: verifiable facts only, no invented content
├── chapter_02_PROMPT_ENG/
│   └── task_01_TCGeneration_RicePot/       # Worked example: RICE-POT prompt framework
│       ├── input/                          # PRD, screenshots, and prompt used as inputs
│       │   ├── LoginPageScreenshot.jpg
│       │   ├── RICE_POT_TC_Prompt.md       # The reusable RICE-POT prompt template
│       │   └── VWO_ProjectRequirementDocument.docx
│       └── output/                         # Generated QA artifacts
│           ├── Functional_TestCases.xlsx
│           ├── NonFunctional_TestCases.xlsx
│           ├── TestPlan.docx
│           └── raw/                        # CSV / DOCX intermediates
├── chapter_03_TC_GENERATOR/               # Streamlit app: Jira ticket → Groq
│   ├── app.py                             # Chat screen w/ mode dropdown (streamlit run app.py)
│   ├── pages/settings.py                  # Settings screen (Jira + Groq credentials)
│   ├── config_store.py                    # Persisted config (config.json, seeded from .env)
│   ├── jira_client.py                     # Fetches ticket details via Jira REST API
│   ├── llm_client.py                      # Merges template + ticket, calls Groq
│   ├── templates/
│   │   ├── test_cases_template.md         # Test case template with placeholders
│   │   └── requirement_analyse_template.md # Requirement readiness template with placeholders
│   └── requirements.txt
├── chapter_07_AI_Agents/
│   └── Test_Plan_Agent/                    # Streamlit app: Jira ticket → B.L.A.S.T. test plan
│       ├── app.py                          # Chat screen w/ mode dropdown
│       ├── pages/settings.py               # Settings screen (Jira + Groq credentials)
│       ├── config_store.py                 # Persisted config (config.json, seeded from .env)
│       ├── jira_client.py                  # Fetches ticket details via Jira REST API
│       ├── llm_client.py                   # Merges template + ticket, calls Groq
│       ├── test_plan_template.md           # Test plan template with placeholders
│       ├── BLAST.md                        # B.L.A.S.T. protocol master system prompt
│       ├── LLM.md                          # Project constitution (schemas, rules)
│       ├── task_plan.md                    # Phases, goals, checklists
│       ├── findings.md                     # Research, discoveries, constraints
│       ├── progress.md                     # What was done, errors, tests, results
│       └── requirements.txt
├── chapter_09_Langflow/                    # Local Langflow instance (visual LLM workflows)
│   └── .venv/                              # Python 3.13 venv, Langflow installed (gitignored)
└── README.md
```

## Chapters

- **Chapter 1 — LLM Basics:** Anti-hallucination rules for LLM-assisted QA
  (no invented features, traceable assertions, deterministic output).
- **Chapter 2 — Prompt Engineering:** RICE-POT framework (Role, Instructions,
  Context, Example, Parameters, Output, Tone) applied to generate functional
  and non-functional test cases for VWO (`app.vwo.com`) from a real PRD.
- **Chapter 3 — Test Case Generator App:** A two-screen Streamlit app that turns
  a Jira ticket key (e.g. `QA-102`) into Groq-generated output. A mode dropdown
  picks between **Generate Test Cases** (existing behavior) and **Analyse
  Requirement**, which produces a requirement-readiness report from the ticket;
  if Jira is unreachable the analyser lets you paste the ticket body instead.
  Credentials are stored locally in `config.json` (seeded from `.env`), both
  excluded from version control.
- **Chapter 7 — AI Agents (Test Plan Agent):** Extends the Chapter 3 app pattern to
  generate a structured **test plan** from a Jira ticket using the **B.L.A.S.T.**
  protocol (Blueprint, Link, Architect, Stylize, Trigger). Project memory lives in
  `task_plan.md`, `findings.md`, and `progress.md`, with `LLM.md` as the project
  constitution. See `BLAST.md` for the full protocol prompt.
- **Chapter 9 — Langflow:** A local [Langflow](https://github.com/langflow-ai/langflow)
  instance (visual, drag-and-drop builder for LLM/agent workflows) installed in an
  isolated Python 3.13 venv. Run it and open <http://127.0.0.1:7860>; setup and
  run steps are in `chapter_09_Langflow/README.md`.

## License

_Add license information here._
