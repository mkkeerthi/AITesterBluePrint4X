import React from 'react';
import { kindOf } from '../kinds.js';

const ms = (v) => (v == null ? '-' : v >= 1000 ? `${(v / 1000).toFixed(2)}s` : `${Math.round(v)}ms`);

export default function Trace({ retrieval, done, onOpen }) {
  const r = retrieval;
  const t = { ...(r.timings || {}), ...(done?.timings || {}) };
  const u = done?.usage || {};
  const stats = [
    ['Embed (Qwen3)', ms(t.embed_ms)],
    ['Qdrant hybrid', ms(t.search_ms)],
    ['Rerank', r.reranked ? ms(t.rerank_ms) : 'off'],
    ['LLM first token', ms(t.llm_first_token_ms)],
    ...(t.rate_limit_wait_ms ? [['Rate-limit wait', ms(t.rate_limit_wait_ms)]] : []),
    ['Total', ms(t.total_ms ?? t.llm_ms)],
    ['Context tokens', t.context_tokens ?? '-'],
    ['Prompt / completion', u.prompt_tokens ? `${u.prompt_tokens} / ${u.completion_tokens}` : '-'],
  ];
  return (
    <div className="trace">
      <h4>How this answer was found</h4>
      {r.demo_engine === 'bm25-browser' && (
        <p className="note">
          Demo engine: keyword (BM25) search running in your browser over the {r.candidates.length ? '' : 'demo '}corpus. The full
          deployment adds Qwen3 dense vectors, Qdrant RRF fusion and a cross-encoder rerank; the example questions replay
          recorded runs of that full pipeline.
        </p>
      )}
      {r.search_query && r.search_query !== r.question && (
        <p className="note">
          Follow-up rewritten as a standalone search query: <b>{r.search_query}</b>
        </p>
      )}
      <div className="trace-grid">
        {stats.map(([l, n]) => (
          <div className="stat" key={l}>
            <div className="n">{n}</div>
            <div className="l">{l}</div>
          </div>
        ))}
      </div>
      {r.terms?.length > 0 && (
        <>
          <h4>Keyword terms (BM25){r.terms.some((x) => x.weight < 1) ? ' · highlighted = glossary expansion' : ''}</h4>
          <div className="terms">
            {r.terms.map((x) => (
              <span key={x.term} className={`term ${x.weight < 1 ? 'exp' : ''}`}>
                {x.term}
              </span>
            ))}
          </div>
        </>
      )}
      {r.exact_ids?.length > 0 && <p className="note">Exact id lookup: {r.exact_ids.join(', ')}</p>}
      <h4>Candidates ({r.candidates.length}) and why each was kept or dropped</h4>
      <div className="tbl-wrap">
        <table className="tr">
          <thead>
            <tr>
              <th>Source</th>
              <th>Title</th>
              <th>Dense #</th>
              <th>BM25 #</th>
              <th>RRF #</th>
              <th>Rerank</th>
              <th>Decision</th>
            </tr>
          </thead>
          <tbody>
            {r.candidates.map((c) => {
              const k = kindOf(c.source_kind);
              const s = c.scores || {};
              return (
                <tr key={c.id} className={c.selected ? 'sel' : ''}>
                  <td>
                    <span className="kind" style={{ color: k.color, background: k.bg }}>
                      {k.icon} {c.source_label}
                    </span>
                  </td>
                  <td className="t" title={c.title} onClick={() => onOpen(c)}>
                    {s.exact ? '🎯 ' : s.pinned ? '📌 ' : ''}
                    {c.title}
                  </td>
                  <td className="mono">{s.dense_rank ?? '-'}</td>
                  <td className="mono">{s.bm25_rank ?? '-'}</td>
                  <td className="mono">{s.fused_rank ?? '-'}</td>
                  <td className="mono">{s.rerank != null ? s.rerank.toFixed(3) : '-'}</td>
                  <td>
                    <span className={`why ${c.selected ? 'sel' : ''}`}>{c.reason || '-'}</span>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
