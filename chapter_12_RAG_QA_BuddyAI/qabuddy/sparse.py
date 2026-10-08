"""Code-aware BM25 sparse vectors for the keyword half of hybrid search.

Why not a stock BM25 tokenizer: QA questions are full of identifiers that a
prose tokenizer mangles or misses.

    "loginToVWOLoginValidCreds"  -> loginto... + login, to, vwo, valid, creds
    "VWO-26", "LOGIN-002"        -> kept whole (exact ticket / test id match)
                                    and split (vwo, 26) for partial matches
    "e2e-checkout.spec.ts"       -> whole file name + its parts

Scoring is real BM25, split between client and Qdrant:
  * document side (here): TF saturation with length normalisation
        tf * (k1 + 1) / (tf + k1 * (1 - b + b * len / avg_len))
  * Qdrant multiplies by IDF itself (`modifier=IDF` on the sparse vector), so
    IDF stays correct as the collection grows, with no re-encoding.

Terms are hashed to uint32 indices (md5, stable across processes and
languages, so the JS demo encoder produces identical indices).
"""

from __future__ import annotations

import hashlib
import re
from collections import Counter
from dataclasses import dataclass

from .config import glossary

K1 = 1.2
B = 0.75

_TOKEN = re.compile(r"[A-Za-z0-9]+(?:[._/-][A-Za-z0-9]+)*")
_CAMEL = re.compile(r"[A-Z]+(?=[A-Z][a-z])|[A-Z]?[a-z]+|[A-Z]+|\d+")

STOPWORDS = frozenset(
    """a an and are as at be been but by can could did do does for from had has have how i if in into is it its
    me my no not of on or our so than that the their them then there these they this those to was we were what
    when where which while who whom why will with would you your about after all also any because before being
    between both each few further here just more most other over own same should some such too under until up very
    please show tell give find get explain describe list using use used via
    public private protected static final void return import package const let var new await async function
    export default true false null undefined""".split()
)


def stem(w: str) -> str:
    """A deliberately small English stemmer (plurals, -ing, -ed).

    Porter/Snowball would be marginally better for prose, but this one is
    trivially identical in Python and JavaScript, which keeps the hosted demo
    and the real index in agreement.
    """
    if len(w) <= 3 or not w.isalpha():
        return w
    if w.endswith("ies") and len(w) > 4:
        return w[:-3] + "y"
    if w.endswith(("sses", "shes", "ches", "xes", "zes")):
        return w[:-2]
    if w.endswith("ing") and len(w) > 5:
        w = w[:-3]
        return w[:-1] if len(w) > 3 and w[-1] == w[-2] and w[-1] not in "lsz" else w
    if w.endswith("ed") and len(w) > 4:
        w = w[:-2]
        return w[:-1] if len(w) > 3 and w[-1] == w[-2] and w[-1] not in "lsz" else w
    if w.endswith("s") and not w.endswith(("ss", "us", "is")):
        return w[:-1]
    return w


def terms(text: str) -> list[str]:
    out: list[str] = []
    for m in _TOKEN.finditer(text):
        tok = m.group(0)
        parts = re.split(r"[._/-]", tok)
        if len(parts) > 1 and len(tok) <= 60:
            out.append(tok.lower())  # vwo-26, e2e-checkout.spec.ts, data.properties
        for p in parts:
            subs = _CAMEL.findall(p)
            if len(subs) > 1 and len(p) <= 60:
                out.append(p.lower())  # whole identifier: logintovwologinvalidcreds
            for s in subs:
                s = s.lower()
                if s in STOPWORDS or (len(s) < 2 and not s.isdigit()):
                    continue
                out.append(stem(s))
    return out


def term_index(term: str) -> int:
    return int.from_bytes(hashlib.md5(term.encode()).digest()[:4], "little")


@dataclass
class SparseVec:
    indices: list[int]
    values: list[float]


def encode_document(text: str, avg_len: float) -> tuple[SparseVec, int]:
    tf = Counter(terms(text))
    length = sum(tf.values())
    norm = K1 * (1 - B + B * length / max(avg_len, 1.0))
    weights: dict[int, float] = {}
    for t, f in tf.items():
        i = term_index(t)
        weights[i] = weights.get(i, 0.0) + f * (K1 + 1) / (f + norm)
    idx = sorted(weights)
    return SparseVec(idx, [round(weights[i], 4) for i in idx]), length


def expand_query(text: str) -> list[tuple[str, float]]:
    """Query terms with weights: 1.0 for the user's words, 0.5 for glossary expansions."""
    base = list(dict.fromkeys(terms(text)))
    weighted = {t: 1.0 for t in base}
    lowered = " " + re.sub(r"[^a-z0-9/ ]+", " ", text.lower()) + " "
    for key, expansions in glossary().items():
        if f" {key} " in lowered:
            for phrase in expansions:
                for t in terms(phrase):
                    weighted.setdefault(t, 0.5)
    return list(weighted.items())


def encode_query(text: str) -> tuple[SparseVec, list[tuple[str, float]]]:
    weighted = expand_query(text)
    agg: dict[int, float] = {}
    for t, w in weighted:
        i = term_index(t)
        agg[i] = max(agg.get(i, 0.0), w)
    idx = sorted(agg)
    return SparseVec(idx, [agg[i] for i in idx]), weighted
