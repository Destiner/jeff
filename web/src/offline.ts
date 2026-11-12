import { model, modelLabel } from './model';

export type OfflineStatus = {
  state: 'unsupported' | 'empty' | 'preparing' | 'ready' | 'error';
  message: string;
  loadedBytes?: number;
  totalBytes?: number;
  completedAssets?: number;
  totalAssets?: number;
  version?: string;
};

type Asset = { url: string; bytes: number; sha256: string };
type Manifest = { schema: 1; version: string; prepared: boolean; missing: string[]; assets: Asset[] };
const prefix = 'jeff-browser-offline-v2-';
const required = [
  ...['model.json', 'model.onnx', 'tokenizer.json', 'tokenizer_config.json'].map(name => model.assetBaseUrl + name),
  ...['ort-wasm-simd-threaded.wasm', 'ort-wasm-simd-threaded.mjs'].map(name => model.ortBaseUrl + name),
];
let preparing = false;
const supported = () => typeof navigator !== 'undefined' && window.isSecureContext &&
  'serviceWorker' in navigator && 'caches' in window;
const unsupported = (): OfflineStatus => ({ state: 'unsupported', message: 'Offline storage requires CacheAPI and service workers on localhost or HTTPS.' });
const empty = (): OfflineStatus => ({ state: 'empty', message: 'Prepare the apps and model for offline use.' });
const errorStatus = (error: unknown): OfflineStatus => ({ state: 'error',
  message: `Offline storage: ${error instanceof Error ? error.message : String(error)}` });
const marker = (version: string) => new URL(`/__jeff_offline_complete__/${version}`, location.origin).href;
const workerUrl = (version: string) => new URL(`/sw-${version}.js`, location.origin).href;
const includesPage = (manifest: Manifest) => manifest.assets.some(asset => new URL(asset.url, location.origin).href === import.meta.url);
const controlled = (manifest: Manifest) => navigator.serviceWorker.controller?.state === 'activated' &&
  navigator.serviceWorker.controller.scriptURL === workerUrl(manifest.version);
const totals = (manifest: Manifest) => ({ version: manifest.version, totalAssets: manifest.assets.length,
  totalBytes: manifest.assets.reduce((sum, asset) => sum + asset.bytes, 0) });

function bounded<T>(promise: Promise<T>, milliseconds = 30_000): Promise<T> {
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error('Offline operation timed out. Retry or reload this page.')), milliseconds);
    promise.then(value => { clearTimeout(timer); resolve(value); }, error => { clearTimeout(timer); reject(error); });
  });
}

function validate(value: unknown): Manifest {
  const m = value as Manifest;
  if (!m || m.schema !== 1 || !/^[a-f0-9]{24}$/.test(m.version) || typeof m.prepared !== 'boolean' ||
      !Array.isArray(m.missing) || !m.missing.every(item => typeof item === 'string') ||
      !Array.isArray(m.assets) || m.assets.length === 0 || m.assets.length > 256 ||
      Object.keys(m).some(key => !['schema', 'version', 'prepared', 'missing', 'assets'].includes(key))) {
    throw new Error('Invalid offline manifest.');
  }
  const seen = new Set<string>();
  for (const asset of m.assets) {
    if (!asset || typeof asset.url !== 'string' || /(?:qwen|m10|jsep)/i.test(asset.url) ||
        !(required.includes(asset.url) || /^\/(?:(?:index|chat|playground)\.html|assets\/[\w.-]+\.(?:js|css))$/.test(asset.url)) ||
        !Number.isSafeInteger(asset.bytes) || asset.bytes <= 0 || !/^[a-f0-9]{64}$/.test(asset.sha256) ||
        Object.keys(asset).some(key => !['url', 'bytes', 'sha256'].includes(key)) || seen.has(asset.url)) {
      throw new Error('Invalid offline asset descriptor.');
    }
    seen.add(asset.url);
  }
  if (['/index.html', '/chat.html', '/playground.html'].some(url => !seen.has(url)) || !Number.isSafeInteger(totals(m).totalBytes) ||
      (m.prepared && (m.missing.length > 0 || required.some(url => !seen.has(url))))) {
    throw new Error('Incomplete offline manifest.');
  }
  return m;
}

async function complete(cache: Cache, manifest: Manifest): Promise<boolean> {
  const saved = await cache.match(marker(manifest.version));
  if (!manifest.prepared || !saved || JSON.stringify(await saved.json()) !== JSON.stringify(manifest)) return false;
  for (const asset of manifest.assets) {
    const response = await cache.match(asset.url);
    if (!response || response.status !== 200 || response.headers.get('X-Jeff-Cached-Bytes') !== String(asset.bytes)) return false;
  }
  return true;
}

async function localStatus(): Promise<OfflineStatus> {
  let savedForPage = false;
  for (const name of await caches.keys()) {
    if (!new RegExp(`^${prefix}[a-f0-9]{24}$`).test(name)) continue;
    const cache = await caches.open(name);
    const response = await cache.match(marker(name.slice(prefix.length)));
    if (!response) continue;
    const manifest = validate(await response.json());
    if (name !== prefix + manifest.version) throw new Error('Offline cache version mismatch.');
    if (!includesPage(manifest) || !await complete(cache, manifest)) continue;
    savedForPage = true;
    if (controlled(manifest)) {
      const base = totals(manifest);
      return { ...base, state: 'ready', loadedBytes: base.totalBytes, completedAssets: base.totalAssets,
        message: `App and ${modelLabel} saved on this browser.` };
    }
  }
  return savedForPage ? { state: 'empty', message: 'The model is saved, but this page is not controlled by its matching offline worker. Close all app tabs and reopen.' } : empty();
}

async function waitForInstall(manifest: Manifest, registration: ServiceWorkerRegistration): Promise<void> {
  const worker = [registration.installing, registration.waiting, registration.active]
    .find(candidate => candidate?.scriptURL === workerUrl(manifest.version));
  if (!worker) throw new Error('The registered worker does not match the saved version.');
  await new Promise<void>((resolve, reject) => {
    const cleanup = () => { clearTimeout(timer); worker.removeEventListener('statechange', check); };
    const check = () => {
      if (['installed', 'activating', 'activated'].includes(worker.state)) { cleanup(); resolve(); }
      else if (worker.state === 'redundant') { cleanup(); reject(new Error('Offline worker installation failed.')); }
    };
    const timer = setTimeout(() => { cleanup(); reject(new Error('Offline worker installation timed out.')); }, 30_000);
    worker.addEventListener('statechange', check);
    check();
  });
}

async function waitForControl(manifest: Manifest, registration: ServiceWorkerRegistration): Promise<void> {
  await bounded(new Promise<void>((resolve, reject) => {
    const worker = registration.installing ?? registration.waiting ?? registration.active;
    const cleanup = () => {
      clearTimeout(timer);
      navigator.serviceWorker.removeEventListener('controllerchange', check);
      worker?.removeEventListener('statechange', check);
    };
    const check = () => {
      if (controlled(manifest)) { cleanup(); resolve(); }
      else if (worker?.state === 'redundant') { cleanup(); reject(new Error('Offline worker installation failed.')); }
    };
    const timer = setTimeout(() => { cleanup(); reject(new Error('Offline worker did not take control. Close all app tabs and reopen.')); }, 29_000);
    navigator.serviceWorker.addEventListener('controllerchange', check);
    worker?.addEventListener('statechange', check);
    check();
  }));
}

async function save(onStatus: (s: OfflineStatus) => void): Promise<void> {
  const abort = new AbortController();
  const deadline = setTimeout(() => abort.abort(), 15 * 60 * 1000);
  const check = () => { if (abort.signal.aborted) throw new Error('Offline preparation cancelled or timed out.'); };
  // Closing/reloading cancels streams; no incomplete version can be registered.
  const cancel = () => abort.abort();
  window.addEventListener('pagehide', cancel);
  try {
    const response = await bounded(fetch('/offline-manifest.json', { cache: 'reload', mode: 'same-origin',
      credentials: 'omit', redirect: 'error', signal: abort.signal }));
    if (response.status !== 200) throw new Error(`Offline manifest HTTP ${response.status}.`);
    const manifest = validate(await bounded(response.json()));
    if (!manifest.prepared) throw new Error(`Offline assets are not staged: ${manifest.missing.join('; ')}`);
    const cache = await bounded(caches.open(prefix + manifest.version));
    const base = totals(manifest);
    if (!await bounded(complete(cache, manifest))) {
      await bounded(cache.delete(marker(manifest.version)));
      let loadedBytes = 0;
      let completedAssets = 0;
      let lastReport = 0;
      const report = (force = false) => {
        if (force || Date.now() - lastReport >= 100) {
          lastReport = Date.now();
          onStatus({ ...base, state: 'preparing', loadedBytes, completedAssets, message: 'Saving app and model assets for offline use…' });
        }
      };
      report(true);
      for (const asset of manifest.assets) {
        check();
        const timer = setTimeout(cancel, 5 * 60 * 1000);
        try {
          // reload, not no-store: an existing worker must not supply its old shell.
          const result = await fetch(asset.url, { cache: 'reload', mode: 'same-origin', credentials: 'omit',
            redirect: 'error', signal: abort.signal });
          if (result.status !== 200 || !result.body) throw new Error(`Asset HTTP ${result.status}: ${asset.url}`);
          const length = result.headers.get('Content-Length');
          if (length !== null && !result.headers.get('Content-Encoding') && Number(length) !== asset.bytes) {
            throw new Error(`Unexpected response size: ${asset.url}`);
          }
          let bytes = 0;
          const stream = result.body.pipeThrough(new TransformStream<Uint8Array, Uint8Array>({
            transform(chunk, target) {
              check();
              bytes += chunk.byteLength;
              if (bytes > asset.bytes) throw new Error(`Oversized response: ${asset.url}`);
              loadedBytes += chunk.byteLength;
              report();
              target.enqueue(chunk);
            },
            flush() { if (bytes !== asset.bytes) throw new Error(`Incomplete response: ${asset.url}`); },
          }), { signal: abort.signal });
          const headers = new Headers(result.headers);
          headers.delete('Content-Encoding');
          headers.set('Content-Length', String(asset.bytes));
          headers.set('X-Jeff-Cached-Bytes', String(asset.bytes));
          await bounded(cache.put(asset.url, new Response(stream, { status: 200, headers })), 5 * 60 * 1000);
          check();
          completedAssets++;
          report(true);
        } finally { clearTimeout(timer); }
      }
      check();
      // The full manifest is also the commit marker and offline discovery record.
      await bounded(cache.put(marker(manifest.version), new Response(JSON.stringify(manifest), { headers: { 'Content-Type': 'application/json' } })));
      if (!await bounded(complete(cache, manifest))) {
        await bounded(cache.delete(marker(manifest.version)));
        throw new Error('Required offline entries are missing after saving.');
      }
    }
    check();
    const hadController = !!navigator.serviceWorker.controller;
    const registration = await bounded(navigator.serviceWorker.register(workerUrl(manifest.version), { scope: '/', updateViaCache: 'none' }));
    await waitForInstall(manifest, registration);
    if (!hadController && includesPage(manifest)) await waitForControl(manifest, registration);
    const current = await bounded(localStatus());
    onStatus(controlled(manifest) && includesPage(manifest) ? current : {
      ...current, message: `${current.message} The update is saved; close all app tabs and reopen to activate it.`,
    });
  } finally {
    abort.abort();
    clearTimeout(deadline);
    window.removeEventListener('pagehide', cancel);
  }
}

export async function initializeOffline(onStatus: (s: OfflineStatus) => void): Promise<void> {
  onStatus(await readOfflineStatus());
}

export async function prepareOffline(onStatus: (s: OfflineStatus) => void): Promise<void> {
  if (!supported()) { onStatus(unsupported()); return; }
  if (preparing) { onStatus({ state: 'preparing', message: 'Offline preparation is already running. Wait for it to finish.' }); return; }
  preparing = true;
  // A cross-tab lock prevents a second writer from modifying a just-completed version.
  try {
    if (!navigator.locks) throw new Error('This browser lacks the cross-tab storage lock required for safe preparation.');
    await navigator.locks.request('jeff-m9-offline-prepare', { ifAvailable: true }, async lock => {
      if (!lock) { onStatus({ state: 'preparing', message: 'Offline preparation is running in another tab.' }); return; }
      await save(onStatus);
    });
  } catch (error) { onStatus(errorStatus(error)); }
  finally { preparing = false; }
}

export async function readOfflineStatus(): Promise<OfflineStatus> {
  if (!supported()) return unsupported();
  try { return await bounded(localStatus()); }
  catch (error) { return errorStatus(error); }
}
