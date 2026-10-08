"""Dense embeddings: Qwen3-Embedding served by Ollama.

* Default model is qwen3-embedding:0.6b, which is 1024-d natively, so the
  default EMBED_DIM (1024) needs no truncation. Ollama's `dimensions`
  parameter still sets the width, so any Matryoshka width works the same way
  (the 4B model is 2560-d natively and gets truncated instead).
* Qwen3-Embedding is instruction-aware: queries get a task instruction,
  documents do not. Skipping the instruction costs a few points of recall.
"""

from __future__ import annotations

import math
import time

import httpx

from .config import settings

QUERY_INSTRUCTION = (
    "Given a QA engineer's question, retrieve the test cases, source code, bug tickets, "
    "requirement sections, meeting notes, diagrams or CI logs that answer it"
)


class EmbedError(RuntimeError):
    pass


def _normalize(v: list[float]) -> list[float]:
    n = math.sqrt(sum(x * x for x in v)) or 1.0
    return [x / n for x in v]


def _post(inputs: list[str]) -> list[list[float]]:
    s = settings()
    body = {"model": s.embed_model, "input": inputs, "dimensions": s.embed_dim, "truncate": True, "keep_alive": "30m"}
    last: Exception | None = None
    for attempt in range(3):
        try:
            r = httpx.post(f"{s.ollama_url}/api/embed", json=body, timeout=300)
            if r.status_code == 404 or "not found" in r.text[:200].lower():
                raise EmbedError(f"Embedding model '{s.embed_model}' is not pulled. Run: ollama pull {s.embed_model}")
            r.raise_for_status()
            vecs = r.json()["embeddings"]
            return [_normalize(v[: s.embed_dim]) for v in vecs]
        except EmbedError:
            raise
        except httpx.ConnectError as e:
            raise EmbedError(f"Ollama is not reachable at {s.ollama_url}. Start it with `ollama serve`.") from e
        except Exception as e:  # transient: model loading, timeouts
            last = e
            time.sleep(1.5 * (attempt + 1))
    raise EmbedError(f"Embedding failed after retries: {last}")


def embed_documents(texts: list[str], batch_size: int = 32, max_batch_chars: int = 60_000, progress=None) -> list[list[float]]:
    out: list[list[float]] = []
    batch: list[str] = []
    chars = 0
    for t in texts:
        if batch and (len(batch) >= batch_size or chars + len(t) > max_batch_chars):
            out.extend(_post(batch))
            if progress:
                progress(len(out))
            batch, chars = [], 0
        batch.append(t)
        chars += len(t)
    if batch:
        out.extend(_post(batch))
        if progress:
            progress(len(out))
    return out


def embed_query(question: str) -> list[float]:
    return _post([f"Instruct: {QUERY_INSTRUCTION}\nQuery: {question}"])[0]
