import { mkdir, realpath, writeFile } from 'node:fs/promises';
import { createRequire } from 'node:module';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';
import { build } from 'vite';

const root = fileURLToPath(new URL('../', import.meta.url));
const require = createRequire(import.meta.url);
// The pinned ORT conditional exports omit types; real paths preserve isolated dependencies.
const ortTypes = await realpath(resolve(dirname(require.resolve('onnxruntime-web/wasm')), '../types.d.ts'));
const config = resolve(root, '.build/tsconfig.json');
await mkdir(dirname(config), { recursive: true });
await writeFile(config, JSON.stringify({
  extends: '../tsconfig.json', files: [ortTypes],
  // Supersede the legacy logical-path declaration references, not the worker source checks.
  exclude: [resolve(root, 'src/runtime/ort-wasm.d.ts'), resolve(root, 'src/runtime/ort-webgpu.d.ts')],
}, null, 2));
function run(args) {
  const result = spawnSync(process.execPath, args, { cwd: root, stdio: 'inherit' });
  if (result.error) throw result.error;
  if (result.status !== 0) process.exit(result.status ?? 1);
}
run([require.resolve('typescript/bin/tsc'), '-p', config]);
await build({ root, configFile: resolve(root, 'vite.config.ts') });
run([resolve(root, 'scripts/build-offline.mjs')]);
