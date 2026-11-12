import './style.css';
import { initializeOffline, prepareOffline, readOfflineStatus, type OfflineStatus } from './offline';
import type { Decision, Prediction, Progress, createEngine } from './runtime/index';

type Engine = Awaited<ReturnType<typeof createEngine>>;
type Diagnostics = Awaited<ReturnType<Engine['predict']>>['diagnostics'];
type Receipt = {
  input: Decision;
  prediction: Prediction;
  diagnostics: Diagnostics;
  engineMetadata: Engine['metadata'];
  wallMs: number;
};
type Phase = 'idle' | 'loading' | 'running' | 'success' | 'error' | 'disposing' | 'saving-offline';
type BrowserState = {
  phase: Phase;
  busy: boolean;
  input: Decision;
  error: string | null;
  engineMetadata: Engine['metadata'] | null;
  result: Receipt | null;
};
type BrowserBridge = {
  loadDecision(input: Decision): void;
  run(input?: Decision): Promise<Receipt>;
  readonly history: readonly Receipt[];
  dispose(): Promise<void>;
  offline: { prepare(): Promise<OfflineStatus>; status(): Promise<OfflineStatus> };
  getState(): BrowserState;
};

declare global {
  interface Window {
    jeffBrowser: BrowserBridge;
  }
}

function element<T extends HTMLElement>(id: string): T {
  const node = document.getElementById(id);
  if (!node) throw new Error(`Missing app element: ${id}`);
  return node as T;
}

const form = element<HTMLFormElement>('decision-form');
const fieldset = element<HTMLFieldSetElement>('inputs');
const context = element<HTMLTextAreaElement>('context');
const question = element<HTMLTextAreaElement>('question');
const choices = element<HTMLDivElement>('choices');
const addButton = element<HTMLButtonElement>('add-choice');
const runButton = element<HTMLButtonElement>('run');
const status = element<HTMLParagraphElement>('status');
const errorBox = element<HTMLParagraphElement>('error');
const backend = element<HTMLSpanElement>('backend');
const results = element<HTMLElement>('results');
const emptyResults = element<HTMLDivElement>('empty-results');
const scores = element<HTMLOListElement>('scores');
const modelProgress = element<HTMLProgressElement>('model-progress');
const modelProgressText = element<HTMLParagraphElement>('model-progress-text');
const offlineButton = element<HTMLButtonElement>('prepare-offline');
const offlineStatusText = element<HTMLParagraphElement>('offline-status');
const offlineProgress = element<HTMLProgressElement>('offline-progress');
const offlineDetail = element<HTMLParagraphElement>('offline-detail');
let offlineState: OfflineStatus = { state: 'empty', message: 'Checking offline storage…' };
let cacheBusy = false;
let operation = 0;
let initializationAbort: AbortController | null = null;
let disposalPromise: Promise<void> | null = null;
let draft: Decision = {
  schema_version: '0.1', id: crypto.randomUUID(), state: '', question: '',
  options: [newOption(), newOption()],
};
let engine: Engine | null = null;
let busy = false;
let phase: Phase = 'idle';
let lastError: string | null = null;
let result: Receipt | null = null;
const history: Receipt[] = [];
const clone = <T>(value: T): T => structuredClone(value);

function newOption(): Decision['options'][number] {
  return { id: crypto.randomUUID(), text: '' };
}

function assertIdle(): void {
  if (busy || cacheBusy) throw new Error('Jeff is busy. Wait for the current operation to finish.');
}

function validateDecision(input: Decision): void {
  if (!input || input.schema_version !== '0.1' || typeof input.id !== 'string' || !input.id.trim()) {
    throw new Error('A decision needs schema version 0.1 and a nonempty ID.');
  }
  if (typeof input.state !== 'string' || typeof input.question !== 'string' || !input.question.trim()) {
    throw new Error('Enter a question. Context may be empty.');
  }
  if (!Array.isArray(input.options) || input.options.length < 2 || input.options.length > 6) {
    throw new Error('Supply between two and six choices.');
  }
  const ids = new Set<string>();
  for (const option of input.options) {
    if (!option || typeof option.id !== 'string' || !option.id.trim() || ids.has(option.id)) {
      throw new Error('Each choice needs a unique, nonempty ID.');
    }
    if (typeof option.text !== 'string' || !option.text.trim()) {
      throw new Error('Enter text for every choice, or remove empty choices.');
    }
    ids.add(option.id);
  }
}

function validatePrediction(input: Decision, prediction: Prediction): void {
  if (!prediction || prediction.schema_version !== '0.1' || prediction.id !== input.id ||
      !Array.isArray(prediction.probabilities) || prediction.probabilities.length !== input.options.length) {
    throw new Error('The model returned an invalid prediction. No scores are shown.');
  }
  const expected = new Set(input.options.map(option => option.id));
  let sum = 0;
  for (const entry of prediction.probabilities) {
    if (!entry || !expected.delete(entry.option_id) || typeof entry.probability !== 'number' ||
        !Number.isFinite(entry.probability) || entry.probability < 0 || entry.probability > 1) {
      throw new Error('The model returned invalid choice IDs or scores. No scores are shown.');
    }
    sum += entry.probability;
  }
  if (expected.size || Math.abs(sum - 1) > 1e-6) {
    throw new Error('The model scores do not sum to one. No scores are shown.');
  }
}

function clearResult(): void {
  result = null;
  results.hidden = true;
  emptyResults.hidden = false;
  scores.replaceChildren();
}

function clearError(): void {
  lastError = null;
  errorBox.hidden = true;
  errorBox.textContent = '';
}

function showError(error: unknown): void {
  phase = 'error';
  lastError = error instanceof Error ? error.message : 'Something went wrong. Please try again.';
  errorBox.textContent = lastError;
  errorBox.hidden = false;
  status.textContent = 'Unable to compare. Resolve the error below and run again.';
}

function edited(regenerateId = true): void {
  if (regenerateId) draft.id = crypto.randomUUID();
  clearResult();
  clearError();
  phase = 'idle';
  status.textContent = engine ? 'Model ready. Run to compare your updated choices.' : 'Model not loaded.';
}

function renderChoices(): void {
  choices.replaceChildren();
  draft.options.forEach((option, index) => {
    const row = document.createElement('div');
    row.className = 'choice-row';
    const label = document.createElement('label');
    label.textContent = `Choice ${index + 1}`;
    const input = document.createElement('textarea');
    input.id = `choice-${index}`;
    input.rows = 2;
    input.required = true;
    input.value = option.text;
    input.placeholder = 'Describe this choice';
    label.htmlFor = input.id;
    input.addEventListener('input', () => {
      option.text = input.value;
      edited();
    });
    const remove = document.createElement('button');
    remove.type = 'button';
    remove.className = 'remove-choice';
    remove.textContent = 'Remove';
    remove.setAttribute('aria-label', `Remove choice ${index + 1}`);
    remove.disabled = draft.options.length <= 2;
    remove.addEventListener('click', () => {
      assertIdle();
      draft.options = draft.options.filter(item => item.id !== option.id);
      edited();
      renderChoices();
      addButton.focus();
    });
    row.append(label, input, remove);
    choices.append(row);
  });
  element('choice-count').textContent = `${draft.options.length} of 6`;
  addButton.disabled = draft.options.length >= 6;
}

function loadDecision(input: Decision): void {
  assertIdle();
  validateDecision(input);
  // Retain caller IDs and exact text, without importing labels or other metadata.
  draft = {
    schema_version: '0.1', id: input.id, state: input.state, question: input.question,
    options: input.options.map(({ id, text }) => ({ id, text })),
  };
  context.value = draft.state;
  question.value = draft.question;
  edited(false);
  renderChoices();
}

function setBusy(value: boolean): void {
  busy = value;
  fieldset.disabled = value || cacheBusy;
  offlineButton.disabled = value || cacheBusy || offlineState.state === 'unsupported';
  form.setAttribute('aria-busy', String(value || cacheBusy));
  runButton.textContent = value ? 'Working…' : cacheBusy ? 'Saving offline…' : 'Run locally →';
}

function bytes(value: number): string { return `${(value / 1_000_000).toFixed(1)} MB`; }

function updateProgress(bar: HTMLProgressElement, loaded?: number, total?: number): void {
  if (typeof loaded === 'number' && Number.isFinite(loaded) && loaded >= 0 &&
      typeof total === 'number' && Number.isFinite(total) && total > 0 && loaded <= total) {
    bar.max = total;
    bar.value = loaded;
  } else {
    bar.removeAttribute('value');
  }
}

function loadingProgress(event: Progress): void {
  status.textContent = event.message;
  modelProgress.hidden = false;
  updateProgress(modelProgress, event.receivedBytes, event.totalBytes);
  modelProgressText.hidden = event.receivedBytes === undefined;
  modelProgressText.textContent = event.receivedBytes === undefined ? '' :
    `${bytes(event.receivedBytes)}${event.totalBytes === undefined ? ' read' : ` of ${bytes(event.totalBytes)} read`} · current asset`;
}

function renderOffline(value: OfflineStatus): void {
  offlineState = clone(value);
  offlineStatusText.textContent = value.message;
  offlineProgress.hidden = value.state !== 'preparing';
  updateProgress(offlineProgress, value.loadedBytes, value.totalBytes);
  offlineButton.textContent = value.state === 'ready' ? 'Refresh offline copy' : 'Make M9 available offline';
  offlineButton.disabled = busy || cacheBusy || value.state === 'unsupported';
  offlineDetail.textContent = value.state === 'preparing' && value.loadedBytes !== undefined
    ? `${bytes(value.loadedBytes)}${value.totalBytes === undefined ? ' saved' : ` of ${bytes(value.totalBytes)} saved`} · app and M9 assets only`
    : 'Only app and model assets are saved. Your inputs and results stay in memory.';
}

async function saveOffline(): Promise<OfflineStatus> {
  assertIdle();
  cacheBusy = true;
  phase = 'saving-offline';
  setBusy(false);
  try {
    await prepareOffline(renderOffline);
    return clone(offlineState);
  } finally {
    cacheBusy = false;
    phase = result ? 'success' : 'idle';
    setBusy(false);
  }
}

function renderReceipt(receipt: Receipt): void {
  const probabilities = new Map(receipt.prediction.probabilities.map(item => [item.option_id, item.probability]));
  const highest = Math.max(...probabilities.values());
  const leaders = receipt.input.options.filter(option => probabilities.get(option.id) === highest);
  element('result-summary').textContent = leaders.length > 1
    ? `Exact tie for highest score: ${leaders.map(option => option.text).join(' / ')}`
    : `Highest score: ${leaders[0].text}`;
  scores.replaceChildren();
  for (const option of receipt.input.options) {
    const probability = probabilities.get(option.id)!;
    const row = document.createElement('li');
    const heading = document.createElement('div');
    heading.className = 'score-heading';
    const text = document.createElement('span');
    text.textContent = option.text;
    const value = document.createElement('span');
    value.className = 'score-value';
    value.textContent = `${(probability * 100).toFixed(2)}%`;
    value.title = String(probability);
    heading.append(text, value);
    const meter = document.createElement('meter');
    meter.min = 0;
    meter.max = 1;
    meter.value = probability;
    meter.setAttribute('aria-label', `Score for ${option.text}`);
    row.append(heading, meter);
    scores.append(row);
  }
  element('timing').textContent = `WASM · Inference ${receipt.diagnostics.inferenceMs.toFixed(0)} ms · This run ${receipt.wallMs.toFixed(0)} ms (includes model loading if needed)`;
  results.hidden = false;
  emptyResults.hidden = true;
}

async function run(input?: Decision): Promise<Receipt> {
  assertIdle();
  const current = ++operation;
  const started = performance.now();
  clearResult();
  clearError();
  try {
    if (input !== undefined) loadDecision(input);
    validateDecision(draft);
    const submitted = clone(draft);
    setBusy(true);
    if (!engine) {
      phase = 'loading';
      status.textContent = 'Loading M9 reference model…';
      initializationAbort = new AbortController();
      const signal = initializationAbort.signal;
      const { createEngine } = await import('./runtime/index');
      if (signal.aborted || current !== operation) throw new Error('Model loading cancelled.');
      const options = {
        assetBaseUrl: '/models/m9/', signal,
        onProgress: (event: Progress) => { if (current === operation) loadingProgress(event); },
      };
      const loaded = await createEngine(options);
      if (current !== operation) { await loaded.dispose(); throw new Error('Model loading cancelled.'); }
      engine = loaded;
      initializationAbort = null;
      backend.textContent = `Backend: ${engine.metadata.backend} · ONNX session ${engine.metadata.modelLoadMs.toFixed(0)} ms`;
    }
    const active = engine;
    phase = 'running';
    modelProgress.hidden = true;
    modelProgressText.hidden = true;
    status.textContent = 'Comparing your choices locally…';
    const output = await active.predict(clone(submitted));
    if (current !== operation) throw new Error('Comparison cancelled.');
    validatePrediction(submitted, output.prediction);
    if (output.diagnostics.backend !== 'wasm' || active.metadata.backend !== 'wasm') {
      throw new Error('Unexpected runtime backend. No scores are shown.');
    }
    const receipt: Receipt = clone({
      input: submitted,
      prediction: output.prediction,
      diagnostics: output.diagnostics,
      engineMetadata: active.metadata,
      wallMs: performance.now() - started,
    });
    renderReceipt(receipt);
    result = receipt;
    history.push(clone(receipt));
    phase = 'success';
    status.textContent = 'Comparison complete. Executed locally with WASM.';
    return clone(receipt);
  } catch (error) {
    if (current === operation) {
      initializationAbort?.abort();
      initializationAbort = null;
      const failed = engine;
      engine = null;
      try { await failed?.dispose(); } catch (cleanupError) {
        console.error('Model cleanup reported an error', cleanupError);
      }
      backend.textContent = 'Backend: not initialized';
      clearResult();
      showError(error);
    }
    throw error;
  } finally {
    if (current === operation) {
      modelProgress.hidden = true;
      modelProgressText.hidden = true;
      setBusy(false);
    }
  }
}

async function dispose(): Promise<void> {
  if (disposalPromise) return disposalPromise;
  const pending = disposeCurrent();
  disposalPromise = pending;
  try { await pending; }
  finally { if (disposalPromise === pending) disposalPromise = null; }
}

async function disposeCurrent(): Promise<void> {
  const current = ++operation;
  initializationAbort?.abort();
  initializationAbort = null;
  const closing = engine;
  engine = null;
  setBusy(true);
  phase = 'disposing';
  clearError();
  modelProgress.hidden = true;
  modelProgressText.hidden = true;
  status.textContent = 'Releasing model…';
  try {
    await closing?.dispose();
    if (current !== operation) return;
    phase = 'idle';
    backend.textContent = 'Backend: not initialized';
    status.textContent = result
      ? 'Model released. Last comparison retained; run again to reload.'
      : 'Model released. Run locally to load it again.';
  } catch (error) {
    if (current === operation) showError(error);
    throw error;
  } finally {
    if (current === operation) setBusy(false);
  }
}

context.addEventListener('input', () => { draft.state = context.value; edited(); });
question.addEventListener('input', () => { draft.question = question.value; edited(); });
addButton.addEventListener('click', () => {
  assertIdle();
  if (draft.options.length >= 6) return;
  draft.options.push(newOption());
  edited();
  renderChoices();
  choices.querySelector<HTMLTextAreaElement>('.choice-row:last-child textarea')?.focus();
});
form.addEventListener('submit', event => {
  event.preventDefault();
  // The shared run path renders errors; consume the button's rejected promise.
  void run().catch(() => {});
});

offlineButton.addEventListener('click', () => { void saveOffline().catch(error => {
  renderOffline({ state: 'error', message: error instanceof Error ? error.message : String(error) });
}); });

window.jeffBrowser = {
  loadDecision,
  run,
  get history() { return clone(history); },
  dispose,
  offline: { prepare: saveOffline, status: async () => {
    const state = await readOfflineStatus();
    renderOffline(state);
    return clone(state);
  } },
  getState: () => clone({
    phase, busy, input: draft, error: lastError,
    engineMetadata: engine?.metadata ?? null, result,
  }),
};
renderChoices();
void initializeOffline(renderOffline);
