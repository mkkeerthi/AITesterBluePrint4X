import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.jsx';
import 'highlight.js/styles/github.css';
import './styles.css';
import './theme/dark.css';
import './theme/toggle.css';
import { initTheme } from './theme/theme.js';

initTheme();

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
