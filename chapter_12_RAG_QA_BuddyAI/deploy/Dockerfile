# ---- 1. build the web UI ----
FROM node:20-slim AS ui
WORKDIR /ui
COPY ui/package.json ui/package-lock.json ./
RUN npm ci
COPY ui/ ./
RUN npm run build

# ---- 2. API + ingestion (one image, one process) ----
FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1 HF_HOME=/models
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends git curl && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
# CPU-only torch: the reranker runs on the droplet's CPU, and the CUDA build
# would add ~4 GB to the image for nothing
RUN pip install --index-url https://download.pytorch.org/whl/cpu torch \
 && pip install -r requirements.txt
COPY qabuddy/ qabuddy/
COPY sources.yaml glossary.yaml ./
COPY eval/ eval/
COPY --from=ui /ui/dist ui/dist
EXPOSE 8300
HEALTHCHECK --interval=30s --timeout=5s CMD curl -fs localhost:8300/api/health || exit 1
CMD ["python", "-m", "qabuddy", "serve"]
