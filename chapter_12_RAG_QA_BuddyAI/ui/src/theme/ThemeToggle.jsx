import React from 'react';
import { useTheme } from './theme.js';

export default function ThemeToggle() {
  const { theme, toggle } = useTheme();
  const dark = theme === 'dark';
  const label = dark ? 'Switch to light theme' : 'Switch to dark theme';
  return (
    <button type="button" className="ghost theme-toggle" onClick={toggle} aria-label={label} title={label} aria-pressed={dark}>
      <span className="ico" aria-hidden="true">
        {dark ? '☀️' : '🌙'}
      </span>
      <span className="lbl">{dark ? 'Light' : 'Dark'}</span>
    </button>
  );
}
