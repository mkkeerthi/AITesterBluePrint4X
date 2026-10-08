# Deploying QABuddy on a DigitalOcean droplet (or any VPS)

The app stack runs on one machine with Docker Compose: Ollama (embeddings), the QABuddy
app (API, reranker, UI) and Caddy (HTTPS + a team login). The vector store is Qdrant — a
managed Qdrant Cloud cluster (recommended) or your own server — reached through
`QDRANT_URL` + `QDRANT_API_KEY` in `.env`; it needs no local container. Only ports 80/443
are exposed; Ollama is reachable from the app container only.

> Status: the compose file and Dockerfile are written but **not yet run end to end**,
> because the build machine had no Docker. The same code runs locally via `./run.sh`
> and is tested there. Expect to iterate once on the first droplet boot.

## 1. Pick a droplet size

The embedding model is the main cost driver. The default is the lightweight
Qwen3-Embedding-0.6B, which runs comfortably on CPU. Measured on the build machine
(M3 Max, Metal GPU) the 4B model embeds about **1,100 tokens/s**, so the 838-chunk
sample corpus took ~5 minutes; a CPU-only droplet is several times slower (not measured
here), which matters for the first full ingest of 5,000 test cases.

| Droplet | EMBED_MODEL | RERANK_MODEL | Notes |
|---|---|---|---|
| 8 GB RAM / 4 vCPU, CPU | `qwen3-embedding:0.6b` | `cross-encoder/ms-marco-MiniLM-L-6-v2`, `RERANK_CANDIDATES=12` | Cheapest. Fine for a team; first ingest of 5k test cases will take a while |
| 16 GB / 8 vCPU, CPU | `qwen3-embedding:0.6b` (or 4b if you can wait for ingest) | `cross-encoder/ms-marco-MiniLM-L-6-v2` | Best CPU option. Reranking 24 candidates on CPU costs a few seconds per question |
| GPU droplet | `qwen3-embedding:4b` | `BAAI/bge-reranker-v2-m3` | Matches the build machine's quality and speed |

Shortcut for a small droplet: run the big first ingest on a laptop with a GPU, then move
the Qdrant collection over with a snapshot (step 6). Queries need one embedding each,
which any CPU handles. **Both machines must use the same EMBED_MODEL and EMBED_DIM.**

## 2. Prepare

```bash
ssh root@your-droplet
apt-get update && apt-get install -y docker.io docker-compose-v2 git
git clone <this repo> /opt/qabuddy && cd /opt/qabuddy/chapter_12_RAG_QA_BuddyAI
cp .env.example .env          # set GROQ_API_KEY, QDRANT_URL + QDRANT_API_KEY, EMBED_MODEL, JIRA_*; keep comments on their own lines
```

Put your data in `data/` (the 10 source folders), and clone the framework repos into
`data/07_Source_Codes/`.

## 3. Login and domain

Point a DNS A record at the droplet, then create `deploy/.env` (read by Compose):

```bash
docker run --rm caddy:2 caddy hash-password --plaintext 'choose-a-password'
```

```dotenv
QABUDDY_DOMAIN=qabuddy.yourcompany.com
QABUDDY_USER=qa
# single quotes: bcrypt hashes contain $ signs that Compose would otherwise interpolate
QABUDDY_PASS_HASH='$2a$14$...paste...'
EMBED_MODEL=qwen3-embedding:0.6b
```

For a stricter setup, skip Caddy's public ports and put the droplet behind your VPN or
Tailscale instead. The index contains source code, tickets and logs: do not expose it
without authentication.

## 4. Start and ingest

```bash
cd deploy
docker compose up -d --build
docker compose logs -f ollama-pull           # wait for the embedding model to finish pulling
docker compose exec app python -m qabuddy ingest
docker compose exec app python -m qabuddy eval   # sanity check: hit@k and MRR on the golden set
```

Open `https://qabuddy.yourcompany.com`.

## 5. The answer LLM and its rate limit

Groq's on-demand tier allows **8,000 tokens per minute** for `openai/gpt-oss-120b`, and it
counts the `max_tokens` reservation against that budget. One answer reserves about
3,000 to 4,000 tokens, so the shared key serves **about two answers per minute**. QABuddy
waits and retries on a 429 (and tells the user it is waiting), but a team will feel it.

Options:
* Upgrade to Groq's Dev tier (higher limits, same code).
* `LLM_PROVIDER=openai` with any OpenAI-compatible endpoint.
* Fully self-hosted: `LLM_PROVIDER=ollama`, `LLM_MODEL=gpt-oss:20b` on a GPU droplet.

## 6. Backups and moving the index

```bash
# $QDRANT_URL is your cluster URL; drop the api-key header for an unauthenticated local server.
# on the source machine: create the snapshot
curl -X POST "$QDRANT_URL/collections/qabuddy/snapshots" -H "api-key: $QDRANT_API_KEY"
# download it (Qdrant Cloud console, or .qdrant/snapshots/ locally), copy it over, then:
curl -X POST "$QDRANT_URL/collections/qabuddy/snapshots/upload?priority=snapshot" \
     -H "api-key: $QDRANT_API_KEY" -H 'Content-Type: multipart/form-data' -F 'snapshot=@<name>.snapshot'
```

Also copy `.index/manifest.json`, so the next ingest knows which files are already indexed.

## 7. Phase 2: hourly auto-ingestion (plan)

`deploy/hourly-ingest.cron` is the whole plan: every hour, `git pull` each framework
repo, sync Jira tickets updated in the last two hours, then run the incremental ingest.
Ingestion hashes every file (sha256), so only changed files are re-chunked and
re-embedded, deleted files are removed from Qdrant, and a quiet hour costs seconds.
Changing EMBED_MODEL or EMBED_DIM forces a full rebuild automatically.

Figma (phase 2): read frame names, text layers and component names through the Figma
REST API node tree as text, and caption frame renders with a vision model; ER diagrams
become entity/relationship sentences, the same way Lucid charts are handled today.
