import type { Decision, Engine, Prediction, Progress } from '@jeff/sdk';
import { model, modelLabel } from './model';

type Input = Pick<Decision, 'id' | 'state' | 'question' | 'options'>;
type Slot = { controller: AbortController; promise: Promise<Engine>; engine?: Engine };
type Receipt = { input: Decision; prediction: Prediction; engineMetadata: Engine['metadata']; wallMs: number };
export function createSession(status: HTMLElement) {
  let slot: Slot | null = null;
  let closed = false;
  let requests = 0;
  const history: Receipt[] = [];
  function show(message: string) { status.textContent = message; status.title = message; }
  show(`${modelLabel} · loads on demand`);
  function progress(event: Progress) {
    const received = event.receivedBytes;
    const total = event.totalBytes;
    show(typeof received === 'number' && Number.isFinite(received) && received >= 0
      ? `${event.message} · ${(received / 1e6).toFixed(1)}${typeof total === 'number' && Number.isFinite(total) && total > 0 && received <= total ? ` / ${(total / 1e6).toFixed(1)}` : ''} MB`
      : event.message);
  }
  function acquire(): Slot {
    if (closed) throw new Error('This page has released its model. Reload to continue.');
    if (slot) return slot;
    const controller = new AbortController();
    const next: Slot = { controller, promise: Promise.resolve().then(async () => {
      const { createEngine } = await import('@jeff/sdk');
      const engine = await createEngine({ ...model, signal: controller.signal,
        onProgress: event => { if (slot === next) progress(event); } });
      if (closed || slot !== next) { await engine.dispose(); throw new Error('Model loading cancelled.'); }
      next.engine = engine;
      return engine;
    }) };
    slot = next;
    show(`Loading ${modelLabel}…`);
    return next;
  }
  return {
    async predict(input: Input): Promise<Prediction> {
      const started = performance.now();
      const submitted: Decision = { schema_version: '0.1', id: input.id, state: input.state,
        question: input.question, options: input.options.map(({id,text}) => ({id,text})) };
      const current = acquire();
      requests++;
      try {
        const engine = await current.promise;
        if (slot === current) show('Comparing locally…');
        const prediction = await engine.predict(submitted);
        if (prediction.id !== submitted.id || prediction.schema_version !== '0.1') throw new Error('The model returned a mismatched decision.');
        history.push(structuredClone({ input: submitted, prediction, engineMetadata: engine.metadata, wallMs: performance.now() - started }));
        return prediction;
      } catch (error) {
        if (slot === current) slot = null;
        current.controller.abort();
        try { await current.engine?.dispose(); } catch { /* Keep the original prediction failure. */ }
        if (!slot && !closed) show(error instanceof Error ? error.message : 'Model unavailable');
        throw error;
      } finally {
        requests--;
        if (!requests && slot === current && current.engine) show(`${current.engine.metadata.model.label} · local`);
      }
    },
    get history(): readonly Receipt[] { return structuredClone(history); },
    getState: () => structuredClone({ closed, busy: requests > 0, initializing: !!slot && !slot.engine,
      engineReady: !!slot?.engine, engineMetadata: slot?.engine?.metadata ?? null }),
    async dispose() {
      closed = true;
      const current = slot; slot = null;
      if (!current) return;
      current.controller.abort();
      try { await (await current.promise).dispose(); } catch { /* Abort terminates the owned worker synchronously. */ }
    },
  };
}

type Session = ReturnType<typeof createSession>;
type Inspection = Pick<Session, 'history' | 'getState' | 'dispose'>;
declare global { interface Window { jeffApp?: Inspection } }
export function exposeSession(current: () => Session): void {
  window.jeffApp = { get history() { return current().history; },
    getState: () => current().getState(), dispose: () => current().dispose() };
}
