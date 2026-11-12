import { mkdir, realpath, writeFile } from 'node:fs/promises';
import { createRequire } from 'node:module';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';
import { build } from 'vite';

const root = fileURLToPath(new URL('../', import.meta.url));
const require = createRequire(import.meta.url);
// ORT's pinned conditional exports omit types. Resolve its real package location
// so both isolated installs and hoisted workspace dependencies use its declarations.
const ortTypes = await realpath(resolve(dirname(require.resolve('onnxruntime-web/wasm')), '../types.d.ts'));
const config = resolve(root, '.build/tsconfig.json');
await mkdir(dirname(config), { recursive: true });
await writeFile(config, JSON.stringify({ extends: '../tsconfig.json', files: [ortTypes] }, null, 2));
const result = spawnSync(process.execPath, [require.resolve('typescript/bin/tsc'), '-p', config], {
  cwd: root, stdio: 'inherit',
});
if (result.error) throw result.error;
if (result.status !== 0) process.exit(result.status ?? 1);
await build({ root, configFile: resolve(root, 'vite.config.ts') });
