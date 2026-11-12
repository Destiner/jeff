export type Decision = {
  schema_version: '0.1'; id: string; state: string; question: string;
  options: { id: string; text: string }[];
};
export type Prediction = {
  schema_version: '0.1'; id: string;
  probabilities: { option_id: string; probability: number }[];
};
export type Progress = {
  stage: string; message: string; receivedBytes?: number; totalBytes?: number;
};
export type RequestRecord = {
  url: string; startedMs: number; durationMs: number; bytes: number | null;
  status: number | null; error?: string; source: 'fetch' | 'resource';
};
export type Metadata = {
  backend: 'wasm'; workerBackend: 'wasm'; threads: 1; modelLoadMs: number;
  initializationMs: number; tokenizerLoadMs: number;
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
  { kind: 'init'; assetBaseUrl: string } | { kind: 'predict'; input: Decision } | { kind: 'dispose' }
);
export type WorkerReply =
  | { kind: 'progress'; event: Progress }
  | { kind: 'result'; id: number; value: Metadata | Result | null }
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
