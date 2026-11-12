import { createHash } from 'node:crypto';
import { readFile, stat, writeFile } from 'node:fs/promises';
import { dirname, resolve, posix } from 'node:path';
import { fileURLToPath } from 'node:url';

const web = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const args = process.argv.slice(2);
if (args.length && (args.length !== 2 || args[0] !== '--dist' || !/^dist(?:-[a-z0-9]+)?$/.test(args[1]))) {
  throw new Error('Usage: bun scripts/build-offline.mjs [--dist dist-NAME]');
}
const dist = resolve(web, args[1] ?? 'dist');
const hash = value => createHash('sha256').update(value).digest('hex');
const config = JSON.parse(await readFile(resolve(web, 'model-config.json'), 'utf8'));
if (!/^\/models\/[a-z0-9-]+\/$/.test(config.assetBaseUrl) || config.ortBaseUrl !== '/ort/') throw new Error('Unsupported configured asset paths');
const required = [
  ...['model.json', 'model.onnx', 'tokenizer.json', 'tokenizer_config.json'].map(name => config.assetBaseUrl + name),
  ...['ort-wasm-simd-threaded.wasm', 'ort-wasm-simd-threaded.mjs'].map(name => config.ortBaseUrl + name),
];
const forbidden = value => /(?:qwen|m10|jsep)/i.test(value);
const assets = new Map();
const missing = [];
const appFiles = new Set(['/index.html', '/chat.html', '/playground.html']);
let viteManifest;
try {
  viteManifest = JSON.parse(await readFile(resolve(dist, '.vite/manifest.json'), 'utf8'));
} catch (error) {
  if (error.code !== 'ENOENT') throw error;
}

// Walk only the app's actual references, not every file Vite happened to emit.
// A Qwen adapter must remain a separately named chunk (qwen/m10), not an M9 dependency.
async function addApp(url) {
  if (assets.has(url) || forbidden(url)) return;
  if (!/^\/(?:(?:index|chat|playground)\.html|assets\/[\w.-]+\.(?:js|css))$/.test(url)) {
    throw new Error(`Unsupported offline app dependency: ${url}`);
  }
  const body = await readFile(resolve(dist, `.${url}`));
  assets.set(url, { url, bytes: body.length, sha256: hash(body) });
  const text = body.toString('utf8');
  const references = text.matchAll(/["']((?:\/?assets\/|\.\/)[\w./-]+\.(?:js|css))["']/g);
  for (const [, reference] of references) {
    const dependency = reference.startsWith('assets/') ? `/${reference}` :
      reference.startsWith('/') ? reference : posix.resolve(posix.dirname(url), reference);
    // Bundled libraries retain source/debug string literals that are not emitted imports.
    if (!/^\/assets\/[\w.-]+\.(?:js|css)$/.test(dependency) || forbidden(dependency)) continue;
    try {
      if ((await stat(resolve(dist, `.${dependency}`))).isFile()) await addApp(dependency);
    } catch (error) {
      if (error.code !== 'ENOENT') throw error;
    }
  }
}
if (viteManifest) {
  const seen = new Set();
  const visit = key => {
    if (seen.has(key)) return;
    seen.add(key);
    const entry = viteManifest[key];
    if (!entry) throw new Error(`Missing Vite manifest entry: ${key}`);
    if (forbidden(`${key} ${entry.file}`)) return;
    appFiles.add(`/${entry.file}`);
    for (const css of entry.css ?? []) appFiles.add(`/${css}`);
    for (const dependency of [...(entry.imports ?? []), ...(entry.dynamicImports ?? [])]) visit(dependency);
  };
  for (const [key, entry] of Object.entries(viteManifest)) {
    if (entry.isEntry && !forbidden(key)) visit(key);
  }
}
for (const file of appFiles) await addApp(file);
if (![...assets.keys()].some(url => /^\/assets\/worker-[\w-]+\.js$/.test(url))) {
  throw new Error('The emitted SDK worker is missing from the offline app graph.');
}
let receipt;
try {
  receipt = JSON.parse(await readFile(resolve(web, 'asset-manifest.local.json'), 'utf8'));
} catch (error) {
  if (error.code !== 'ENOENT') throw error;
}
for (const url of required) {
  const rows = receipt?.assets?.filter(asset => asset.url === url) ?? [];
  const entry = rows.length === 1 ? rows[0] : undefined;
  if (!entry || !Number.isSafeInteger(entry.bytes) || entry.bytes <= 0 ||
      !/^[a-f0-9]{64}$/.test(entry.sha256) || typeof entry.source !== 'string') {
    missing.push(`${url}: missing valid staged receipt`);
    continue;
  }
  try {
    const actual = await stat(resolve(dist, `.${url}`));
    if (!actual.isFile() || actual.size !== entry.bytes) {
      missing.push(`${url}: staged size differs from receipt`);
      continue;
    }
    assets.set(url, { url, bytes: entry.bytes, sha256: entry.sha256 });
  } catch (error) {
    if (error.code !== 'ENOENT') throw error;
    missing.push(`${url}: not staged`);
  }
}
const descriptors = [...assets.values()].sort((a, b) => a.url.localeCompare(b.url));
const template = await readFile(resolve(web, 'scripts/service-worker-template.js'), 'utf8');
const payload = { schema: 1, prepared: missing.length === 0, missing, assets: descriptors };
// Includes worker implementation and compiled app bytes; staged large assets use their existing source identity.
const version = hash(template + JSON.stringify(payload)).slice(0, 24);
const manifest = { ...payload, version };
await writeFile(resolve(dist, `sw-${version}.js`), template.replace('/* OFFLINE_MANIFEST */', () => JSON.stringify(manifest)));
await writeFile(resolve(dist, 'offline-manifest.json'), `${JSON.stringify(manifest)}\n`);
await writeFile(resolve(web, 'offline-manifest.local.json'), `${JSON.stringify(manifest, null, 2)}\n`);
console.log(`Offline ${version}: ${manifest.prepared ? `${descriptors.length} required assets` : `not prepared (${missing.join('; ')})`}`);
