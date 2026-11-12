import { defineConfig } from 'vite';

export default defineConfig({
  build: { target: 'safari16', sourcemap: false },
  worker: { format: 'es' },
});
