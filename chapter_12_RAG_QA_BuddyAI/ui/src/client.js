// One event contract, two engines.
//
//  live  the Python API: exact ids + Qwen3 dense + BM25 in Qdrant, RRF,
//        cross-encoder rerank, streamed answer from the LLM (SSE)
//  demo  the hosted build: the example questions replay recorded runs of the
//        full pipeline; anything else runs BM25 in the browser and asks a
//        rate-limited serverless function for the answer
//
// Both yield: {type:'status'} -> {type:'retrieval'} -> {type:'token'}* -> {type:'done'}

import { Bm25Index, expandQuery } from './bm25.js';

export const DEMO = Boolean(import.meta.env.VITE_DEMO);

const json = async (url, opts) => {
  const r = await fetch(url, opts);
  const d = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(d.detail || d.error || `HTTP ${r.status}`);
  return d;
};

// ------------------------------------------------------------------ live

async function* sse(res) {
  const reader = res.body.getReader();
  const dec = new TextDecoder();
  let buf = '';
  for (;;) {
    const { value, done } = await reader.read();
    if (done) break;
    buf += dec.decode(value, { stream: true });
    let i;
    while ((i = buf.indexOf('\n\n')) >= 0) {
      const raw = buf.slice(0, i);
      buf = buf.slice(i + 2);
      const line = raw.split('\n').find((l) => l.startsWith('data:'));
      if (line) yield JSON.parse(line.slice(5));
    }
  }
}

const live = {
  health: () => json('/api/health'),
  sources: () => json('/api/sources'),
  modes: () => json('/api/modes'),
  chunk: (id) => json(`/api/chunk/${id}`),
  ingest: (body) => json('/api/ingest', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) }),
  ingestStatus: () => json('/api/ingest/status'),
  async *chat({ question, mode, sources, history, signal }) {
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question, mode, sources, history }),
      signal,
    });
    if (!res.ok) {
      const d = await res.json().catch(() => ({}));
      throw new Error(d.detail || `HTTP ${res.status}`);
    }
    yield* sse(res);
  },
};

// ------------------------------------------------------------------ demo

let demoData = null;
let corpus = null;
let index = null;

const loadDemo = async () => (demoData ??= await json('/demo/demo.json'));
const loadCorpus = async () => {
  if (!corpus) {
    corpus = await json('/demo/corpus.json');
    index = new Bm25Index(corpus);
  }
  return corpus;
};

export const keyOf = (q, mode) => `${mode}::${q.trim().toLowerCase().replace(/\s+/g, ' ').replace(/[?.!]+$/, '')}`;
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const CITE = /\[(\d{1,2})\]/g; // code is stripped first, so word[1] is a citation
export function citationsOf(answer, n) {
  const prose = answer.replace(/```[\s\S]*?```|`[^`\n]*`/g, ' ');
  const found = [...prose.matchAll(CITE)].map((m) => Number(m[1]));
  const used = [...new Set(found.filter((x) => x >= 1 && x <= n))].sort((a, b) => a - b);
  const notFound = /couldn't find|could not find/i.test(answer);
  return { used, invalid: [...new Set(found.filter((x) => x < 1 || x > n))], grounded: used.length > 0 || notFound, said_not_found: notFound };
}

async function* replay(rec, signal) {
  yield { type: 'status', message: 'Replaying a recorded run of the full pipeline' };
  await sleep(250);
  yield { ...rec.retrieval_event, recorded: rec.recorded_at };
  const text = rec.done.answer || '';
  const step = Math.max(6, Math.round(text.length / 160));
  for (let i = 0; i < text.length; i += step) {
    if (signal?.aborted) return;
    yield { type: 'token', text: text.slice(i, i + step) };
    await sleep(14);
  }
  yield { ...rec.done, type: 'done', recorded: rec.recorded_at };
}

function demoRetrieval(question, mode, sourceIds, glossary, k) {
  const sources = sourceIds?.length ? sourceIds : mode.sources;
  const weighted = expandQuery(question, glossary);
  const hits = index.search(weighted, { sourceIds: sources, limit: 40 });
  const ids = [...new Set((question.toUpperCase().match(/\b[A-Z][A-Z0-9]{1,15}-\d{1,6}\b/g) || []))];
  const exact = corpus.filter(
    (c) => (!sources || sources.includes(c.source_id)) && (ids.includes(c.meta?.jira_key) || ids.includes(c.meta?.tc_id))
  );
  const pinned = Object.keys(mode.quotas || {}).length
    ? corpus.filter((c) => Object.keys(mode.quotas).includes(c.source_id) && ['repository', 'outline'].includes(c.meta?.summary))
    : [];
  const order = [...exact.map((c) => ({ chunk: c, exact: true })), ...pinned.map((c) => ({ chunk: c, pinned: true })), ...hits];
  const seen = new Set();
  const perSource = {};
  const cap = Math.max(2, Math.round(k * 0.6));
  const final = [];
  const candidates = [];
  hits.forEach((h, i) => (h.rank = i + 1));
  for (const h of order) {
    if (seen.has(h.chunk.id)) continue;
    seen.add(h.chunk.id);
    const sid = h.chunk.source_id;
    let reason = 'selected';
    if (final.length >= k) reason = 'beyond top-k';
    else if (!h.exact && !h.pinned && (perSource[sid] || 0) >= cap) reason = `source cap (${cap})`;
    const selected = reason === 'selected';
    const view = {
      id: h.chunk.id,
      source_id: sid,
      source_label: h.chunk.source_label,
      source_kind: h.chunk.source_kind,
      title: h.chunk.title,
      locator: h.chunk.locator,
      file_path: h.chunk.file_path,
      meta: h.chunk.meta || {},
      scores: { exact: !!h.exact, pinned: !!h.pinned, bm25_rank: h.rank ?? null, bm25: h.score ? +h.score.toFixed(3) : null },
      selected,
      reason: selected ? (h.exact ? 'exact id match' : h.pinned ? 'inventory (pinned)' : 'selected') : reason,
    };
    candidates.push(view);
    if (selected) {
      perSource[sid] = (perSource[sid] || 0) + 1;
      final.push({ ...view, n: final.length + 1, text: h.chunk.text, body: h.chunk.body });
    }
  }
  return {
    question,
    search_query: question,
    sources: final,
    candidates: candidates.slice(0, 30),
    terms: weighted.map(([term, weight]) => ({ term, weight })),
    exact_ids: ids,
    source_filter: sources,
    timings: {},
    reranked: false,
    low_confidence: final.length === 0,
    demo_engine: 'bm25-browser',
  };
}

const demo = {
  async health() {
    return (await loadDemo()).health;
  },
  async sources() {
    return (await loadDemo()).sources;
  },
  async modes() {
    return (await loadDemo()).modes;
  },
  async chunk(id) {
    const c = (await loadCorpus()).find((x) => x.id === id);
    if (!c) throw new Error('Chunk not in the demo corpus.');
    return { ...c, ...(c.meta || {}) };
  },
  ingest: async () => {
    throw new Error('Ingestion is disabled in the hosted demo. Run QABuddy locally to index your own data.');
  },
  ingestStatus: async () => ({ running: false, stage: 'idle' }),
  async *chat({ question, mode: modeId, sources, history, signal }) {
    const d = await loadDemo();
    const rec = d.recorded[keyOf(question, modeId)];
    if (rec && !history?.length) {
      yield* replay(rec, signal);
      return;
    }
    yield { type: 'status', message: 'Searching the demo corpus (BM25 in your browser)' };
    await loadCorpus();
    const mode = d.modes.find((m) => m.id === modeId) || d.modes[0];
    const t0 = performance.now();
    const retrieval = demoRetrieval(question, mode, sources, d.glossary, mode.k);
    retrieval.timings.search_ms = +(performance.now() - t0).toFixed(1);
    yield { type: 'retrieval', mode, retrieval };
    if (!retrieval.sources.length) {
      const msg = "I couldn't find anything relevant in the demo corpus. Try one of the example questions.";
      yield { type: 'token', text: msg };
      yield { type: 'done', answer: msg, citations: citationsOf(msg, 0), usage: {}, timings: retrieval.timings };
      return;
    }
    const t1 = performance.now();
    const r = await fetch('/api/demo-chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      signal,
      body: JSON.stringify({
        question,
        mode: modeId,
        sources: retrieval.sources.map((s) => ({ n: s.n, title: s.title, source_id: s.source_id, file_path: s.file_path, locator: s.locator, text: s.text })),
      }),
    });
    const out = await r.json().catch(() => ({}));
    if (!r.ok) throw new Error(out.error || `HTTP ${r.status}`);
    const text = out.answer || '';
    for (let i = 0; i < text.length; i += 24) {
      yield { type: 'token', text: text.slice(i, i + 24) };
      await sleep(8);
    }
    yield {
      type: 'done',
      answer: text,
      citations: citationsOf(text, retrieval.sources.length),
      usage: out.usage || {},
      model: out.model,
      timings: { ...retrieval.timings, llm_ms: +(performance.now() - t1).toFixed(1) },
    };
  },
};

export const api = DEMO ? demo : live;
export const demoMeta = async () => (DEMO ? loadDemo() : null);
