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
└── README.md
```

## Chapters

- **Chapter 1 — LLM Basics:** Anti-hallucination rules for LLM-assisted QA
  (no invented features, traceable assertions, deterministic output).
- **Chapter 2 — Prompt Engineering:** RICE-POT framework (Role, Instructions,
  Context, Example, Parameters, Output, Tone) applied to generate functional
  and non-functional test cases for VWO (`app.vwo.com`) from a real PRD.

## License

_Add license information here._
