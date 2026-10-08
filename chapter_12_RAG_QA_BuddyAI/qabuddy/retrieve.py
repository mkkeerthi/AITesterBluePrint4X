"""Hybrid retrieval: exact ids + dense + BM25 -> RRF -> cross-encoder -> budget.

    question
      ├─ exact id lookup      "VWO-26", "LOGIN-002" are fetched, not searched
      ├─ dense  (Qwen3)       meaning: "sign in broken" ~ "login failure"
      └─ bm25   (code-aware)  exact strings: TimeoutException, WaitHelpers.java
            └─ Qdrant RRF fusion  (top RERANK_CANDIDATES)
                  └─ cross-encoder rerank
                        └─ select: dedupe, per-source cap, relevance floor,
                                   token budget -> FINAL_K sources
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field

from . import rerank, store
from .config import source_by_id, settings
from .embed import embed_query
from .sparse import encode_query
from .text import approx_tokens

RERANK_FLOOR = 0.02  # below this a candidate is noise once two good sources are in
LOW_CONFIDENCE = 0.10  # best rerank score under this: tell the user the evidence is thin

META_KEYS = (
    "tc_id", "module", "priority", "automated", "status", "jira_key", "issue_type", "section", "page_start", "page_end",
    "line_start", "line_end", "symbols", "scope", "language", "path_in_repo", "build", "job", "result", "failed_tests",
    "flaky_tests", "stage", "meeting_date", "speakers", "diagram_title", "doc_type", "url", "repeat_count",
)


@dataclass
class Candidate:
    id: str
    payload: dict
    exact: bool = False
    fused_rank: int | None = None
    rrf: float | None = None
    dense_rank: int | None = None
    dense: float | None = None
    bm25_rank: int | None = None
    bm25: float | None = None
    rerank: float | None = None
    pinned: bool = False  # inventory chunk (repository summary / outline) for a quota source
    selected: bool = False
    reason: str = ""

    def public(self, n: int | None = None, full: bool = False) -> dict:
        p = self.payload
        src = source_by_id(p.get("source_id", ""))
        d = {
            "n": n,
            "id": self.id,
            "source_id": p.get("source_id"),
            "source_label": src.label if src else p.get("source_id"),
            "source_kind": p.get("source_kind"),
            "title": p.get("title"),
            "locator": p.get("locator"),
            "file_path": p.get("file_path"),
            "meta": {k: p[k] for k in META_KEYS if k in p},
            "scores": {
                "exact": self.exact,
                "pinned": self.pinned,
                "dense_rank": self.dense_rank,
                "dense": round(self.dense, 4) if self.dense is not None else None,
                "bm25_rank": self.bm25_rank,
                "bm25": round(self.bm25, 3) if self.bm25 is not None else None,
                "fused_rank": self.fused_rank,
                "rrf": round(self.rrf, 4) if self.rrf is not None else None,
                "rerank": round(self.rerank, 4) if self.rerank is not None else None,
            },
            "selected": self.selected,
            "reason": self.reason,
        }
        if full:
            d["text"] = p.get("text", "")
            d["body"] = p.get("body", "")
        return d


@dataclass
class Retrieval:
    question: str
    search_query: str
    sources: list[Candidate]
    candidates: list[Candidate]
    terms: list[tuple[str, float]]
    exact_ids: list[str]
    source_filter: list[str] | None
    timings: dict = field(default_factory=dict)
    reranked: bool = False
    low_confidence: bool = False

    def public(self) -> dict:
        return {
            "question": self.question,
            "search_query": self.search_query,
            "sources": [c.public(i + 1, full=True) for i, c in enumerate(self.sources)],
            "candidates": [c.public() for c in self.candidates],
            "terms": [{"term": t, "weight": w} for t, w in self.terms[:40]],
            "exact_ids": self.exact_ids,
            "source_filter": self.source_filter,
            "timings": self.timings,
            "reranked": self.reranked,
            "low_confidence": self.low_confidence,
        }


def _overlaps(a: Candidate, b: Candidate) -> bool:
    pa, pb = a.payload, b.payload
    if pa.get("file_path") != pb.get("file_path"):
        return False
    if pa.get("text") == pb.get("text"):
        return True
    la, lb = (pa.get("line_start"), pa.get("line_end")), (pb.get("line_start"), pb.get("line_end"))
    if None in la or None in lb:
        return False
    inter = min(la[1], lb[1]) - max(la[0], lb[0])
    return inter > 0.5 * min(la[1] - la[0] + 1, lb[1] - lb[0] + 1)


def retrieve(
    question: str,
    *,
    source_ids: list[str] | None = None,
    k: int | None = None,
    search_query: str | None = None,
    quotas: dict[str, int] | None = None,
) -> Retrieval:
    s = settings()
    k = k or s.final_k
    query = search_query or question
    quotas = quotas or {}
    t: dict[str, float] = {}

    t0 = time.perf_counter()
    dense = embed_query(query)
    t["embed_ms"] = round((time.perf_counter() - t0) * 1000, 1)

    sparse, weighted = encode_query(query)
    fused_k = max(s.rerank_candidates, k * 3)
    t0 = time.perf_counter()
    res = store.hybrid(dense, sparse, source_ids=source_ids, prefetch_k=s.prefetch_k, fused_k=fused_k)
    ids = store.exact_ids(f"{question} {query}")
    exact = store.by_exact_id(ids, source_ids)
    t["search_ms"] = round((time.perf_counter() - t0) * 1000, 1)

    cands: list[Candidate] = []
    seen: set[str] = set()

    def add(point, **kw) -> None:
        pid = str(point.id)
        if pid in seen:
            for c in cands:
                if c.id == pid:
                    for key, val in kw.items():
                        if val is not None and getattr(c, key) in (None, False):
                            setattr(c, key, val)
            return
        seen.add(pid)
        dr, ds = res["dense"].get(pid, (None, None))
        br, bs = res["sparse"].get(pid, (None, None))
        cands.append(Candidate(pid, point.payload or {}, dense_rank=dr, dense=ds, bm25_rank=br, bm25=bs, **kw))

    for p in exact:
        add(p, exact=True)
    for i, p in enumerate(res["fused"]):
        add(p, fused_rank=i + 1, rrf=p.score)
    pool_size = max(s.rerank_candidates, len(exact))
    head = cands[:pool_size]

    # quota sources get their own filtered search, so their best candidates
    # reach the reranker even when another source dominates the global list
    t0 = time.perf_counter()
    quota_extra: list[Candidate] = []
    head_ids = {c.id for c in head}
    for sid, n in quotas.items():
        have = sum(1 for c in head if c.payload.get("source_id") == sid)
        if have >= n * 2:
            continue
        extra = store.hybrid(dense, sparse, source_ids=[sid], prefetch_k=s.prefetch_k, fused_k=n * 2)
        for p in extra["fused"]:
            add(p)  # no-op if already a candidate further down the fused list
            pid = str(p.id)
            if pid not in head_ids and all(c.id != pid for c in quota_extra):
                quota_extra.append(next(c for c in cands if c.id == pid))
    # corpus-level tasks (gap analysis, RTM) need the inventory of each quota
    # source; similarity search alone never returns "the list of all modules"
    for p in store.summaries(list(quotas)) if quotas else []:
        pid = str(p.id)
        add(p, pinned=True)
        if pid not in head_ids and all(c.id != pid for c in quota_extra):
            quota_extra.append(next(c for c in cands if c.id == pid))
    if quotas:
        t["quota_search_ms"] = round((time.perf_counter() - t0) * 1000, 1)

    pool = head + quota_extra
    t0 = time.perf_counter()
    scores = rerank.score(query, [c.payload.get("text", "")[:2000] for c in pool])
    t["rerank_ms"] = round((time.perf_counter() - t0) * 1000, 1)
    if scores:
        for c, sc in zip(pool, scores):
            c.rerank = sc
        ordered = sorted(pool, key=lambda c: (not c.exact, -(c.rerank or 0.0)))
    else:
        ordered = sorted(cands, key=lambda c: (not c.exact, c.fused_rank or 10**6))

    # selection: exact ids pinned, then best-first with dedupe, a per-source cap
    # (so a 500-row test case CSV cannot crowd out the one PRD section that
    # matters), a relevance floor, and a hard token budget
    per_source_cap = max(2, round(k * 0.6), *quotas.values()) if quotas else max(2, round(k * 0.6))
    budget = s.context_tokens
    used_tokens = 0
    final: list[Candidate] = []
    per_source: dict[str, int] = {}

    def take(c: Candidate, reason: str) -> bool:
        nonlocal used_tokens
        sid = c.payload.get("source_id", "")
        if c.selected:
            return False
        if any(_overlaps(c, f) for f in final):
            c.reason = "duplicate of a selected chunk"
            return False
        cost = min(approx_tokens(c.payload.get("text", "")), 900)
        if final and used_tokens + cost > budget:
            c.reason = "token budget"
            return False
        c.selected, c.reason = True, reason
        final.append(c)
        per_source[sid] = per_source.get(sid, 0) + 1
        used_tokens += cost
        return True

    # 1) exact id matches are always in
    for c in ordered:
        if c.exact and len(final) < k:
            take(c, "exact id match")
    # 2) quotas: the best few from each required source, with no relevance
    #    floor. The cross-encoder scores "Test case LOGIN-001 ..." near zero for
    #    "build an RTM", yet the RTM is impossible without test cases in context.
    for sid, n in quotas.items():
        for c in sorted([c for c in ordered if c.payload.get("source_id") == sid], key=lambda c: not c.pinned):
            if per_source.get(sid, 0) >= n or len(final) >= k:
                break
            take(c, "inventory (pinned)" if c.pinned else f"quota ({sid})")
    # 3) everything else, best first
    for c in ordered:
        sid = c.payload.get("source_id", "")
        if c.selected:
            continue
        if len(final) >= k:
            c.reason = c.reason or "beyond top-k"
            continue
        if scores and (c.rerank or 0) < RERANK_FLOOR and len(final) >= 2:
            c.reason = "below relevance floor"
            continue
        if per_source.get(sid, 0) >= per_source_cap:
            c.reason = f"source cap ({per_source_cap})"
            continue
        take(c, "selected")
    final.sort(key=lambda c: (not c.exact, -(c.rerank or 0.0)) if scores else (not c.exact, c.fused_rank or 10**6))

    t["context_tokens"] = used_tokens
    best = max((c.rerank or 0.0) for c in final) if final and scores else None
    trace = sorted(cands, key=lambda c: (not c.selected, not c.exact, -(c.rerank or 0.0), c.fused_rank or 10**6))
    return Retrieval(
        question=question,
        search_query=query,
        sources=final,
        candidates=trace[: max(fused_k, len(exact))],
        terms=weighted,
        exact_ids=ids,
        source_filter=source_ids,
        timings=t,
        reranked=bool(scores),
        low_confidence=bool(scores) and (best or 0.0) < LOW_CONFIDENCE and not any(c.exact for c in final),
    )
