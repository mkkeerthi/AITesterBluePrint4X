import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// `npm run dev` proxies /api to the Python server; `npm run build` output is
// served by that same server in production (one process, one port).
export default defineConfig({
  plugins: [react()],
  server: { port: 5300, proxy: { '/api': { target: 'http://localhost:8300', changeOrigin: true } } },
});
