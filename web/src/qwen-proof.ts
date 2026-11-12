import { createQwenEngine } from './runtime/qwen/index';
import type { Decision } from './runtime/types';

type Engine = Awaited<ReturnType<typeof createQwenEngine>>;
let engine: Engine | null = null;
let abort: AbortController | null = null;
let generation = 0;
let busy = false;
let closing: Promise<void> | null = null;
const history: unknown[] = [];
const status = document.getElementById('state')!;

async function run(input: Decision) {
  if (busy || closing) throw new Error('The task engine is busy.');
  const current = ++generation;
  busy = true;
  const started = performance.now();
  try {
    if (!engine) {
      abort = new AbortController();
      const created = await createQwenEngine({ assetBaseUrl: '/qwen-proof/models/m10/', signal: abort.signal,
        onProgress: event => { if (current === generation) status.textContent = event.message; } });
      if (current !== generation) { await created.dispose(); throw new Error('Cancelled.'); }
      engine = created;
    }
    const active = engine;
    const output = await active.predict(structuredClone(input));
    if (current !== generation) throw new Error('Cancelled.');
    const receipt = structuredClone({ input, ...output, engineMetadata: active.metadata, wallMs: performance.now() - started });
    history.push(receipt);
    status.textContent = 'Actual task prediction complete; no normal-demo gate is implied.';
    return structuredClone(receipt);
  } catch (error) {
    if (current === generation) {
      abort?.abort();
      const failed = engine; engine = null;
      await failed?.dispose().catch(() => undefined);
      status.textContent = error instanceof Error ? error.message : String(error);
    }
    throw error;
  } finally { if (current === generation) busy = false; }
}

function dispose(): Promise<void> {
  if (closing) return closing;
  ++generation;
  abort?.abort(); abort = null;
  const active = engine; engine = null;
  closing = (async () => {
    try { await active?.dispose(); }
    finally { busy = false; closing = null; status.textContent = 'Task model released.'; }
  })();
  return closing;
}

async function create(options: Parameters<typeof createQwenEngine>[0]) {
  if (busy || closing || engine) throw new Error('The task engine is already active.');
  const current = ++generation;
  busy = true;
  const control = new AbortController();
  abort = control;
  const relay = () => control.abort();
  if (options.signal?.aborted) control.abort();
  else options.signal?.addEventListener('abort', relay, { once: true });
  try {
    const loaded = await createQwenEngine({ ...options, assetBaseUrl: '/qwen-proof/models/m10/', signal: control.signal });
    if (current !== generation) { await loaded.dispose(); throw new Error('Cancelled.'); }
    const tracked: Engine = { metadata: loaded.metadata, predict: input => loaded.predict(input), dispose: async () => {
      try { await loaded.dispose(); }
      finally { options.signal?.removeEventListener('abort', relay); if (engine === tracked) engine = null; }
    } };
    engine = tracked;
    return tracked;
  } catch (error) {
    options.signal?.removeEventListener('abort', relay);
    control.abort();
    throw error;
  } finally { if (current === generation) busy = false; }
}

const bridge = { createEngine: create, run, dispose, get history() { return structuredClone(history); },
  getState: () => ({ busy, engineMetadata: engine ? structuredClone(engine.metadata) : null }) };
declare global { interface Window { jeffQwenProof: typeof bridge } }
window.jeffQwenProof = bridge;
