import React, { useState } from 'react';
import Answer from './Answer.jsx';
import Trace from './Trace.jsx';
import { kindOf } from '../kinds.js';

const ms = (v) => (v == null ? null : v >= 1000 ? `${(v / 1000).toFixed(1)}s` : `${Math.round(v)}ms`);

export default function Message({ msg, onOpen }) {
  const [trace, setTrace] = useState(false);
  const r = msg.retrieval;
  const sources = r?.sources || [];
  const done = msg.done;
  const used = new Set(done?.citations?.used || []);
  const t = { ...(r?.timings || {}), ...(done?.timings || {}) };
  const u = done?.usage || {};

  return (
    <>
      <div className="q">
        <small>
          {msg.modeIcon} {msg.modeLabel}
        </small>
        {msg.question}
      </div>
      <div className="a">
        <div className="a-head">
          <b>QABuddy</b>
          {msg.streaming && (
            <span className="badge info" style={{ display: 'inline-flex', gap: 6, alignItems: 'center' }}>
              <span className="spinner" /> {msg.status || 'Working'}
            </span>
          )}
          {done?.citations?.grounded && !done.citations.said_not_found && <span className="badge ok">✓ grounded · {used.size} source{used.size === 1 ? '' : 's'} cited</span>}
          {done?.citations?.said_not_found && <span className="badge warn">Not in the knowledge base</span>}
          {done && !done.citations?.grounded && <span className="badge bad">⚠ no citations, verify before trusting</span>}
          {r?.low_confidence && <span className="badge warn">thin evidence</span>}
          {msg.recorded && <span className="badge info">recorded run · full pipeline</span>}
          {r?.demo_engine && <span className="badge info">demo · BM25 in browser</span>}
        </div>
        <div className="a-body">
          {msg.error && <div className="err">{msg.error}</div>}
          {!msg.text && msg.streaming && (
            <div className="status">
              <span className="spinner" />
              {r ? `Found ${sources.length} sources. Writing the answer…` : msg.status || 'Searching…'}
            </div>
          )}
          {msg.text && <Answer text={msg.text} sources={sources} onOpen={onOpen} />}
          {msg.streaming && msg.text && <span className="caret" />}
        </div>
        {sources.length > 0 && (
          <div className="a-sources">
            <h4>Sources ({sources.length})</h4>
            <div className="cards">
              {sources.map((s) => {
                const k = kindOf(s.source_kind);
                const score = s.scores?.rerank;
                return (
                  <button key={s.id} className={`card ${used.has(s.n) ? 'cited' : ''}`} onClick={() => onOpen(s)} title={s.title}>
                    <div className="ct">
                      <span className="num" style={{ color: k.color, borderColor: `${k.color}66`, background: k.bg }}>
                        {s.n}
                      </span>
                      <span>
                        {k.icon} {s.source_label}
                      </span>
                      {s.scores?.exact && <span title="exact id match">🎯</span>}
                      {s.scores?.pinned && <span title="inventory chunk">📌</span>}
                    </div>
                    <div className="tt">{s.title}</div>
                    <div className="lc">{s.locator}</div>
                    {score != null && (
                      <div className="bar" title={`rerank ${score.toFixed(3)}`}>
                        <i style={{ width: `${Math.max(3, score * 100)}%` }} />
                      </div>
                    )}
                  </button>
                );
              })}
            </div>
          </div>
        )}
        {(done || r) && (
          <div className="a-foot">
            {ms(t.total_ms) && (
              <span>
                total <b>{ms(t.total_ms)}</b>
              </span>
            )}
            {ms(t.rerank_ms) && r?.reranked && (
              <span>
                rerank <b>{ms(t.rerank_ms)}</b>
              </span>
            )}
            {ms(t.llm_first_token_ms) && (
              <span>
                first token <b>{ms(t.llm_first_token_ms)}</b>
              </span>
            )}
            {t.rate_limit_wait_ms && (
              <span title="Time spent queued behind the LLM provider's rate limit, not model latency">
                rate-limit wait <b>{ms(t.rate_limit_wait_ms)}</b>
              </span>
            )}
            {u.prompt_tokens && (
              <span>
                tokens <b>{u.prompt_tokens}</b> in / <b>{u.completion_tokens}</b> out
              </span>
            )}
            {done?.model && <span>{done.model}</span>}
            <span className="spacer" />
            {r && (
              <button className="ghost" onClick={() => setTrace(!trace)}>
                {trace ? 'Hide trace' : 'How was this found?'}
              </button>
            )}
          </div>
        )}
        {trace && r && <Trace retrieval={r} done={done} onOpen={onOpen} />}
      </div>
    </>
  );
}
