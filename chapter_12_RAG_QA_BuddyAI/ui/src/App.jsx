import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import Sidebar from './components/Sidebar.jsx';
import Message from './components/Message.jsx';
import SourceViewer from './components/SourceViewer.jsx';
import { api, DEMO, demoMeta } from './client.js';
import ThemeToggle from './theme/ThemeToggle.jsx';

export default function App() {
  const [health, setHealth] = useState(null);
  const [sources, setSources] = useState([]);
  const [modes, setModes] = useState([]);
  const [modeId, setModeId] = useState('ask');
  const [custom, setCustom] = useState(null); // null = use the mode's default sources
  const [msgs, setMsgs] = useState([]);
  const [input, setInput] = useState('');
  const [busy, setBusy] = useState(false);
  const [viewer, setViewer] = useState(null);
  const [job, setJob] = useState(null);
  const [bootErr, setBootErr] = useState(null);
  const [meta, setMeta] = useState(null);
  const abortRef = useRef(null);
  const endRef = useRef(null);
  const inputRef = useRef(null);

  const refresh = useCallback(async () => {
    const [h, s] = await Promise.all([api.health(), api.sources()]);
    setHealth(h);
    setSources(s);
  }, []);

  useEffect(() => {
    Promise.all([refresh(), api.modes().then(setModes), demoMeta().then(setMeta)]).catch((e) => setBootErr(e.message));
  }, [refresh]);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth', block: 'end' });
  }, [msgs]);

  const mode = modes.find((m) => m.id === modeId);
  const phase1 = sources.filter((s) => s.phase === 1).map((s) => s.id);
  const selected = custom ?? mode?.sources ?? phase1;

  const setMode = (id) => {
    setModeId(id);
    setCustom(null);
    inputRef.current?.focus();
  };
  const toggleSource = (id) => {
    const base = custom ?? mode?.sources ?? phase1;
    setCustom(base.includes(id) ? base.filter((x) => x !== id) : [...base, id]);
  };

  // One code path for typed questions and example clicks. The mode is passed
  // explicitly because an example may switch modes in the same click, before
  // React state has settled.
  async function ask(question, m = mode, srcs = custom) {
    const q = question.trim();
    if (!q || busy || !m) return;
    setInput('');
    const id = Date.now();
    const history = msgs
      .filter((x) => x.done && !x.error)
      .slice(-2)
      .flatMap((x) => [
        { role: 'user', content: x.question },
        { role: 'assistant', content: x.text.slice(0, 1500) },
      ]);
    setMsgs((prev) => [...prev, { id, question: q, modeId: m.id, modeLabel: m.label, modeIcon: m.icon, text: '', status: 'Searching', streaming: true }]);
    const update = (patch) => setMsgs((prev) => prev.map((x) => (x.id === id ? { ...x, ...(typeof patch === 'function' ? patch(x) : patch) } : x)));
    const ctl = new AbortController();
    abortRef.current = ctl;
    setBusy(true);
    try {
      for await (const evt of api.chat({ question: q, mode: m.id, sources: srcs, history, signal: ctl.signal })) {
        if (evt.type === 'status') update({ status: evt.message });
        else if (evt.type === 'retrieval') update({ retrieval: evt.retrieval, recorded: evt.recorded, status: 'Writing the answer' });
        else if (evt.type === 'token') update((x) => ({ text: x.text + evt.text }));
        else if (evt.type === 'done') update((x) => ({ done: evt, text: evt.answer ?? x.text }));
        else if (evt.type === 'error') update({ error: evt.message });
      }
    } catch (e) {
      if (e.name !== 'AbortError') update({ error: e.message });
    } finally {
      update({ streaming: false });
      setBusy(false);
      abortRef.current = null;
    }
  }

  async function startIngest() {
    try {
      await api.ingest({ full: false });
      const poll = async () => {
        const s = await api.ingestStatus();
        setJob(s);
        if (s.running) setTimeout(poll, 1000);
        else refresh();
      };
      poll();
    } catch (e) {
      setJob({ running: false, error: e.message });
    }
  }

  const examples = useMemo(() => {
    if (!modes.length) return [];
    if (mode && mode.id !== 'ask') return mode.examples.map((q) => ({ q, m: mode }));
    return modes.flatMap((m) => m.examples.slice(0, m.id === 'ask' ? 2 : 1).map((q) => ({ q, m })));
  }, [modes, mode]);

  const runExample = (q, m) => {
    if (m.id !== modeId) {
      setModeId(m.id);
      setCustom(null);
      return ask(q, m, null);
    }
    return ask(q, m, custom);
  };

  const h = health || {};
  const rr = h.reranker || {};
  return (
    <div className="app">
      <Sidebar
        modes={modes}
        modeId={modeId}
        setMode={setMode}
        sources={sources}
        selected={selected}
        toggleSource={toggleSource}
        resetSources={() => setCustom(null)}
        custom={custom}
        health={health}
        job={job}
        onIngest={startIngest}
      />
      <main className="main">
        <div className="topbar">
          {DEMO && <span className="pill demo">Demo mode</span>}
          {!health && !bootErr && (
            <span className="pill">
              <span className="dot" />
              {DEMO ? 'Loading demo data…' : 'Connecting…'}
            </span>
          )}
          {health && (
            <>
              <span className={`pill ${h.qdrant ? 'ok' : 'bad'}`}>
                <span className="dot" />
                {h.vector_db || 'Qdrant'} · {(h.points ?? 0).toLocaleString()} chunks
              </span>
              <span className={`pill ${h.embed_model_ready ? 'ok' : 'bad'}`}>
                <span className="dot" />
                {h.embed_model} · {h.embed_dim}d
              </span>
              <span className={`pill ${rr.enabled ? 'ok' : ''}`}>
                <span className="dot" />
                {rr.enabled ? rr.model?.split('/').pop() : 'rerank off'}
              </span>
              <span className={`pill ${h.llm_configured ? 'ok' : 'bad'}`}>
                <span className="dot" />
                {h.llm_model} · {h.llm_provider}
              </span>
            </>
          )}
          <span className="spacer" />
          <ThemeToggle />
          {msgs.length > 0 && (
            <button className="ghost" onClick={() => setMsgs([])} disabled={busy}>
              New chat
            </button>
          )}
        </div>

        <div className="thread">
          <div className="thread-inner">
            {bootErr && <div className="err">Could not reach the QABuddy API: {bootErr}</div>}
            {msgs.length === 0 && (
              <div className="hero">
                <h2>{mode && mode.id !== 'ask' ? `${mode.icon} ${mode.label}` : 'Ask your QA knowledge base'}</h2>
                <p>
                  {mode && mode.id !== 'ask'
                    ? mode.description
                    : 'One question, one cited answer, grounded in your Selenium and Playwright frameworks, test cases, Jira bugs, requirements, meeting notes, Lucid charts and Jenkins logs.'}
                </p>
                <div className="examples">
                  {examples.map(({ q, m }) => (
                    <button key={q} className="example" onClick={() => runExample(q, m)}>
                      <small>
                        {m.icon} {m.label}
                      </small>
                      {q}
                    </button>
                  ))}
                </div>
                <div className="pipeline">
                  <span>exact ids</span>+<span>Qwen3 dense</span>+<span>code-aware BM25</span>→<span>Qdrant RRF</span>→
                  <span>bge rerank</span>→<span>cited answer</span>
                </div>
                {DEMO && meta?.recorded_at && (
                  <p style={{ marginTop: 18, fontSize: 12.5 }}>
                    Demo mode: the example questions replay runs of the full self-hosted pipeline recorded on{' '}
                    {new Date(meta.recorded_at).toLocaleDateString()}. Your own questions run keyword search in the browser.
                  </p>
                )}
              </div>
            )}
            {msgs.map((m) => (
              <Message key={m.id} msg={m} onOpen={setViewer} />
            ))}
            <div ref={endRef} />
          </div>
        </div>

        <div className="composer-wrap">
          <div className="composer-inner">
            <form
              className="composer"
              onSubmit={(e) => {
                e.preventDefault();
                ask(input);
              }}
            >
              <textarea
                ref={inputRef}
                rows={1}
                value={input}
                placeholder={mode ? `${mode.icon} ${mode.label}: ask a question…` : 'Ask a question…'}
                onChange={(e) => {
                  setInput(e.target.value);
                  e.target.style.height = 'auto';
                  e.target.style.height = `${e.target.scrollHeight}px`;
                }}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    ask(input);
                  }
                }}
              />
              {busy ? (
                <button type="button" className="send stop" onClick={() => abortRef.current?.abort()}>
                  ■ Stop
                </button>
              ) : (
                <button type="submit" className="send" disabled={!input.trim()}>
                  Ask ↵
                </button>
              )}
            </form>
            <div className="hint">
              <span>
                Mode: <span className="mode-chip">{mode?.label}</span> · searching {selected.length} source{selected.length === 1 ? '' : 's'}
                {custom ? ' (custom)' : ''}
              </span>
              <span>Enter to send · Shift+Enter for a new line · answers cite their sources</span>
            </div>
          </div>
        </div>
      </main>
      {viewer && <SourceViewer source={viewer} onClose={() => setViewer(null)} />}
    </div>
  );
}
