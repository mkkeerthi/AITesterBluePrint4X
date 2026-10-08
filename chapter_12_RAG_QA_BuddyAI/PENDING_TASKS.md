# QABuddy.ai: pending tasks

Status on 2026-10-04. QABuddy runs locally end to end (`./run.sh`, 838 chunks, cited answers in
3-5 s), the hosted demo is live at https://qabuddy-ai-nine.vercel.app, 18 regression tests pass,
and retrieval eval is 100% hit@6 on the golden set. Everything below is **not** done yet.

| Priority | Meaning |
|---|---|
| **P0** | Security or exposure: do first |
| **P1** | Needed before the team uses the DigitalOcean deployment |
| **P2** | Answer and retrieval quality |
| **P3** | Hygiene and nice-to-haves |

## P0: Security

- [ ] **Rotate the VWO test-account password in the public Selenium repo.**
  `ATB13xSeleniumAdvanceFramework/src/main/resources/data.properties` holds it in plain text on
  public GitHub. QABuddy redacts it before indexing, but the source repo still exposes it.
  *Done when:* the password is changed and the file reads it from an environment variable or CI secret.
- [ ] **Decide whether the public demo may expose the whole corpus.** Anyone can download
  `/demo/corpus.json`: the PRD, all 500 test cases, the VWO-26 and VWO-33 Jira exports and both
  repos' code. A secret scan found nothing, but the content itself is public.
  *Done when:* you accept it as-is, or turn on Vercel Deployment Protection, or ship a reduced corpus.
- [ ] **Make the demo rate limit real.** `api/demo-chat.js` counts requests in an in-memory `Map`.
  That count resets on every serverless cold start and is not shared between instances, so the
  "20 questions per hour per IP" cap does not hold under load. That cap is what protects the Groq key.
  *Done when:* the counter lives in Upstash Redis or Vercel KV.

## P1: DigitalOcean deployment (phase 1, written but never run)

- [ ] **Run the Docker Compose stack end to end on a droplet.** The build machine had no Docker, so
  `deploy/Dockerfile`, `docker-compose.yml` and `Caddyfile` are untested.
  *Done when:* `docker compose up -d --build`, then `ingest`, then `eval` shows 100% hit@6 behind the Caddy login.
- [ ] **Update `deploy/DEPLOY.md` for submodules.** Step 2 clones without `--recurse-submodules` and
  still says "clone the framework repos into `data/07_Source_Codes/`". Use
  `git clone --recurse-submodules` instead.
- [ ] **Check GitHub permalinks inside the container (likely broken).** In a fresh clone, each
  submodule's `.git` is a file that points into the parent repo's `.git/modules/`. Compose mounts only
  `../data`, so `git_info()` in `qabuddy/chunkers/code.py` cannot resolve the URL and commit. Ingestion
  still works, but code citations lose their GitHub links.
  *Fix:* mount the repo root read-only, or resolve URL and SHA on the host and pass them in through `sources.yaml`.
- [ ] **Fix `deploy/hourly-ingest.cron` before installing it.**
  - It runs `cd /opt/qabuddy`, but `DEPLOY.md` puts the app in `/opt/qabuddy/chapter_12_RAG_QA_BuddyAI`.
  - `git -C <repo> pull` fails on submodules, which sit on a detached HEAD. Use `git submodule update --remote --merge`.
  - `>> /var/log/qabuddy-ingest.log` captures only the last command. Wrap the chain in `{ ...; } >> log 2>&1`.
- [ ] **Measure CPU latency and pick the droplet size.** `DEPLOY.md` sizes the droplet from M3 Max
  numbers, and CPU embed and rerank speed was never measured.
  *Done when:* you have numbers for `qwen3-embedding:0.6b` vs `4b` and `bge-reranker-base` vs `v2-m3` on the chosen droplet.
- [ ] **Test the snapshot move** (`DEPLOY.md` step 6): build the index on a laptop, restore it on the droplet.
- [ ] **Run the Jira sync against a live Jira.** `python -m qabuddy sync-jira` (REST
  `/rest/api/3/search/jql`, `nextPageToken` paging) is unit-tested only.
  *Done when:* `JIRA_BASE_URL`, `JIRA_EMAIL`, `JIRA_API_TOKEN` and `JIRA_JQL` are set in `.env`, a sync
  writes tickets to `data/01_JIRA_Tickets/`, and they answer questions after `ingest`.
- [ ] **Raise the LLM capacity.** Groq's on-demand tier allows 8,000 tokens per minute and counts the
  `max_tokens` reservation, which is about 2 answers per minute per key.
  *Options:* Groq Dev tier, another OpenAI-compatible provider (`LLM_PROVIDER=openai`), or
  self-hosted `gpt-oss:20b` on a GPU droplet (`LLM_PROVIDER=ollama`).

## Phase 2 (from the build brief, plan only)

- [ ] **Hourly auto-ingestion:** install the fixed cron above, plus an alert when an ingest run fails.
- [ ] **Figma ingestion:** read frame names, text layers and component names from the Figma REST API
  node tree as text, and caption frame renders with a vision model. Turn ER diagrams into
  entity/relationship sentences, as Lucid charts are today. `data/06_Figma_Desings/` holds only a README.

## P2: Retrieval and answer quality

- [ ] **Stop summary chunks from outranking exact rows.** Outside the gap and RTM modes, module summaries
  sometimes rank above the row a question names: "email field visibility" puts the Login summary at #1
  and LOGIN-002 at #2. This is why the full pipeline only ties hybrid on MRR (0.91; it was 0.93 before
  the summaries).
  *Fix:* exclude or down-weight `summary` chunks unless the mode has quotas.
- [ ] **Grow the golden set** from 24 cases toward 100, using real team questions.
- [ ] **Add answer-level eval** (citation correctness, faithfulness). Today only retrieval is measured.
- [ ] **Re-record two demo answers.**
  - The gap analysis lists "Login" as a PRD feature (marked inferred), but the PRD has no login section.
  - "Build an RTM for PRD section 6" cites a single source.

  Run `./run.sh demo` (32 s pacing between questions, about 10 minutes), then `vercel --prod`.
- [ ] **Replace the sample data with real exports** as they become available. The Jenkins logs, meeting
  notes, Lucid charts, company docs and QAB-101..103 tickets are synthetic; see each folder's
  `_README_SAMPLE_DATA.md`.
- [ ] **When a framework repo changes upstream:** bump the submodule, re-ingest, re-run eval and
  re-record the demo. Code citations link to the pinned commit, so they stay correct until then.

## P3: Hygiene and nice-to-haves

- [ ] **Commit the UI checks as Playwright tests**, for both live mode and `VITE_DEMO=1`:
  - the page loads
  - an example replays
  - a citation chip opens the source viewer
  - there are no console errors

  So far these have only been checked by hand.
- [ ] **Code-split the UI bundle.** It is 677 KB, and Vite warns above 500 KB. Lazy-loading the
  highlight.js languages is the likely win.
- [ ] **Tidy the repo.** `.gitignore` lists `.vercel` twice. The folder name `06_Figma_Desings` has a typo,
  and two folders start with `06_`. Renaming means updating `sources.yaml` and re-ingesting, because
  chunk ids hash the file path.
- [ ] **Give the demo a custom domain** if it will be shared widely (`qabuddy-ai.vercel.app` was taken,
  hence `-nine`).
- [ ] **Capture feedback** (thumbs up or down per answer) and log questions, to feed the golden set and
  find weak spots.
