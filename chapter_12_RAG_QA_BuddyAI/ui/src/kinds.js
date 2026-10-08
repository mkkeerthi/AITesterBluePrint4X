// Visual identity per knowledge source, so a citation chip tells you at a
// glance whether the claim came from code, a ticket, a log or a requirement.
import { isDark } from './theme/theme.js';
import { KIND_DARK } from './theme/kindsDark.js';

export const KIND = {
  testcases: { icon: '🧪', color: '#2f7d4f', bg: '#eaf6ee', label: 'Test case' },
  jira: { icon: '🐞', color: '#2563eb', bg: '#eaf1fe', label: 'Jira' },
  docs: { icon: '📄', color: '#b45309', bg: '#fdf3e4', label: 'Doc' },
  transcript: { icon: '🗓️', color: '#7c3aed', bg: '#f3eefe', label: 'Meeting' },
  diagram: { icon: '🔷', color: '#0e7490', bg: '#e6f5f8', label: 'Diagram' },
  logs: { icon: '🧯', color: '#c2410c', bg: '#fdeee6', label: 'CI log' },
  code: { icon: '⌨️', color: '#4338ca', bg: '#eeeffd', label: 'Code' },
  figma: { icon: '🎨', color: '#be185d', bg: '#fdecf4', label: 'Figma' },
};

const FALLBACK = { icon: '•', color: '#6f6b60', bg: '#f1efe8' };

// Colour chips are applied as inline styles, so the theme swap happens here:
// dark only overrides colour/background; icon and label come from KIND.
export const kindOf = (k) => {
  const base = KIND[k] || { ...FALLBACK, label: k || 'source' };
  if (!isDark()) return base;
  return { ...base, ...(KIND_DARK[k] || KIND_DARK.default) };
};
