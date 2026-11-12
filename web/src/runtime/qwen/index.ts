import type { Decision } from '../types';
import type { QwenMetadata, QwenProgress, QwenResult, Reply, Request } from './types';
export type { QwenMetadata, QwenProgress, QwenResult } from './types';

export async function createQwenEngine({ assetBaseUrl, onProgress, signal }: {
  assetBaseUrl: string; onProgress?: (event: QwenProgress) => void; signal?: AbortSignal;
}): Promise<{ metadata: QwenMetadata; predict(input: Decision): Promise<QwenResult>; dispose(): Promise<void> }> {
  if (signal?.aborted) throw new DOMException('Qwen creation aborted', 'AbortError');
  const worker = new Worker(new URL('./worker.ts', import.meta.url), { type: 'module' });
  let nextId = 0;
  let closed = false;
  let disposing = false;
  const pending = new Map<number, { resolve(value: unknown): void; reject(error: Error): void; timer: ReturnType<typeof setTimeout> }>();
  const abort = () => stop(new DOMException('Qwen operation aborted', 'AbortError'));
  const stop = (error: Error) => {
    closed = true;
    signal?.removeEventListener('abort', abort);
    worker.terminate();
    for (const entry of pending.values()) { clearTimeout(entry.timer); entry.reject(error); }
    pending.clear();
  };
  signal?.addEventListener('abort', abort, {once: true});
  if (signal?.aborted) abort();
  worker.onerror = () => stop(new Error('Qwen worker failed; disposed, no retry'));
  worker.onmessageerror = () => stop(new Error('Qwen worker message failed; disposed'));
  worker.onmessage = ({ data }: MessageEvent<Reply>) => {
    if (closed) return;
    if (data.kind === 'progress') {
      try { onProgress?.(data.event); } catch { stop(new Error('Qwen progress callback failed; disposed')); }
      return;
    }
    if (data.kind === 'error' && data.id === -1) { stop(new Error(data.message)); return; }
    const entry = pending.get(data.id);
    if (!entry) { stop(new Error('Unexpected Qwen worker response')); return; }
    clearTimeout(entry.timer); pending.delete(data.id);
    if (data.kind === 'error') { entry.reject(new Error(data.message)); stop(new Error(data.message)); }
    else entry.resolve(data.value);
  };
  const request = <T>(body: Omit<Extract<Request, {kind: 'init'}>, 'id'> |
    Omit<Extract<Request, {kind: 'predict'}>, 'id'> | {kind: 'dispose'}, timeout: number): Promise<T> => {
    if (closed || (disposing && body.kind !== 'dispose')) return Promise.reject(new Error('Qwen engine disposed'));
    return new Promise<T>((resolve, reject) => {
      const id = ++nextId;
      const timer = setTimeout(() => stop(new Error(`Qwen ${body.kind} timed out including queued work; disposed`)), timeout);
      pending.set(id, { resolve: value => resolve(value as T), reject, timer });
      try { worker.postMessage({ ...body, id }); } catch { stop(new Error('Qwen message submission failed; disposed')); }
    });
  };
  try {
    const metadata = await request<QwenMetadata>({ kind: 'init', assetBaseUrl }, 180_000);
    let disposal: Promise<void> | undefined;
    return {
      metadata,
      predict: input => request<QwenResult>({ kind: 'predict', input }, 60_000),
      dispose: () => {
        if (disposal) return disposal;
        if (closed) return Promise.resolve();
        disposing = true;
        disposal = request<null>({ kind: 'dispose' }, 5_000).then(() => { stop(new Error('Qwen engine disposed')); });
        return disposal;
      },
    };
  } catch (error) { stop(error instanceof Error ? error : new Error('Qwen initialization failed')); throw error; }
}
