import React, { useEffect, useMemo, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import hljs from 'highlight.js/lib/common';
import { api } from '../client.js';
import { kindOf } from '../kinds.js';

const LANG = { java: 'java', typescript: 'typescript', tsx: 'typescript', javascript: 'javascript', xml: 'xml', json: 'json', yml: 'yaml', yaml: 'yaml', properties: 'ini', sh: 'bash', py: 'python' };

const SHOW = [
  ['tc_id', 'Test case'], ['module', 'Module'], ['priority', 'Priority'], ['automated', 'Automated'], ['status', 'Status'],
  ['jira_key', 'Ticket'], ['issue_type', 'Type'], ['section', 'Section'], ['doc_type', 'Doc type'], ['page_start', 'Page'],
  ['scope', 'Scope'], ['symbols', 'Defines'], ['language', 'Language'], ['line_start', 'From line'], ['line_end', 'To line'],
  ['job', 'Job'], ['build', 'Build'], ['result', 'Result'], ['stage', 'Stage'], ['failed_tests', 'Failed tests'],
  ['flaky_tests', 'Flaky tests'], ['repeat_count', 'Seen'], ['meeting_date', 'Meeting date'], ['speakers', 'Speakers'],
  ['diagram_title', 'Diagram'],
];

const fmt = (v) => (Array.isArray(v) ? v.join(', ') : String(v));

function Code({ body, language, start }) {
  const html = useMemo(() => {
    const lang = LANG[language];
    try {
      return lang && hljs.getLanguage(lang) ? hljs.highlight(body, { language: lang }).value : hljs.highlightAuto(body).value;
    } catch {
      return body.replace(/[&<>]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' })[c]);
    }
  }, [body, language]);
  const lines = html.split('\n');
  return (
    <div className="codebox">
      <table>
        <tbody>
          {lines.map((l, i) => (
            <tr key={i}>
              <td className="ln">{(start || 1) + i}</td>
              <td className="cl" dangerouslySetInnerHTML={{ __html: l || ' ' }} />
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default function SourceViewer({ source, onClose }) {
  const [chunk, setChunk] = useState(source.text || source.body ? source : null);
  const [err, setErr] = useState(null);

  useEffect(() => {
    if (!chunk) api.chunk(source.id).then(setChunk).catch((e) => setErr(e.message));
  }, [source.id]); // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => {
    const onKey = (e) => e.key === 'Escape' && onClose();
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [onClose]);

  const p = chunk || {};
  const meta = { ...p, ...(p.meta || {}), ...(source.meta || {}) };
  const k = kindOf(source.source_kind || p.source_kind);
  const content = p.body || p.text || '';
  const isCode = (source.source_kind || p.source_kind) === 'code' && meta.language && meta.language !== 'markdown';
  const isMarkdown = ['docs', 'transcript', 'diagram'].includes(source.source_kind) || meta.language === 'markdown';
  const url = meta.url;
  const sc = source.scores;

  return (
    <div className="overlay" onClick={onClose}>
      <aside className="viewer" onClick={(e) => e.stopPropagation()}>
        <div className="v-head">
          <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
            <span className="kind" style={{ color: k.color, background: k.bg }}>
              {k.icon} {source.source_label || p.source_id}
            </span>
            {source.n && <span className="badge info">source [{source.n}]</span>}
            <button className="x" onClick={onClose} aria-label="Close">
              ×
            </button>
          </div>
          <h3>{source.title || p.title}</h3>
          <div className="path">
            {source.file_path || p.file_path} · {source.locator || p.locator}
          </div>
          <div className="v-actions">
            {url && (
              <a className="ghost" href={url} target="_blank" rel="noreferrer" style={{ textDecoration: 'none' }}>
                {url.includes('github.com') ? 'Open on GitHub ↗' : url.includes('/browse/') ? 'Open in Jira ↗' : 'Open ↗'}
              </a>
            )}
            {sc && (
              <span style={{ font: '11.5px var(--mono)', color: 'var(--muted)' }}>
                {sc.exact ? 'exact id · ' : ''}
                {sc.pinned ? 'inventory · ' : ''}
                dense #{sc.dense_rank ?? '-'} · bm25 #{sc.bm25_rank ?? '-'} · rrf #{sc.fused_rank ?? '-'} · rerank{' '}
                {sc.rerank != null ? sc.rerank.toFixed(3) : '-'}
              </span>
            )}
          </div>
        </div>
        <div className="v-body">
          {err && <div className="err">{err}</div>}
          {!chunk && !err && (
            <div className="status">
              <span className="spinner" /> Loading the chunk
            </div>
          )}
          {chunk && (
            <>
              <div className="meta">
                {SHOW.filter(([key]) => meta[key] != null && meta[key] !== '' && !(Array.isArray(meta[key]) && !meta[key].length)).map(
                  ([key, label]) => (
                    <div key={key}>
                      <small>{label}</small>
                      <span>{fmt(meta[key])}</span>
                    </div>
                  )
                )}
              </div>
              {isCode ? (
                <Code body={content} language={meta.language} start={meta.line_start} />
              ) : isMarkdown ? (
                <div className="md plain" style={{ whiteSpace: 'normal', fontFamily: 'var(--sans)', fontSize: 14 }}>
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>{content}</ReactMarkdown>
                </div>
              ) : (
                <div className="plain">{p.text || content}</div>
              )}
            </>
          )}
        </div>
      </aside>
    </div>
  );
}
