import { defineConfig } from 'vite';
import { fileURLToPath } from 'node:url';

export default defineConfig({
  build: { target: 'safari16', sourcemap: false, manifest: true,
    rollupOptions: { input: ['index.html', 'chat.html', 'playground.html'].map(name => fileURLToPath(new URL(name, import.meta.url))) } },
  worker: { format: 'es' },
});
