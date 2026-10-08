// Code-aware BM25 in the browser, for the hosted demo's free-text questions.
// A line-for-line port of qabuddy/sparse.py: same tokenizer, same light
// stemmer, same glossary expansion, same BM25 formula. The real deployment
// adds Qwen3 dense vectors and a cross-encoder on top of this; the demo can
// only run the keyword half, because a 4B embedding model does not fit in a
// browser tab.

const TOKEN = /[A-Za-z0-9]+(?:[._/-][A-Za-z0-9]+)*/g;
const CAMEL = /[A-Z]+(?=[A-Z][a-z])|[A-Z]?[a-z]+|[A-Z]+|\d+/g;
const K1 = 1.2;
const B = 0.75;

const STOP = new Set(
  `a an and are as at be been but by can could did do does for from had has have how i if in into is it its
  me my no not of on or our so than that the their them then there these they this those to was we were what
  when where which while who whom why will with would you your about after all also any because before being
  between both each few further here just more most other over own same should some such too under until up very
  please show tell give find get explain describe list using use used via
  public private protected static final void return import package const let var new await async function
  export default true false null undefined`.split(/\s+/)
);

export function stem(w) {
  if (w.length <= 3 || !/^[a-z]+$/.test(w)) return w;
  if (w.endsWith('ies') && w.length > 4) return w.slice(0, -3) + 'y';
  if (['sses', 'shes', 'ches', 'xes', 'zes'].some((s) => w.endsWith(s))) return w.slice(0, -2);
  const undouble = (x) => (x.length > 3 && x.at(-1) === x.at(-2) && !'lsz'.includes(x.at(-1)) ? x.slice(0, -1) : x);
  if (w.endsWith('ing') && w.length > 5) return undouble(w.slice(0, -3));
  if (w.endsWith('ed') && w.length > 4) return undouble(w.slice(0, -2));
  if (w.endsWith('s') && !['ss', 'us', 'is'].some((s) => w.endsWith(s))) return w.slice(0, -1);
  return w;
}

export function terms(text) {
  const out = [];
  for (const m of text.matchAll(TOKEN)) {
    const tok = m[0];
    const parts = tok.split(/[._/-]/);
    if (parts.length > 1 && tok.length <= 60) out.push(tok.toLowerCase());
    for (const p of parts) {
      const subs = p.match(CAMEL) || [];
      if (subs.length > 1 && p.length <= 60) out.push(p.toLowerCase());
      for (let s of subs) {
        s = s.toLowerCase();
        if (STOP.has(s) || (s.length < 2 && !/^\d+$/.test(s))) continue;
        out.push(stem(s));
      }
    }
  }
  return out;
}

export function expandQuery(text, glossary) {
  const weighted = new Map();
  for (const t of terms(text)) weighted.set(t, 1.0);
  const lowered = ' ' + text.toLowerCase().replace(/[^a-z0-9/ ]+/g, ' ') + ' ';
  for (const [key, phrases] of Object.entries(glossary || {})) {
    if (lowered.includes(` ${key} `)) {
      for (const ph of phrases) for (const t of terms(ph)) if (!weighted.has(t)) weighted.set(t, 0.5);
    }
  }
  return [...weighted.entries()];
}

export class Bm25Index {
  constructor(chunks) {
    this.docs = chunks.map((c) => {
      const tf = new Map();
      const ts = terms(c.text || '');
      for (const t of ts) tf.set(t, (tf.get(t) || 0) + 1);
      return { chunk: c, tf, len: ts.length };
    });
    this.df = new Map();
    for (const d of this.docs) for (const t of d.tf.keys()) this.df.set(t, (this.df.get(t) || 0) + 1);
    this.avg = this.docs.reduce((a, d) => a + d.len, 0) / Math.max(1, this.docs.length);
  }

  idf(t) {
    const n = this.docs.length;
    const df = this.df.get(t) || 0;
    return Math.log(1 + (n - df + 0.5) / (df + 0.5));
  }

  search(weighted, { sourceIds = null, limit = 40 } = {}) {
    const scored = [];
    for (const d of this.docs) {
      if (sourceIds && !sourceIds.includes(d.chunk.source_id)) continue;
      let s = 0;
      for (const [t, w] of weighted) {
        const f = d.tf.get(t);
        if (!f) continue;
        s += w * this.idf(t) * ((f * (K1 + 1)) / (f + K1 * (1 - B + (B * d.len) / this.avg)));
      }
      if (s > 0) scored.push({ chunk: d.chunk, score: s });
    }
    return scored.sort((a, b) => b.score - a.score).slice(0, limit);
  }
}
