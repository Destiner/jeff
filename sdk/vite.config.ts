import { defineConfig } from 'vite';

export default defineConfig({
  resolve: {
    // Transformers only supplies the tokenizer; share the worker's WASM-only ORT.
    alias: [{ find: /^onnxruntime-web$/, replacement: 'onnxruntime-web/wasm' }],
  },
  build: {
    target: 'safari16',
    outDir: 'dist',
    // TypeScript has already emitted the public entry and declarations here.
    emptyOutDir: false,
    sourcemap: false,
    // Library mode forcibly inlines WASM assets, including unused ORT backends.
    assetsInlineLimit: 0,
    rollupOptions: {
      input: 'src/worker.ts',
      output: {
        format: 'es',
        entryFileNames: 'worker.js',
        inlineDynamicImports: true,
      },
    },
  },
});
