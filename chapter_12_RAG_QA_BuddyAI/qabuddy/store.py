"""Qdrant: one collection, two named vectors per point.

    dense  1024-d cosine   Qwen3-Embedding (meaning)
    bm25   sparse + IDF    code-aware BM25 (exact identifiers, error strings)

Hybrid search is a single batched request with three queries:
dense-only and bm25-only (so the UI can show where each candidate ranked on
each side) and Qdrant's own prefetch + RRF fusion, which is the result we use.
"""

from __future__ import annotations

import re
from typing import Any

from qdrant_client import QdrantClient, models

from .config import settings
from .models import Chunk
from .sparse import SparseVec

PAYLOAD_INDEXES = {
    "source_id": models.PayloadSchemaType.KEYWORD,
    "source_kind": models.PayloadSchemaType.KEYWORD,
    "file_path": models.PayloadSchemaType.KEYWORD,
    "jira_key": models.PayloadSchemaType.KEYWORD,
    "tc_id": models.PayloadSchemaType.KEYWORD,
    "module": models.PayloadSchemaType.KEYWORD,
    "priority": models.PayloadSchemaType.KEYWORD,
    "job": models.PayloadSchemaType.KEYWORD,
    "build": models.PayloadSchemaType.KEYWORD,
    "failed_tests": models.PayloadSchemaType.KEYWORD,
    "flaky_tests": models.PayloadSchemaType.KEYWORD,
    "symbols": models.PayloadSchemaType.KEYWORD,
    "summary": models.PayloadSchemaType.KEYWORD,
}

_client: QdrantClient | None = None


def client() -> QdrantClient:
    global _client
    if _client is None:
        _client = QdrantClient(
            url=settings().qdrant_url,
            api_key=settings().qdrant_api_key or None,
            timeout=60,
            check_compatibility=False,
        )
    return _client


def collection_exists() -> bool:
    return client().collection_exists(settings().collection)


def create_collection(recreate: bool = False) -> None:
    s, c = settings(), client()
    if recreate and c.collection_exists(s.collection):
        c.delete_collection(s.collection)
    if c.collection_exists(s.collection):
        return
    c.create_collection(
        collection_name=s.collection,
        vectors_config={"dense": models.VectorParams(size=s.embed_dim, distance=models.Distance.COSINE)},
        sparse_vectors_config={"bm25": models.SparseVectorParams(modifier=models.Modifier.IDF)},
    )
    for field, schema in PAYLOAD_INDEXES.items():
        c.create_payload_index(s.collection, field_name=field, field_schema=schema)


def collection_dim() -> int | None:
    try:
        info = client().get_collection(settings().collection)
        vec = info.config.params.vectors
        return vec["dense"].size if isinstance(vec, dict) else None
    except Exception:
        return None


def count(source_id: str | None = None) -> int:
    flt = None
    if source_id:
        flt = models.Filter(must=[models.FieldCondition(key="source_id", match=models.MatchValue(value=source_id))])
    try:
        return client().count(settings().collection, count_filter=flt, exact=True).count
    except Exception:
        return 0


def delete_file(file_path: str) -> None:
    client().delete(
        settings().collection,
        points_selector=models.FilterSelector(
            filter=models.Filter(must=[models.FieldCondition(key="file_path", match=models.MatchValue(value=file_path))])
        ),
        wait=True,
    )


def upsert(chunks: list[Chunk], dense: list[list[float]], sparse: list[SparseVec], batch: int = 64) -> None:
    pts = [
        models.PointStruct(
            id=c.id,
            vector={"dense": d, "bm25": models.SparseVector(indices=sv.indices, values=sv.values)},
            payload=c.payload(),
        )
        for c, d, sv in zip(chunks, dense, sparse)
    ]
    for i in range(0, len(pts), batch):
        client().upsert(settings().collection, points=pts[i: i + batch], wait=True)


def _filter(source_ids: list[str] | None) -> models.Filter | None:
    if not source_ids:
        return None
    return models.Filter(must=[models.FieldCondition(key="source_id", match=models.MatchAny(any=source_ids))])


def hybrid(dense: list[float], sparse: SparseVec, *, source_ids: list[str] | None, prefetch_k: int, fused_k: int) -> dict[str, Any]:
    s = settings()
    flt = _filter(source_ids)
    sv = models.SparseVector(indices=sparse.indices, values=sparse.values)
    reqs = [
        models.QueryRequest(query=dense, using="dense", limit=prefetch_k, filter=flt, with_payload=False),
        models.QueryRequest(query=sv, using="bm25", limit=prefetch_k, filter=flt, with_payload=False),
        models.QueryRequest(
            prefetch=[
                models.Prefetch(query=dense, using="dense", limit=prefetch_k, filter=flt),
                models.Prefetch(query=sv, using="bm25", limit=prefetch_k, filter=flt),
            ],
            query=models.FusionQuery(fusion=models.Fusion.RRF),
            limit=fused_k,
            with_payload=True,
        ),
    ]
    dense_res, sparse_res, fused_res = client().query_batch_points(s.collection, requests=reqs)
    dense_rank = {str(p.id): (i + 1, p.score) for i, p in enumerate(dense_res.points)}
    sparse_rank = {str(p.id): (i + 1, p.score) for i, p in enumerate(sparse_res.points)}
    return {"dense": dense_rank, "sparse": sparse_rank, "fused": fused_res.points}


_ID = re.compile(r"\b[A-Z][A-Z0-9]{1,15}-\d{1,6}\b")


def exact_ids(question: str) -> list[str]:
    return list(dict.fromkeys(_ID.findall(question.upper())))


def by_exact_id(ids: list[str], source_ids: list[str] | None, limit: int = 8) -> list:
    """Ticket keys and test case ids are looked up directly, not searched for."""
    if not ids:
        return []
    must = []
    if source_ids:
        must.append(models.FieldCondition(key="source_id", match=models.MatchAny(any=source_ids)))
    flt = models.Filter(
        must=must,
        should=[
            models.FieldCondition(key="jira_key", match=models.MatchAny(any=ids)),
            models.FieldCondition(key="tc_id", match=models.MatchAny(any=ids)),
        ],
    )
    pts, _ = client().scroll(settings().collection, scroll_filter=flt, limit=limit, with_payload=True)
    return pts


def summaries(source_ids: list[str], limit: int = 12) -> list:
    """Inventory chunks (test repository summary, document outlines) for the given sources."""
    if not source_ids:
        return []
    flt = models.Filter(
        must=[
            models.FieldCondition(key="source_id", match=models.MatchAny(any=source_ids)),
            models.FieldCondition(key="summary", match=models.MatchAny(any=["repository", "outline"])),
        ]
    )
    pts, _ = client().scroll(settings().collection, scroll_filter=flt, limit=limit, with_payload=True)
    return pts


def get(point_id: str) -> dict | None:
    pts = client().retrieve(settings().collection, ids=[point_id], with_payload=True)
    return pts[0].payload if pts else None
