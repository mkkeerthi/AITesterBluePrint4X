// Vercel serverless function for the hosted demo's free-text questions.
//
// Retrieval already happened in the browser (BM25 over the exported corpus);
// this function only turns the retrieved sources into a cited answer. The
// system prompt and mode instructions are generated from the real Python
// code (api/_prompt.js), so the demo follows the same grounding rules.
// GROQ_API_KEY lives in the Vercel project settings, never in the browser.

import PROMPT from './_prompt.js';

const WINDOW_MS = 60 * 60 * 1000;
const MAX_PER_IP = 20;
const hits = new Map();

function rateLimit(ip) {
  const now = Date.now();
  const recent = (hits.get(ip) || []).filter((t) => now - t < WINDOW_MS);
  if (recent.length >= MAX_PER_IP) return { ok: false, mins: Math.ceil((WINDOW_MS - (now - recent[0])) / 60000) };
  recent.push(now);
  hits.set(ip, recent);
  if (hits.size > 5000) hits.clear();
  return { ok: true };
}

const normalizeCitations = (t) => t.replace(/【\s*(\d{1,2})(?:†[^】]*)?】/g, '[$1]');
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).json({ error: 'Use POST.' });
  }
  if (!process.env.GROQ_API_KEY) return res.status(503).json({ error: 'GROQ_API_KEY is not set on this deployment.' });

  const ip = (req.headers['x-forwarded-for'] || '').split(',')[0].trim() || 'unknown';
  const limit = rateLimit(ip);
  if (!limit.ok) {
    return res.status(429).json({
      error: `Demo limit reached (${MAX_PER_IP} questions per hour). Try again in about ${limit.mins} minutes, or run QABuddy locally.`,
    });
  }

  const body = typeof req.body === 'string' ? JSON.parse(req.body || '{}') : req.body || {};
  const question = String(body.question || '').slice(0, 1000);
  const mode = PROMPT.modes[body.mode] || PROMPT.modes.ask;
  const sources = Array.isArray(body.sources) ? body.sources.slice(0, 10) : [];
  if (!question || !sources.length) return res.status(400).json({ error: 'Send { question, mode, sources: [...] }.' });

  const context = sources
    .map((s, i) => `[${i + 1}] ${String(s.title || '').slice(0, 200)}\nsource: ${s.source_id} | ${s.file_path} | ${s.locator}\n${String(s.text || '').slice(0, 3200)}`)
    .join('\n\n');
  const system = PROMPT.system + (mode.instruction ? `\n\nTask: ${mode.label}. ${mode.instruction}` : '');

  for (let attempt = 0; attempt < 3; attempt++) {
    const r = await fetch('https://api.groq.com/openai/v1/chat/completions', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${process.env.GROQ_API_KEY}` },
      body: JSON.stringify({
        model: PROMPT.model,
        temperature: 0.1,
        max_tokens: Math.min(mode.max_tokens || 900, 1200),
        reasoning_effort: 'low',
        messages: [
          { role: 'system', content: system },
          { role: 'user', content: `Sources:\n\n${context}\n\nQuestion: ${question}` },
        ],
      }),
      signal: AbortSignal.timeout(50000),
    });
    const text = await r.text();
    if (r.status === 429 && attempt < 2) {
      const m = text.match(/try again in ([\d.]+)s/);
      await sleep(Math.min(20, m ? parseFloat(m[1]) + 0.5 : 5) * 1000);
      continue;
    }
    if (!r.ok) return res.status(502).json({ error: `The LLM provider returned ${r.status}. Try again shortly.` });
    const data = JSON.parse(text);
    return res.status(200).json({
      answer: normalizeCitations(data.choices?.[0]?.message?.content || ''),
      usage: data.usage,
      model: data.model,
    });
  }
  return res.status(429).json({ error: 'The shared demo key is busy (provider rate limit). Try again in a minute.' });
}
