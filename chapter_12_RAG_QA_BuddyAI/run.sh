#!/usr/bin/env bash
# QABuddy, locally, in one command.
#
#   ./run.sh            start Ollama (and a local Qdrant unless QDRANT_URL is remote), ingest if empty, serve, open the browser
#   ./run.sh ingest     index changed files      (./run.sh ingest --full  rebuilds everything)
#   ./run.sh eval       retrieval hit-rate + MRR on eval/golden.yaml, with ablations
#   ./run.sh test       regression tests (no services needed)
#   ./run.sh ask "Why did build #142 fail?" [--mode rca]
#   ./run.sh demo       re-record the hosted demo (ui/public/demo + api/_prompt.js)
set -euo pipefail
cd "$(dirname "$0")"

PORT=$(grep -E '^PORT=' .env 2>/dev/null | cut -d= -f2 || true); PORT=${PORT:-8300}
EMBED_MODEL=$(grep -E '^EMBED_MODEL=' .env 2>/dev/null | cut -d= -f2 || true); EMBED_MODEL=${EMBED_MODEL:-qwen3-embedding:0.6b}
QDRANT_URL=$(grep -E '^QDRANT_URL=' .env 2>/dev/null | cut -d= -f2- || true); QDRANT_URL=${QDRANT_URL:-http://localhost:6333}
QDRANT_API_KEY=$(grep -E '^QDRANT_API_KEY=' .env 2>/dev/null | cut -d= -f2- || true)
QDRANT_CURL=(curl -s); [ -n "$QDRANT_API_KEY" ] && QDRANT_CURL=(curl -s -H "api-key: $QDRANT_API_KEY")
PY=.venv/bin/python

[ -f .env ] || { cp .env.example .env; echo "Created .env from .env.example. Add GROQ_API_KEY, then re-run."; exit 1; }

start_qdrant() {
  case "$QDRANT_URL" in
    *localhost*|*127.0.0.1*) ;;
    *) echo "Using remote Qdrant at $QDRANT_URL (skipping local server)"; return ;;
  esac
  curl -sf localhost:6333/ >/dev/null && return
  if [ ! -x .bin/qdrant ]; then
    case "$(uname -s)-$(uname -m)" in
      Darwin-arm64) asset=qdrant-aarch64-apple-darwin.tar.gz ;;
      Darwin-x86_64) asset=qdrant-x86_64-apple-darwin.tar.gz ;;
      Linux-x86_64) asset=qdrant-x86_64-unknown-linux-gnu.tar.gz ;;
      *) echo "Install Qdrant for your platform (or run: docker run -p 6333:6333 qdrant/qdrant)"; exit 1 ;;
    esac
    echo "Downloading Qdrant v1.19.1 ($asset)…"
    mkdir -p .bin && curl -sL "https://github.com/qdrant/qdrant/releases/download/v1.19.1/$asset" | tar xz -C .bin
    xattr -d com.apple.quarantine .bin/qdrant 2>/dev/null || true
  fi
  mkdir -p .qdrant
  QDRANT__STORAGE__STORAGE_PATH=.qdrant/storage QDRANT__STORAGE__SNAPSHOTS_PATH=.qdrant/snapshots \
    QDRANT__TELEMETRY_DISABLED=true nohup .bin/qdrant > .qdrant/qdrant.log 2>&1 &
  for _ in $(seq 20); do curl -sf localhost:6333/ >/dev/null && return; sleep 0.5; done
  echo "Qdrant did not start; see .qdrant/qdrant.log"; exit 1
}

start_ollama() {
  command -v ollama >/dev/null || { echo "Install Ollama from https://ollama.com, then re-run."; exit 1; }
  curl -sf localhost:11434/api/version >/dev/null || { nohup ollama serve > /tmp/ollama.log 2>&1 & sleep 3; }
  ollama list | grep -q "^${EMBED_MODEL}" || ollama pull "$EMBED_MODEL"
}

python_env() {
  [ -x "$PY" ] && return
  if command -v uv >/dev/null; then
    uv venv -q --python 3.13 .venv && uv pip install -q --python "$PY" -r requirements.txt pytest
  else
    python3 -m venv .venv && "$PY" -m pip install -q -r requirements.txt pytest
  fi
}

fetch_repos() {
  # the two framework repos are git submodules, pinned to the commits the index was built from
  [ -e data/07_Source_Codes/ATB13xSeleniumAdvanceFramework/.git ] && [ -e data/07_Source_Codes/AdvancePlaywrightFramework1x/.git ] && return
  echo "Fetching the framework repos (git submodules)…"
  git submodule update --init -- data/07_Source_Codes ||
    echo "Could not fetch them: clone both repos into data/07_Source_Codes/ (see README). Code questions will have no sources."
}

ui_build() {
  [ -f ui/dist/index.html ] && return
  (cd ui && npm install --silent && npm run build)
}

cmd=${1:-up}
case "$cmd" in
  test)  python_env; exec "$PY" -m pytest -q tests ;;
  ingest) fetch_repos; start_qdrant; start_ollama; python_env; shift; exec "$PY" -m qabuddy ingest "$@" ;;
  eval)  start_qdrant; start_ollama; python_env; exec "$PY" -m qabuddy eval ;;
  ask)   start_qdrant; start_ollama; python_env; shift; exec "$PY" -m qabuddy ask "$@" ;;
  demo)
    start_qdrant; start_ollama; python_env; "$PY" -m qabuddy export-demo; (cd ui && npm install --silent && npm run build:demo)
    echo "Demo build -> ui/dist-demo (preview: python3 -m http.server 5310 -d ui/dist-demo). Deploy: vercel --prod"
    ;;
  up|*)
    fetch_repos; start_qdrant; start_ollama; python_env; ui_build
    points=$("${QDRANT_CURL[@]}" "$QDRANT_URL/collections/qabuddy" | "$PY" -c "import json,sys; print(json.load(sys.stdin).get('result',{}).get('points_count',0))" 2>/dev/null || echo 0)
    if [ "${points:-0}" = "0" ]; then echo "Index is empty: ingesting (first run embeds everything, a few minutes)…"; "$PY" -m qabuddy ingest; fi
    echo "QABuddy -> http://localhost:${PORT}"
    (sleep 4 && (open "http://localhost:${PORT}" 2>/dev/null || xdg-open "http://localhost:${PORT}" 2>/dev/null || true)) &
    exec "$PY" -m qabuddy serve
    ;;
esac
