import { validateDecision } from './types';
import type { Decision, Metadata, Progress, Result, WorkerReply, WorkerRequest } from './types';
export type { Decision, Prediction, Metadata, Progress, Result, RequestRecord } from './types';

export type Engine = {
  metadata: Metadata;
  predict(input: Decision): Promise<Result>;
  dispose(): Promise<void>;
};

const INIT_MS = 120_000;
const PREDICT_MS = 60_000;
const DISPOSE_MS = 5_000;

export async function createEngine(options: {
  assetBaseUrl: string; onProgress?: (event: Progress) => void; signal?: AbortSignal;
}): Promise<Engine> {
  if (options.signal?.aborted) throw new DOMException('Engine creation aborted', 'AbortError');
  const base = new URL(options.assetBaseUrl, location.href);
  if (base.origin !== location.origin || !['http:', 'https:'].includes(base.protocol) ||
      base.username || base.password || base.search || base.hash || !base.pathname.endsWith('/')) {
    throw new Error('assetBaseUrl must be a same-origin HTTP(S) directory URL ending in /');
  }
  const worker = new Worker(new URL('./worker.ts', import.meta.url), { type: 'module' });
  let sequence = 0;
  let closed = false;
  let disposing = false;
  let disposePromise: Promise<void> | undefined;
  let queue: Promise<unknown> = Promise.resolve();
  const pending = new Map<number, {
    resolve: (value: Metadata | Result | null) => void;
    reject: (error: Error) => void; timer: ReturnType<typeof setTimeout>;
  }>();
  const abort = () => stop(new DOMException('Engine operation aborted', 'AbortError'));
  function stop(error: Error) {
    if (closed) return;
    closed = true;
    options.signal?.removeEventListener('abort', abort);
    worker.terminate();
    for (const item of pending.values()) {
      clearTimeout(item.timer);
      item.reject(error);
    }
    pending.clear();
  }
  options.signal?.addEventListener('abort', abort, { once: true });
  if (options.signal?.aborted) abort();
  worker.onerror = event => { event.preventDefault(); stop(new Error(event.message || 'Engine worker failed')); };
  worker.onmessageerror = () => stop(new Error('Engine worker message could not be decoded'));
  worker.onmessage = ({ data }: MessageEvent<WorkerReply>) => {
    if (data.kind === 'progress') {
      // A UI callback must not strand initialization or its worker.
      try { options.onProgress?.(data.event); } catch { /* caller callback is isolated */ }
      return;
    }
    const item = pending.get(data.id);
    if (!item) return;
    if (data.kind === 'error') { stop(new Error(data.message)); return; }
    clearTimeout(item.timer);
    pending.delete(data.id);
    item.resolve(data.value);
  };
  function request(message: WorkerRequest, timeoutMs: number) {
    return new Promise<Metadata | Result | null>((resolve, reject) => {
      if (closed) { reject(new Error('Engine is closed')); return; }
      const timer = setTimeout(() => stop(new Error(`Engine ${message.kind} deadline exceeded (${timeoutMs}ms)`)), timeoutMs);
      pending.set(message.id, { resolve, reject, timer });
      try { worker.postMessage(message); } catch (error) { stop(new Error(String(error))); }
    });
  }
  try {
    const metadata = await request({ kind: 'init', id: ++sequence, assetBaseUrl: base.href }, INIT_MS) as Metadata;
    return {
      metadata,
      predict(input) {
        if (closed || disposing) return Promise.reject(new Error('Engine is closed or disposing'));
        try { validateDecision(input); } catch (error) { return Promise.reject(error); }
        // Capture now so caller mutation cannot change a queued decision.
        const snapshot: Decision = {
          schema_version: '0.1', id: input.id, state: input.state, question: input.question,
          options: input.options.map(o => ({ id: o.id, text: o.text })),
        };
        const task = queue.then(async () => {
          const result = await request({ kind: 'predict', id: ++sequence, input: snapshot }, PREDICT_MS) as Result;
          metadata.requests = result.diagnostics.requests;
          return result;
        });
        queue = task;
        return task;
      },
      dispose() {
        if (disposePromise) return disposePromise;
        disposing = true;
        disposePromise = (async () => {
          let timedOut = false;
          const deadline = setTimeout(() => {
            timedOut = true;
            stop(new Error('Engine dispose deadline exceeded'));
          }, DISPOSE_MS);
          try {
            await queue.catch(() => undefined);
            if (!closed) await request({ kind: 'dispose', id: ++sequence }, DISPOSE_MS);
            if (timedOut) throw new Error('Engine dispose deadline exceeded');
          } finally {
            clearTimeout(deadline);
            stop(new Error('Engine disposed'));
          }
        })();
        return disposePromise;
      },
    };
  } catch (error) {
    stop(error instanceof Error ? error : new Error(String(error)));
    throw error;
  }
}
