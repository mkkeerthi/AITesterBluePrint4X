import { useCallback, useEffect, useState } from 'react';

const KEY = 'qabuddy-theme';
const root = () => document.documentElement;

export function currentTheme() {
  return root().dataset.theme === 'dark' ? 'dark' : 'light';
}

// Read outside React too (kinds.js), so colour chips follow the theme.
export const isDark = () => currentTheme() === 'dark';

function store(theme) {
  root().dataset.theme = theme;
  try {
    localStorage.setItem(KEY, theme);
  } catch {
    /* private mode: keep it in-memory only */
  }
}

// Called once before the first render (main.jsx + the pre-paint script in index.html).
export function initTheme() {
  let theme = null;
  try {
    theme = localStorage.getItem(KEY);
  } catch {
    /* ignore */
  }
  if (theme !== 'dark' && theme !== 'light') {
    theme = window.matchMedia?.('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }
  root().dataset.theme = theme;
  return theme;
}

export function useTheme() {
  const [theme, setTheme] = useState(currentTheme);
  useEffect(() => {
    root().dataset.theme = theme;
  }, [theme]);
  const toggle = useCallback(() => {
    setTheme((t) => {
      const next = t === 'dark' ? 'light' : 'dark';
      store(next);
      return next;
    });
  }, []);
  return { theme, toggle };
}
