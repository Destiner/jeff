/* Generated immutable static-only worker. Preparation belongs to the window. */
const manifest = /* OFFLINE_MANIFEST */;
const cacheName = `jeff-browser-offline-v2-${manifest.version}`;
const markerUrl = new URL(`/__jeff_offline_complete__/${manifest.version}`, self.location.origin).href;
const descriptors = new Map(manifest.assets.map(asset => [asset.url, asset]));

async function complete(cache) {
  const marker = await cache.match(markerUrl);
  if (!manifest.prepared || !marker || JSON.stringify(await marker.json()) !== JSON.stringify(manifest)) return false;
  for (const asset of manifest.assets) {
    const response = await cache.match(new URL(asset.url, self.location.origin).href);
    if (!response || response.status !== 200 || response.headers.get('X-Jeff-Cached-Bytes') !== String(asset.bytes)) return false;
  }
  return true;
}

// A direct/accidental registration cannot install an unprepared replacement.
self.addEventListener('install', event => event.waitUntil((async () => {
  if (!await complete(await caches.open(cacheName))) throw new Error('Offline version is not completely prepared.');
})()));
// No skipWaiting and no cache deletion: old tabs keep their complete build.
self.addEventListener('activate', event => event.waitUntil((async () => {
  if (!await complete(await caches.open(cacheName))) throw new Error('Offline version is no longer complete.');
  await self.clients.claim();
})()));

self.addEventListener('fetch', event => {
  const request = event.request;
  const url = new URL(request.url);
  // Explicit preparation must reach the network, even through an older worker.
  // Ordinary runtime no-store requests deliberately still use completed entries.
  if (request.cache === 'reload' || request.method !== 'GET' || url.origin !== self.location.origin ||
      url.search || url.hash || request.headers.has('Range')) return;
  const path = request.mode === 'navigate' && url.pathname === '/' ? '/index.html' : url.pathname;
  if (!descriptors.has(path)) return;
  event.respondWith((async () => {
    const cache = await caches.open(cacheName);
    if (await complete(cache)) {
      const response = await cache.match(new URL(path, self.location.origin).href);
      if (response) return response;
    }
    return fetch(request);
  })());
});
