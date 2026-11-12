import { access } from 'node:fs/promises';
import { execFile, spawn } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { promisify } from 'node:util';

const web = fileURLToPath(new URL('../', import.meta.url));
const log = event => console.log(JSON.stringify({ timestamp: new Date().toISOString(), ...event }));

function options() {
  const result = { port: 4173, durationSeconds: 7200 };
  const seen = new Set();
  const args = process.argv.slice(2);
  for (let i = 0; i < args.length; i += 2) {
    const flag = args[i];
    const value = args[i + 1];
    if (!['--model-dir', '--inputs', '--port', '--duration-seconds', '--stop-at'].includes(flag)
      || seen.has(flag) || !value) {
      throw new Error('Usage: bun run demo [--model-dir ABSOLUTE_ASSETS_DIR] [--inputs ABSOLUTE_P11_JSONL] [--port 1..65535] [--duration-seconds 1..14400] [--stop-at UTC_ISO_TIMESTAMP]');
    }
    seen.add(flag);
    if (flag === '--model-dir' || flag === '--inputs') {
      if (!path.isAbsolute(value)) throw new Error(`${flag} requires an absolute path`);
      result[flag] = path.resolve(value);
    } else if (flag === '--stop-at') {
      const timestamp = Date.parse(value);
      if (!/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{3})?Z$/.test(value)
        || !Number.isFinite(timestamp)
        || new Date(timestamp).toISOString() !== (value.includes('.') ? value : value.replace('Z', '.000Z'))) {
        throw new Error('Invalid --stop-at: use a UTC ISO timestamp');
      }
      if (timestamp <= Date.now()) throw new Error('--stop-at deadline has elapsed');
      result.stopAt = timestamp;
    } else {
      const max = flag === '--port' ? 65535 : 14400;
      const number = Number(value);
      if (!/^\d+$/.test(value) || !Number.isSafeInteger(number) || number < 1 || number > max) throw new Error(`Invalid ${flag}`);
      result[flag === '--port' ? 'port' : 'durationSeconds'] = number;
    }
  }
  return result;
}

async function main() {
  if (!globalThis.Bun) throw new Error('Run this launcher with Bun');
  const args = options();
  // Include preparation/build time in the finite lifetime, not just server uptime.
  const deadline = Math.min(Date.now() + args.durationSeconds * 1000, args.stopAt ?? Infinity);
  const { stdout } = await promisify(execFile)('git', ['rev-parse', '--path-format=absolute', '--git-common-dir'], {
    cwd: web, timeout: 10000, maxBuffer: 64 * 1024,
  });
  const canonical = path.dirname(stdout.trim());
  const modelDir = args['--model-dir'] ?? path.join(canonical, 'artifacts/release/browser-b1-20261112-01/export-01/assets');
  const inputs = args['--inputs'] ?? path.join(canonical, 'artifacts/infra/browser-b2-20261112-01/p11-train.jsonl');
  // Never implicitly install, download, export, or import a model.
  for (const dependency of ['@huggingface/transformers', 'onnxruntime-web', 'typescript', 'vite']) {
    try { await access(path.join(web, 'node_modules', dependency, 'package.json')); }
    catch { throw new Error(`Missing dependency ${dependency}. In ${web}, install scoped dependencies with bun install --frozen-lockfile --ignore-scripts, then retry. No install was attempted.`); }
  }

  let child;
  let interrupted;
  let escalator;
  const killTree = signal => {
    if (!child?.pid) return;
    try { process.kill(-child.pid, signal); }
    catch (error) { if (error.code !== 'ESRCH') throw error; }
  };
  const stop = reason => {
    if (interrupted) return;
    interrupted = reason;
    log({ event: 'launcher-stopping', reason, pid: process.pid, childPid: child?.pid });
    if (child) {
      killTree('SIGTERM');
      escalator = setTimeout(() => killTree('SIGKILL'), 3000);
    }
  };
  const onInterrupt = () => stop('SIGINT');
  const onTerminate = () => stop('SIGTERM');
  process.on('SIGINT', onInterrupt);
  process.on('SIGTERM', onTerminate);
  const timer = setTimeout(() => stop('deadline'), Math.max(0, deadline - Date.now()));
  const run = async (stage, commandArgs) => {
    if (interrupted || Date.now() >= deadline) throw new Error(`Launch stopped before ${stage}: ${interrupted ?? 'deadline'}`);
    // A separate POSIX process group lets us stop build shells and their children.
    // This is not a daemon: inherited terminal, no unref, foreground wrapper awaits it.
    const command = [process.execPath, ...commandArgs];
    child = spawn(command[0], command.slice(1), { cwd: web, stdio: 'inherit', detached: true });
    log({ event: 'child-started', stage, command, cwd: web, pid: child.pid,
      wrapperPid: process.pid, deadline: new Date(deadline).toISOString(),
      ...(stage === 'serve' ? { url: `http://127.0.0.1:${args.port}` } : {}) });
    const outcome = await new Promise((resolve, reject) => {
      child.once('error', reject);
      child.once('close', (code, signal) => resolve({ code, signal }));
    });
    // A build shell exiting must not leave descendants behind, even on failure.
    killTree('SIGKILL');
    child = undefined;
    clearTimeout(escalator);
    log({ event: 'child-exited', stage, ...outcome });
    if (interrupted || outcome.code !== 0) {
      const error = new Error(`${stage} stopped: ${interrupted ?? outcome.signal ?? `exit ${outcome.code}`}`);
      error.exitCode = interrupted === 'SIGINT' ? 130 : interrupted === 'SIGTERM' ? 143 : outcome.code || 1;
      throw error;
    }
  };
  try {
    log({ event: 'launcher-started', pid: process.pid, web, canonical, modelDir, inputs,
      deadline: new Date(deadline).toISOString(), dependencies: 'required; no automatic install' });
    await run('assets', ['scripts/copy-assets.mjs', '--model-dir', modelDir, '--inputs', inputs]);
    await run('build', ['run', 'build']);
    await run('serve', ['scripts/serve.mjs', '--port', String(args.port),
      '--duration-seconds', String(args.durationSeconds), '--stop-at', new Date(deadline).toISOString()]);
  } finally {
    clearTimeout(timer);
    clearTimeout(escalator);
    process.off('SIGINT', onInterrupt);
    process.off('SIGTERM', onTerminate);
    log({ event: 'launcher-stopped', pid: process.pid, reason: interrupted ?? 'child-exited' });
  }
}

main().catch(error => {
  console.error(JSON.stringify({ event: 'launcher-error', message: error.message }));
  process.exitCode = error.exitCode ?? 1;
});
