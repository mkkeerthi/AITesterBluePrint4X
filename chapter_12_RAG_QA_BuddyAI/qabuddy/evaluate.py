"""Retrieval evaluation with ablations: what does each component buy?

For every case in eval/golden.yaml, four retrievers are compared at the
same k:

    dense       Qwen3 vectors only
    bm25        code-aware BM25 only
    hybrid      Qdrant RRF fusion of both (no reranker)
    full        exact ids + hybrid + cross-encoder + selection (production)

hit@k  = share of questions with at least one expected source in the top k
MRR    = mean of 1/rank of the first expected source (0 when missing)
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import yaml
from qdrant_client import models

from . import store
from .config import ROOT, settings
from .embed import embed_query
from .retrieve import retrieve
from .sparse import encode_query


def _match(payload: dict, exp: dict) -> bool:
    if "title" in exp and exp["title"].lower() not in (payload.get("title") or "").lower():
        return False
    if "file" in exp and exp["file"].lower() not in (payload.get("file_path") or "").lower():
        return False
    if "source" in exp and exp["source"] != payload.get("source_id"):
        return False
    return True


def _first_hit(payloads: list[dict], expect: list[dict]) -> int | None:
    for rank, p in enumerate(payloads, start=1):
        if any(_match(p, e) for e in expect):
            return rank
    return None


def run(path: Path | None = None) -> int:
    spec = yaml.safe_load((path or ROOT / "eval" / "golden.yaml").read_text())
    k = spec.get("k", 6)
    s = settings()
    names = ("dense", "bm25", "hybrid", "full")
    results = {n: [] for n in names}
    rows = []
    t0 = time.perf_counter()
    for case in spec["cases"]:
        q, expect = case["q"], case["expect"]
        dv = embed_query(q)
        sv, _ = encode_query(q)
        svec = models.SparseVector(indices=sv.indices, values=sv.values)
        c = store.client()
        dense = [p.payload for p in c.query_points(s.collection, query=dv, using="dense", limit=k, with_payload=True).points]
        bm25 = [p.payload for p in c.query_points(s.collection, query=svec, using="bm25", limit=k, with_payload=True).points]
        hybrid = [
            p.payload
            for p in c.query_points(
                s.collection,
                prefetch=[models.Prefetch(query=dv, using="dense", limit=s.prefetch_k), models.Prefetch(query=svec, using="bm25", limit=s.prefetch_k)],
                query=models.FusionQuery(fusion=models.Fusion.RRF),
                limit=k,
                with_payload=True,
            ).points
        ]
        full = [cand.payload for cand in retrieve(q, k=k).sources]
        row = {"q": q}
        for n, payloads in zip(names, (dense, bm25, hybrid, full)):
            r = _first_hit(payloads, expect)
            results[n].append(r)
            row[n] = r
        rows.append(row)

    def hit(n): return sum(1 for r in results[n] if r) / len(results[n])
    def mrr(n): return sum(1 / r for r in results[n] if r) / len(results[n])

    print(f"\n{'question':62s} " + " ".join(f"{n:>7s}" for n in names))
    for row in rows:
        cells = " ".join(f"{('#' + str(row[n])) if row[n] else 'miss':>7s}" for n in names)
        print(f"{row['q'][:62]:62s} {cells}")
    print("\n" + f"{'hit@' + str(k):62s} " + " ".join(f"{hit(n):7.0%}" for n in names))
    print(f"{'MRR':62s} " + " ".join(f"{mrr(n):7.2f}" for n in names))
    print(f"\n{len(rows)} questions in {time.perf_counter() - t0:.1f}s")
    out = {n: {"hit": round(hit(n), 3), "mrr": round(mrr(n), 3)} for n in names}
    (ROOT / "eval" / "last_run.json").write_text(json.dumps({"k": k, "summary": out, "rows": rows}, indent=1))
    return 0 if hit("full") >= 0.9 else 1
