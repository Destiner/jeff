export type Option = { id: string; text: string };
export type Decision = {
  schema_version: '0.1'; id: string; state: string; question: string;
  options: Option[];
};
export type DecisionInput = {
  schema_version?: '0.1'; id?: string; state?: string; question: string;
  options: readonly Option[] | readonly string[];
};
export type Prediction = {
  schema_version: '0.1'; id: string;
  probabilities: { option_id: string; probability: number }[];
};
export type Progress = {
  stage: string; message: string; receivedBytes?: number; totalBytes?: number;
};
export type AssetPin = { bytes: number; sha256: string };
export type ModelDescriptor = {
  schema_version: 'jeff.browser-encoder.v1'; id: string; label: string;
  checkpoint_sha256: string; format: 'state-question-candidate-v1';
  precision: 'fp32'; max_pair_tokens: 256; scoring: 'softmax-t1';
  files: Record<'model.onnx' | 'tokenizer.json' | 'tokenizer_config.json', AssetPin>;
};
export type RequestRecord = {
  url: string; startedMs: number; durationMs: number; bytes: number | null;
  status: number | null; error?: string; source: 'fetch' | 'resource';
};
export type Metadata = {
  backend: 'wasm'; workerBackend: 'wasm'; threads: 1; model: ModelDescriptor;
  modelLoadMs: number; initializationMs: number; tokenizerLoadMs: number;
  versions: { transformers: string; onnxruntime: string; browser: string };
  requests: RequestRecord[];
};
export type Result = {
  prediction: Prediction;
  diagnostics: {
    backend: 'wasm'; tokenization: {
      input_ids: number[][]; attention_mask: number[][]; token_type_ids: number[][];
    }; logits: number[]; inferenceMs: number; tokenizerMs: number; totalMs: number;
    requests: RequestRecord[];
  };
};
export type WorkerRequest = { id: number } & (
  { kind: 'init'; assetBaseUrl: string; ortBaseUrl: string; expectedModelId?: string } |
  { kind: 'predict'; input: Decision; diagnostics: boolean } | { kind: 'dispose' }
);
export type WorkerReply =
  | { kind: 'progress'; event: Progress }
  | { kind: 'result'; id: number; value: Metadata | Prediction | Result | null }
  | { kind: 'error'; id: number; message: string };

export function validateDecision(value: Decision): void {
  const text = (x: unknown) => typeof x === 'string' && x.trim().length > 0;
  if (!value || value.schema_version !== '0.1' || !text(value.id) ||
      typeof value.state !== 'string' || !text(value.question) ||
      !Array.isArray(value.options) || value.options.length < 2 ||
      value.options.some(o => !o || !text(o.id) || !text(o.text)) ||
      new Set(value.options.map(o => o.id)).size !== value.options.length) {
    throw new Error('Invalid v0.1 decision: require id, state, question and at least two uniquely identified options');
  }
}

export function snapshotDecision(input: DecisionInput): Decision {
  if (!input || !Array.isArray(input.options) ||
      (!input.options.every(o => typeof o === 'string') &&
       !input.options.every(o => o !== null && typeof o === 'object'))) {
    throw new Error('Options must be either strings or explicit {id, text} objects');
  }
  const value: Decision = {
    schema_version: input.schema_version === undefined ? '0.1' : input.schema_version,
    id: input.id === undefined ? `sdk:${crypto.randomUUID()}` : input.id,
    state: input.state === undefined ? '' : input.state,
    question: input.question,
    options: input.options.map((o, i) => typeof o === 'string'
      ? { id: `option-${i + 1}`, text: o } : { id: o.id, text: o.text }),
  };
  validateDecision(value);
  return value;
}
