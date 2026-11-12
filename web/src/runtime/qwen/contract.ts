import { requireValue as check } from './types';
export const MANIFEST_SHA = '765d802270b8c0b090e9206c3e52f12e76ea7e224dbb4f07c9cc3c709aa6b15a';
export const WEIGHTS_SHA = '751ecdc0433b21d200af0e38966b5b28107dc9ff2267977f0eae2e936cb5131d';
export const SYSTEM = 'You are a decision assistant. Choose exactly one of the listed options. Reply with only its letter.';
export const USER = 'State:\n{state}\n\nQuestion:\n{question}\n\nOptions:\n{options}';
export const LETTERS = 'ABCDEF';
export const ANSWERS = [32, 33, 34, 35, 36, 37];
export const EMBEDDING_BYTES = 272269312;
export type Inventory = { bytes: number; sha256: string };
export type Contract = {
  input: { name: string; dtype: string; shape: (string | number)[] };
  output: { name: string; dtype: string; shape: number[]; letters: string; answer_token_ids: number[] };
  opset: number; dynamo: boolean; external_data: boolean; export_attention: string;
  backbone_dtype: string; projection_dtype: string; rotary_inv_freq_dtype: string;
  no_generation: boolean; no_kv_cache: boolean;
  actual_graph: { inputs: {name: string; element_type: number; shape: (string | number)[]}[];
    outputs: {name: string; element_type: number; shape: (string | number)[]}[];
    external_initializers: number; opsets: {domain: string; version: number}[] };
};
export type Receipt = {
  schema_version: string; status: string; stage: string; export_contract: Contract;
  binding: { checkpoint_manifest_sha256: string; weights_sha256: string; weights_bytes: number;
    system: string; user_template: string; symbols: string; native_dtype: string; native_attention: string;
    temperature: number; logits_to_keep: number; max_input_tokens: number; add_generation_prompt: boolean;
    add_special_tokens: boolean; truncation: boolean };
  artifacts: Record<string, Inventory>;
  loading_info: Record<string, unknown[]>;
  parameter_metadata: { unique_parameter_count: number; head_embedding_same_parameter: boolean;
    head_embedding_same_storage: boolean; head_shape: number[]; embedding_shape: number[]; head_bias: boolean };
  fp16_parameter_metadata: { largest_embedding_fp16_bytes: number; selected_head_dtype: string;
    selected_head_shape: number[]; native_head_embedding_still_tied: boolean };
};
export const same = (a: unknown, b: unknown) => JSON.stringify(a) === JSON.stringify(b);
export async function digest(bytes: Uint8Array): Promise<string> {
  return Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256', bytes as Uint8Array<ArrayBuffer>)), b => b.toString(16).padStart(2, '0')).join('');
}
export function inventory(value: Inventory | undefined): Inventory {
  check(value && Number.isSafeInteger(value.bytes) && value.bytes > 0 && /^[0-9a-f]{64}$/.test(value.sha256), 'Invalid producer asset inventory');
  return value;
}
export function validateContract(c: Contract, r: Receipt): void {
  check(r.schema_version === 'jeff.browser-b2.export.v1' && r.status === 'complete' &&
    r.stage === 'export_complete_browser_execution_not_performed', 'Require completed actual B2 producer receipt');
  const b = r.binding;
  check(b.checkpoint_manifest_sha256 === MANIFEST_SHA && b.weights_sha256 === WEIGHTS_SHA &&
    b.weights_bytes === 1976163472 && b.system === SYSTEM && b.user_template === USER &&
    b.symbols === LETTERS && b.native_dtype === 'float32' && b.native_attention === 'sdpa' &&
    b.temperature === 1 && b.logits_to_keep === 1 && b.max_input_tokens === 1024 &&
    b.add_generation_prompt === true && b.add_special_tokens === false && b.truncation === false,
  'M10 scientific/scoring identity mismatch');
  check(same(c, r.export_contract), 'Contract differs from producer receipt');
  check(same(c.input, {name: 'input_ids', dtype: 'int64', shape: [1, 'sequence']}) &&
    same(c.output, {name: 'logits', dtype: 'float32', shape: [1, 6], letters: LETTERS, answer_token_ids: ANSWERS}) &&
    c.opset === 17 && c.dynamo === false && c.external_data === false && c.export_attention === 'eager' &&
    c.backbone_dtype === 'float16' && c.projection_dtype === 'float16' && c.rotary_inv_freq_dtype === 'float32' &&
    c.no_generation === true && c.no_kv_cache === true, 'Frozen one-input FP16 contract mismatch');
  const g = c.actual_graph;
  check(same(g.inputs, [{name: 'input_ids', element_type: 7, shape: [1, 'sequence']}]) &&
    same(g.outputs, [{name: 'logits', element_type: 1, shape: ['Castlogits_dim_0', 6]}]) && g.external_initializers === 0 &&
    g.opsets.some(o => o.domain === '' && o.version === 17), 'Inspected actual ONNX I/O mismatch');
  check(['missing_keys', 'unexpected_keys', 'mismatched_keys', 'error_msgs'].every(k =>
    Array.isArray(r.loading_info[k]) && r.loading_info[k].length === 0), 'Strict native load diagnostics required');
  const p = r.parameter_metadata;
  check(p.unique_parameter_count === 494032768 && p.head_embedding_same_parameter === true &&
    p.head_embedding_same_storage === true && p.head_bias === false && same(p.head_shape, [151936, 896]) &&
    same(p.embedding_shape, [151936, 896]), 'Actual trained tied-head identity mismatch');
  const f = r.fp16_parameter_metadata;
  check(f.largest_embedding_fp16_bytes === EMBEDDING_BYTES && f.selected_head_dtype === 'torch.float16' &&
    same(f.selected_head_shape, [6, 896]) && f.native_head_embedding_still_tied === true, 'FP16 selected-head mismatch');
  check(inventory(r.artifacts['model.onnx']).bytes < 2_000_000_000, 'Require single-file model below 2GB');
}
