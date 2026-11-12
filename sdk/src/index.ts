import { snapshotDecision } from './types.js';
import { localDirectory } from './assets.js';
import type { Decision, DecisionInput, Prediction, Metadata, Progress, Result, WorkerReply, WorkerRequest } from './types.js';
export type { Decision, DecisionInput, Option, Prediction, Metadata, ModelDescriptor, AssetPin, Progress, Result, RequestRecord } from './types.js';

export type Engine = {
  metadata: Metadata;
  predict(input: DecisionInput): Promise<Prediction>;
  predictWithDiagnostics(input: DecisionInput): Promise<Result>;
  dispose(): Promise<void>;
};

const INIT_MS = 120_000;
const PREDICT_MS = 60_000;
const DISPOSE_MS = 5_000;

export type EngineOptions = {
  assetBaseUrl: string; ortBaseUrl: string; expectedModelId?: string;
  onProgress?: (event: Progress) => void; signal?: AbortSignal;
};

export async function createEngine(options: EngineOptions): Promise<Engine> {
  if (typeof window === 'undefined' || typeof Worker === 'undefined' || !globalThis.isSecureContext) {
    throw new Error('Jeff requires a secure browser context with module workers (HTTPS or localhost)');
  }
  if (options.signal?.aborted) throw new DOMException('Engine creation aborted', 'AbortError');
  const base = localDirectory(options.assetBaseUrl, location.origin, location.href);
  const ortBase = localDirectory(options.ortBaseUrl, location.origin, location.href);
  if (options.expectedModelId !== undefined &&
      (typeof options.expectedModelId !== 'string' || !options.expectedModelId.trim())) {
    throw new Error('expectedModelId must be a nonempty string when supplied');
  }
  const workerUrl = new URL('./worker.js', import.meta.url);
  const worker = new Worker(workerUrl, { type: 'module' });
  let sequence = 0;
  let closed = false;
  let disposing = false;
  let disposePromise: Promise<void> | undefined;
  let queue: Promise<unknown> = Promise.resolve();
  const pending = new Map<number, {
    resolve: (value: Metadata | Prediction | Result | null) => void;
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
    return new Promise<Metadata | Prediction | Result | null>((resolve, reject) => {
      if (closed) { reject(new Error('Engine is closed')); return; }
      const timer = setTimeout(() => stop(new Error(`Engine ${message.kind} deadline exceeded (${timeoutMs}ms)`)), timeoutMs);
      pending.set(message.id, { resolve, reject, timer });
      try { worker.postMessage(message); } catch (error) { stop(new Error(String(error))); }
    });
  }
  try {
    const metadata = await request({ kind: 'init', id: ++sequence, assetBaseUrl: base.href,
      ortBaseUrl: ortBase.href, expectedModelId: options.expectedModelId }, INIT_MS) as Metadata;
    function run(input: DecisionInput, diagnostics: boolean): Promise<Prediction | Result> {
      if (closed || disposing) return Promise.reject(new Error('Engine is closed or disposing'));
      let snapshot: Decision;
      // Capture before queueing so later caller mutation cannot change the decision.
      try { snapshot = snapshotDecision(input); } catch (error) { return Promise.reject(error); }
      const task = queue.then(async () => {
        const result = await request({ kind: 'predict', id: ++sequence, input: snapshot, diagnostics }, PREDICT_MS) as Prediction | Result;
        if ('diagnostics' in result) metadata.requests = result.diagnostics.requests;
        return result;
      });
      queue = task;
      // Observe internally while leaving the original rejecting promise with the caller.
      void task.catch(() => undefined);
      return task;
    }
    return {
      metadata,
      predict: input => run(input, false) as Promise<Prediction>,
      predictWithDiagnostics: input => run(input, true) as Promise<Result>,
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
