import './style.css';
import type { Decision, Prediction, createEngine } from './runtime/index';

type Engine = Awaited<ReturnType<typeof createEngine>>;
type Diagnostics = Awaited<ReturnType<Engine['predict']>>['diagnostics'];
type Receipt = {
  input: Decision;
  prediction: Prediction;
  diagnostics: Diagnostics;
  engineMetadata: Engine['metadata'];
  wallMs: number;
};
type Phase = 'idle' | 'loading' | 'running' | 'success' | 'error' | 'disposing';
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
  if (busy) throw new Error('Jeff is busy. Wait for the current operation to finish.');
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
  fieldset.disabled = value;
  form.setAttribute('aria-busy', String(value));
  runButton.textContent = value ? 'Working…' : 'Run locally →';
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
      const { createEngine } = await import('./runtime/index');
      engine = await createEngine({
        assetBaseUrl: '/models/m9/',
        onProgress: event => {
          status.textContent = `${event.stage}: ${event.message}`;
        },
      });
      backend.textContent = `Backend: ${engine.metadata.backend} · Model load ${engine.metadata.modelLoadMs.toFixed(0)} ms`;
    }
    phase = 'running';
    status.textContent = 'Comparing your choices locally…';
    const output = await engine.predict(clone(submitted));
    validatePrediction(submitted, output.prediction);
    if (output.diagnostics.backend !== 'wasm' || engine.metadata.backend !== 'wasm') {
      throw new Error('Unexpected runtime backend. No scores are shown.');
    }
    const receipt: Receipt = clone({
      input: submitted,
      prediction: output.prediction,
      diagnostics: output.diagnostics,
      engineMetadata: engine.metadata,
      wallMs: performance.now() - started,
    });
    renderReceipt(receipt);
    result = receipt;
    history.push(clone(receipt));
    phase = 'success';
    status.textContent = 'Comparison complete. Executed locally with WASM.';
    return clone(receipt);
  } catch (error) {
    clearResult();
    showError(error);
    throw error;
  } finally {
    setBusy(false);
  }
}

async function dispose(): Promise<void> {
  assertIdle();
  setBusy(true);
  phase = 'disposing';
  clearResult();
  clearError();
  status.textContent = 'Releasing model…';
  try {
    if (engine) await engine.dispose();
    engine = null;
    phase = 'idle';
    backend.textContent = 'Backend: not initialized';
    status.textContent = 'Model released. Run locally to load it again.';
  } catch (error) {
    showError(error);
    throw error;
  } finally {
    setBusy(false);
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

window.jeffBrowser = {
  loadDecision,
  run,
  get history() { return clone(history); },
  dispose,
  getState: () => clone({
    phase, busy, input: draft, error: lastError,
    engineMetadata: engine?.metadata ?? null, result,
  }),
};
renderChoices();
