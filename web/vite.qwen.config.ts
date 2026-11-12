import { defineConfig } from 'vite';
export default defineConfig({
  base: '/qwen-proof/', publicDir: false,
  build: { target: 'safari16', outDir: 'dist-qwen', emptyOutDir: true, sourcemap: false,
    rollupOptions: { input: 'qwen-proof.html' } },
  worker: { format: 'es' },
});
