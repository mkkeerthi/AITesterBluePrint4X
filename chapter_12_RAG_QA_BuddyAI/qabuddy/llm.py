"""Answer LLM: any OpenAI-compatible chat endpoint (Groq by default).

The embedding model and the Qdrant vector DB are the open-source half of the
system, run locally or as managed services. The answer LLM is pluggable: Groq
for speed, Ollama for a fully
offline deployment, or OpenAI. Only the retrieved sources are ever sent.
"""

from __future__ import annotations

import json
import re
import time
from typing import Iterator

import httpx

from .config import settings


def _endpoint() -> tuple[str, dict[str, str]]:
    s = settings()
    if s.llm_provider == "groq":
        return "https://api.groq.com/openai/v1", {"Authorization": f"Bearer {s.groq_api_key}"}
    if s.llm_provider == "ollama":
        return f"{s.ollama_url}/v1", {}
    return s.openai_base_url.rstrip("/"), {"Authorization": f"Bearer {s.openai_api_key}"}


def configured() -> bool:
    s = settings()
    if s.llm_provider == "groq":
        return bool(s.groq_api_key)
    if s.llm_provider == "openai":
        return bool(s.openai_api_key)
    return True


def _body(messages: list[dict], max_tokens: int, stream: bool) -> dict:
    s = settings()
    body = {"model": s.llm_model, "messages": messages, "temperature": 0.1, "max_tokens": max_tokens, "stream": stream}
    if "gpt-oss" in s.llm_model:
        body["reasoning_effort"] = "low"  # gpt-oss reasons before answering; low keeps tokens and latency down
    if stream:
        body["stream_options"] = {"include_usage": True}
    return body


MAX_RETRIES = 4
MAX_WAIT_S = 30.0


def _retry_after(r: httpx.Response) -> float:
    """Seconds to wait after a 429. Groq says "Please try again in 14.835s"."""
    m = re.search(r"try again in ([\d.]+)\s*(ms|s)", r.text)
    if m:
        secs = float(m.group(1)) / (1000 if m.group(2) == "ms" else 1)
    else:
        secs = float(r.headers.get("retry-after", 5) or 5)
    return min(MAX_WAIT_S, secs + 0.5)


def complete(messages: list[dict], max_tokens: int = 300) -> tuple[str, dict]:
    base, headers = _endpoint()
    for attempt in range(MAX_RETRIES + 1):
        r = httpx.post(f"{base}/chat/completions", headers=headers, json=_body(messages, max_tokens, False), timeout=60)
        if r.status_code == 429 and attempt < MAX_RETRIES:
            time.sleep(_retry_after(r))
            continue
        if r.status_code >= 400:
            raise RuntimeError(f"LLM error {r.status_code}: {r.text[:300]}")
        d = r.json()
        return (d["choices"][0]["message"].get("content") or "").strip(), d.get("usage", {})
    raise RuntimeError("LLM rate limit: retries exhausted")


def stream(messages: list[dict], max_tokens: int = 1200) -> Iterator[tuple[str | None, dict | None]]:
    """Yields (text_delta, usage); usage is set only on the final event.

    On a rate limit (429) it yields (None, {"rate_limited_s": n}), waits, and
    retries. Groq counts the max_tokens *reservation* against tokens-per-minute,
    so on the on-demand tier a few large answers in a minute trip the limit.
    """
    base, headers = _endpoint()
    for attempt in range(MAX_RETRIES + 1):
        with httpx.stream(
            "POST", f"{base}/chat/completions", headers=headers, json=_body(messages, max_tokens, True), timeout=120
        ) as r:
            if r.status_code == 429 and attempt < MAX_RETRIES:
                r.read()
                wait = _retry_after(r)
                yield None, {"rate_limited_s": round(wait, 1)}
                time.sleep(wait)
                continue
            if r.status_code >= 400:
                r.read()
                raise RuntimeError(f"LLM error {r.status_code}: {r.text[:300]}")
            yield from _consume(r)
            return
    raise RuntimeError("LLM rate limit: retries exhausted")


def _consume(r: httpx.Response) -> Iterator[tuple[str, dict | None]]:
    usage: dict | None = None
    for line in r.iter_lines():
        if not line.startswith("data:"):
            continue
        data = line[5:].strip()
        if data == "[DONE]":
            break
        try:
            evt = json.loads(data)
        except json.JSONDecodeError:
            continue
        u = evt.get("usage") or (evt.get("x_groq") or {}).get("usage")
        if u:
            usage = u
        for ch in evt.get("choices") or []:
            delta = (ch.get("delta") or {}).get("content")
            if delta:
                yield delta, None
    yield "", usage or {}
