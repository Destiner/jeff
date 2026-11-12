import { constants } from 'node:fs';
import { lstat, open, realpath } from 'node:fs/promises';
import path from 'node:path';
import { Readable } from 'node:stream';
import { fileURLToPath } from 'node:url';

const web = fileURLToPath(new URL('../', import.meta.url));
const securityHeaders = {
  'Cross-Origin-Opener-Policy': 'same-origin',
  'Cross-Origin-Embedder-Policy': 'require-corp',
  'Cross-Origin-Resource-Policy': 'same-origin',
  'Content-Security-Policy': "default-src 'self'; script-src 'self' blob: 'wasm-unsafe-eval'; worker-src 'self' blob:; connect-src 'self'; style-src 'self'; img-src 'self' data:; object-src 'none'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'",
  'X-Content-Type-Options': 'nosniff',
  // The service worker owns CacheAPI; HTTP caching remains disabled.
  'Cache-Control': 'no-store',
};
const mime = {
  '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8',
  '.mjs': 'text/javascript; charset=utf-8', '.json': 'application/json; charset=utf-8',
  '.jsonl': 'application/x-ndjson; charset=utf-8', '.wasm': 'application/wasm',
  '.onnx': 'application/octet-stream', '.css': 'text/css; charset=utf-8',
  '.txt': 'text/plain; charset=utf-8', '.svg': 'image/svg+xml',
  '.png': 'image/png', '.ico': 'image/x-icon',
};

function options() {
  const result = { port: 4173, durationSeconds: 1800 };
  const seen = new Set();
  const args = process.argv.slice(2);
  for (let i = 0; i < args.length; i += 2) {
    const flag = args[i];
    const value = args[i + 1];
    if (!['--port', '--duration-seconds', '--stop-at'].includes(flag) || seen.has(flag) || !value) {
      throw new Error('Usage: bun scripts/serve.mjs [--port 1..65535] [--duration-seconds 1..14400] [--stop-at UTC_ISO_TIMESTAMP]');
    }
    seen.add(flag);
    if (flag === '--stop-at') {
      const timestamp = Date.parse(value);
      if (!/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{3})?Z$/.test(value)
        || !Number.isFinite(timestamp)
        || new Date(timestamp).toISOString() !== (value.includes('.') ? value : value.replace('Z', '.000Z'))) {
        throw new Error('Invalid --stop-at: use a UTC ISO timestamp');
      }
      if (timestamp <= Date.now()) throw new Error('--stop-at deadline has elapsed');
      result.stopAt = timestamp;
      continue;
    }
    if (!/^\d+$/.test(value)) throw new Error(`Invalid ${flag}`);
    const number = Number(value);
    const max = flag === '--port' ? 65535 : 14400;
    if (!Number.isSafeInteger(number) || number < 1 || number > max) throw new Error(`Invalid ${flag}`);
    result[flag === '--port' ? 'port' : 'durationSeconds'] = number;
  }
  return result;
}

async function main() {
  const { port, durationSeconds, stopAt = Infinity } = options();
  const deadline = Math.min(Date.now() + durationSeconds * 1000, stopAt);
  const dist = path.join(web, 'dist');
  if (!(await lstat(dist)).isDirectory() || await realpath(dist) !== dist) {
    throw new Error('web/dist must be a real directory without symlink ancestors');
  }
  const index = await lstat(path.join(dist, 'index.html'));
  if (!index.isFile() || index.isSymbolicLink()) throw new Error('Build web/dist/index.html before serving');

  if (deadline <= Date.now()) throw new Error('Serving deadline has elapsed');
  const server = Bun.serve({
    hostname: '127.0.0.1', port,
    async fetch(request) {
      let loggedPath = '/';
      let status = 500;
      let bytes = 0;
      let handle;
      const reply = (code, message, extra = {}) => {
        status = code;
        bytes = request.method === 'HEAD' ? 0 : Buffer.byteLength(message);
        return new Response(request.method === 'HEAD' ? null : message, {
          status: code,
          headers: { ...securityHeaders, 'Content-Type': 'text/plain; charset=utf-8',
            'Content-Length': String(Buffer.byteLength(message)), ...extra },
        });
      };
      try {
        // Inspect the path as supplied by Bun, before any additional URL normalization.
        const raw = request.url.match(/^https?:\/\/[^/]+(\/[^?#]*)?/)?.[1] ?? '/';
        loggedPath = raw.slice(0, 8192);
        if (!['GET', 'HEAD'].includes(request.method)) return reply(405, 'Method not allowed\n', { Allow: 'GET, HEAD' });
        if (raw.length > 8192) return reply(414, 'URI too long\n');
        let decoded;
        try { decoded = decodeURIComponent(raw); } catch { return reply(400, 'Bad path\n'); }
        // Reject residual encoding too: double-encoded traversal is never a filename here.
        if (/[\x00-\x1f\x7f\\%]/.test(decoded) || decoded.split('/').some(part => part === '.' || part === '..')) {
          return reply(400, 'Bad path\n');
        }
        const relative = decoded === '/' ? 'index.html' : decoded.slice(1);
        const parts = relative.split('/');
        if (parts.some(part => !part)) return reply(404, 'Not found\n');
        let target = dist;
        let targetStat;
        for (const part of parts) {
          target = path.join(target, part);
          targetStat = await lstat(target);
          if (targetStat.isSymbolicLink()) return reply(404, 'Not found\n');
        }
        if (!targetStat.isFile()) return reply(404, 'Not found\n');
        const resolved = await realpath(target);
        if (!resolved.startsWith(`${dist}${path.sep}`)) return reply(404, 'Not found\n');
        handle = await open(resolved, constants.O_RDONLY | constants.O_NOFOLLOW | constants.O_NONBLOCK);
        const stat = await handle.stat();
        if (!stat.isFile()) return reply(404, 'Not found\n');
        status = 200;
        // Payload size offered, not a claim of bytes received by the client.
        bytes = request.method === 'HEAD' ? 0 : stat.size;
        const headers = { ...securityHeaders, 'Content-Type': mime[path.extname(resolved).toLowerCase()] ?? 'application/octet-stream', 'Content-Length': String(stat.size) };
        if (relative === 'sw.js') headers['Service-Worker-Allowed'] = '/';
        if (request.method === 'HEAD') return new Response(null, { headers });
        const stream = Readable.toWeb(handle.createReadStream());
        handle = undefined; // Stream owns and closes the file descriptor, including cancellation.
        return new Response(stream, { headers });
      } catch (error) {
        if (['ENOENT', 'ENOTDIR', 'ELOOP', 'EACCES'].includes(error.code)) return reply(404, 'Not found\n');
        return reply(500, 'Internal server error\n');
      } finally {
        if (handle) await handle.close().catch(() => {});
        console.log(JSON.stringify({ timestamp: new Date().toISOString(), method: request.method, path: loggedPath, status, bytes }));
      }
    },
    error() {
      return new Response('Bad request\n', { status: 400, headers: securityHeaders });
    },
  });
  const started = new Date();
  let stopping = false;
  const stop = async reason => {
    if (stopping) return;
    stopping = true;
    clearTimeout(timer);
    await server.stop(true);
    console.log(JSON.stringify({ event: 'stopped', timestamp: new Date().toISOString(), pid: process.pid, reason }));
    process.off('SIGINT', onInterrupt);
    process.off('SIGTERM', onTerminate);
  };
  const onInterrupt = () => { void stop('SIGINT'); };
  const onTerminate = () => { void stop('SIGTERM'); };
  const timer = setTimeout(() => { void stop('deadline'); }, Math.max(0, deadline - Date.now()));
  process.on('SIGINT', onInterrupt);
  process.on('SIGTERM', onTerminate);
  console.log(JSON.stringify({ event: 'started', url: `http://127.0.0.1:${server.port}`, pid: process.pid,
    start: started.toISOString(), deadline: new Date(deadline).toISOString() }));
}

main().catch(error => { console.error(error.message); process.exitCode = 1; });
