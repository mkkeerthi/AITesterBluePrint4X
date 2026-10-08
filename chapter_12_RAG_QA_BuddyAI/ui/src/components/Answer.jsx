import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeHighlight from 'rehype-highlight';
import { kindOf } from '../kinds.js';

// [3] -> a clickable chip, coloured by the kind of source it points to.
// Code spans and fences are left alone so `args[0]` never becomes a citation.
export function linkify(md, n) {
  const parts = md.split(/(```[\s\S]*?(?:```|$)|`[^`\n]*`)/g);
  return parts
    .map((p, i) =>
      i % 2
        ? p
        : p
            .replace(/【\s*(\d{1,2})(?:†[^】]*)?】/g, '[$1]')
            .replace(/\[(\d{1,2})\](?!\()/g, (m, d) => (+d >= 1 && +d <= n ? `[${d}](#cite-${d})` : m))
    )
    .join('');
}

export default function Answer({ text, sources, onOpen }) {
  const components = {
    a({ href, children }) {
      if (href && href.startsWith('#cite-')) {
        const n = Number(href.slice(6));
        const s = sources[n - 1];
        const k = kindOf(s?.source_kind);
        return (
          <button
            type="button"
            className="cite"
            style={{ color: k.color, background: k.bg, borderColor: `${k.color}55` }}
            title={s ? `${s.title} · ${s.locator}` : ''}
            onClick={() => s && onOpen(s)}
          >
            {n}
          </button>
        );
      }
      return (
        <a href={href} target="_blank" rel="noreferrer">
          {children}
        </a>
      );
    },
  };
  return (
    <div className="md">
      <ReactMarkdown remarkPlugins={[remarkGfm]} rehypePlugins={[rehypeHighlight]} components={components}>
        {linkify(text, sources.length)}
      </ReactMarkdown>
    </div>
  );
}
