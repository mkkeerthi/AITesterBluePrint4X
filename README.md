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

## License

_Add license information here._
