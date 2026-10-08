"""Cross-encoder reranking (ms-marco-MiniLM-L-6-v2 by default).

Hybrid search is good at recall; a cross-encoder is good at precision. It
reads the question and each candidate together, so it can tell that
"why did login fail on CI" is answered by the IP-allowlist comment, not by
the 40 test cases that merely contain the word "login".

Ollama has no rerank endpoint, so this runs in-process via
sentence-transformers (MPS on Apple Silicon, CUDA or CPU elsewhere).
"""

from __future__ import annotations

import math
import threading
import time

from .config import settings

_model = None
_lock = threading.Lock()
_load_error: str | None = None


def _device() -> str:
    try:
        import torch

        if torch.cuda.is_available():
            return "cuda"
        if torch.backends.mps.is_available():
            return "mps"
    except Exception:
        pass
    return "cpu"


def load():
    global _model, _load_error
    if not settings().rerank_enabled:
        return None
    with _lock:
        if _model is None and _load_error is None:
            try:
                from sentence_transformers import CrossEncoder

                t0 = time.perf_counter()
                _model = CrossEncoder(settings().rerank_model, max_length=512, device=_device())
                if _device() in {"mps", "cuda"}:
                    _model.model.half()  # ~1.4s -> ~1.0s for 24 candidates on an M3 Max, same ranking
                _model.predict([("warm up", "warm up")])
                print(f"[rerank] {settings().rerank_model} loaded on {_device()} in {time.perf_counter() - t0:.1f}s")
            except Exception as e:  # reranking is an enhancement: retrieval still works without it
                _load_error = str(e)
                print(f"[rerank] disabled: {e}")
    return _model


def status() -> dict:
    return {
        "enabled": settings().rerank_enabled,
        "model": settings().rerank_model,
        "loaded": _model is not None,
        "device": _device() if _model is not None else None,
        "error": _load_error,
    }


def score(question: str, texts: list[str]) -> list[float] | None:
    model = load()
    if model is None or not texts:
        return None
    raw = model.predict([(question, t) for t in texts], batch_size=16, show_progress_bar=False)
    out = []
    for x in raw:
        x = float(x)
        out.append(x if 0.0 <= x <= 1.0 else 1 / (1 + math.exp(-x)))
    return out
