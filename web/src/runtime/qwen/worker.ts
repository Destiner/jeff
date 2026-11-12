import { Qwen2Tokenizer, env as hfEnv } from '@huggingface/transformers';
import * as ort from 'onnxruntime-web/webgpu';
import { validateDecision } from '../types';
import type { RequestRecord } from '../types';
import type { DeviceMetadata, QwenMetadata, QwenResult, Reply, Request } from './types';
import { requireValue as check } from './types';
import { ANSWERS, EMBEDDING_BYTES, LETTERS, MANIFEST_SHA, SYSTEM, WEIGHTS_SHA,
  digest, inventory, same, validateContract } from './contract';
import type { Contract, Inventory, Receipt } from './contract';

// Narrow structural types avoid depending on ambient WebGPU declarations.
type GPUFacts = { features: {has(name: string): boolean; [Symbol.iterator](): Iterator<string>};
  limits: {maxBufferSize: number; maxStorageBufferBindingSize: number}; info?: Record<string, unknown>; adapterInfo?: Record<string, unknown> };
type Device = GPUFacts & { destroy(): void; lost: Promise<unknown>; addEventListener(type: string, listener: () => void): void };
type GPU = { requestAdapter(): Promise<GPUFacts | null> };
const scope = self as unknown as { postMessage(reply: Reply): void; close(): void;
  onmessage: ((event: MessageEvent<Request>) => void) | null };
let session: ort.InferenceSession | undefined;
let tokenizer: Qwen2Tokenizer | undefined;
let specialTokens: string[] = [];
let metadata: QwenMetadata | undefined;
let device: Device | undefined;
let dead = false;
let normalDisposal = false;
let runtimeModuleUrl: string | undefined;
const requests: RequestRecord[] = [];
const gpuKernels: Record<string, number> = {};
const originalFetch = globalThis.fetch.bind(globalThis);
let allowed = new Set<string>();
const progress = (stage: string, asset: string, loadedBytes?: number, totalBytes?: number | null) =>
  scope.postMessage({kind: 'progress', event: {stage, asset, message: asset, receivedBytes: loadedBytes,
    ...(totalBytes == null ? {} : {totalBytes})}});

// Guard library fetches too; JSEP is fetched here before importing an owned blob URL.
globalThis.fetch = async (input, init) => {
  const url = new URL(typeof input === 'string' ? input : input instanceof URL ? input.href : input.url, location.href);
  check(allowed.has(url.href) && url.origin === location.origin, 'Qwen blocked non-allowlisted request');
  check(!init?.method || init.method === 'GET', 'Qwen permits GET only');
  const record: RequestRecord = {url: url.href, startedMs: performance.now(), durationMs: 0, bytes: 0, status: null, source: 'fetch'};
  requests.push(record);
  try {
    const response = await originalFetch(url.href, {...init, method: 'GET', credentials: 'omit', redirect: 'error'});
    record.status = response.status;
    check(response.ok && !response.redirected && response.url === url.href, 'Qwen asset response failed or redirected');
    const length = response.headers.get('content-length');
    const total = !response.headers.get('content-encoding') && length && /^\d+$/.test(length) ? Number(length) : null;
    progress('download', url.pathname, 0, total);
    check(response.body, 'Qwen asset has no response body');
    const reader = response.body.getReader();
    const stream = new ReadableStream<Uint8Array>({
      async pull(controller) {
        try {
          const {done, value} = await reader.read();
          if (done) { record.durationMs = performance.now() - record.startedMs; progress('download-complete', url.pathname, record.bytes!, record.bytes); controller.close(); }
          else { record.bytes! += value.byteLength; progress('download', url.pathname, record.bytes!, total); controller.enqueue(value); }
        } catch (error) { record.error = String(error); record.durationMs = performance.now() - record.startedMs; controller.error(error); }
      },
      cancel: reason => reader.cancel(reason),
    });
    return new Response(stream, {status: response.status, statusText: response.statusText, headers: response.headers});
  } catch (error) { record.error = String(error); record.durationMs = performance.now() - record.startedMs; throw error; }
};
async function bytes(url: URL, expected?: number): Promise<Uint8Array> {
  const response = await fetch(url);
  const reader = response.body!.getReader();
  if (expected !== undefined) {
    const result = new Uint8Array(expected);
    let offset = 0;
    while (true) {
      const {done, value} = await reader.read();
      if (done) break;
      if (offset + value.byteLength > expected) { await reader.cancel(); throw new Error('Asset exceeds producer byte inventory'); }
      result.set(value, offset); offset += value.byteLength;
    }
    check(offset === expected, 'Asset shorter than producer byte inventory');
    return result;
  }
  const chunks: Uint8Array[] = [];
  let length = 0;
  while (true) {
    const {done, value} = await reader.read();
    if (done) break;
    length += value.byteLength;
    if (length > 32 * 1024 * 1024) { await reader.cancel(); throw new Error('Metadata asset exceeds 32MiB bound'); }
    chunks.push(value);
  }
  const result = new Uint8Array(length);
  let offset = 0;
  for (const chunk of chunks) {result.set(chunk, offset); offset += chunk.length;}
  return result;
}
const parse = <T>(value: Uint8Array): T => JSON.parse(new TextDecoder('utf-8', {fatal: true}).decode(value)) as T;
async function verified(url: URL, entry: Inventory): Promise<Uint8Array> {
  inventory(entry);
  check(entry.bytes <= 32 * 1024 * 1024, 'Small asset exceeds bound');
  const result = await bytes(url, entry.bytes);
  check(await digest(result) === entry.sha256, 'Small asset SHA256 mismatch: ' + url.pathname);
  return result;
}
function facts(value: GPUFacts): DeviceMetadata {
  check(value.features.has('shader-f16') && value.limits.maxBufferSize >= EMBEDDING_BYTES &&
    value.limits.maxStorageBufferBindingSize >= EMBEDDING_BYTES, 'WebGPU shader-f16 or 272269312-byte binding unavailable');
  const info: Record<string, string> = {};
  for (const name of ['vendor', 'architecture', 'device', 'description']) {
    const field = (value.info ?? value.adapterInfo)?.[name]; if (typeof field === 'string') info[name] = field;
  }
  return {features: Array.from(value.features), limits: {maxBufferSize: value.limits.maxBufferSize,
    maxStorageBufferBindingSize: value.limits.maxStorageBufferBindingSize}, info, browserMemoryBytes: null};
}
async function initialize(baseUrl: string): Promise<QwenMetadata> {
  check(!session && !metadata && !dead, 'Qwen initialization is single-use');
  const started = performance.now();
  check(hfEnv.version === '3.8.1' && ort.env.versions.web === '1.22.0-dev.20250409-89f8206ba4', 'Loaded runtime version mismatch');
  const base = new URL(baseUrl, location.href);
  check(base.origin === location.origin && /^https?:$/.test(base.protocol) && !base.username && !base.password &&
    !base.search && !base.hash && base.pathname.endsWith('/'), 'Require same-origin asset directory URL ending in /');
  const names = ['receipt.json', 'export-contract.json', 'source-checkpoint-manifest.json', 'model.onnx',
    'assets/tokenizer.json', 'assets/tokenizer_config.json'];
  const wasm = new URL('/ort/ort-wasm-simd-threaded.jsep.wasm', location.href);
  const mjs = new URL('/ort/ort-wasm-simd-threaded.jsep.mjs', location.href);
  allowed = new Set([...names.map(name => new URL(name, base).href), wasm.href, mjs.href]);
  const gpu = (navigator as unknown as {gpu?: GPU}).gpu;
  check(gpu, 'Worker navigator.gpu unavailable');
  const adapter = await gpu.requestAdapter();
  check(adapter, 'Worker WebGPU adapter unavailable');
  facts(adapter);
  hfEnv.allowRemoteModels = false; hfEnv.allowLocalModels = true;
  hfEnv.useBrowserCache = false;
  const receipt = parse<Receipt>(await bytes(new URL('receipt.json', base)));
  const contract = parse<Contract>(await verified(new URL('export-contract.json', base), inventory(receipt.artifacts['export-contract.json'])));
  validateContract(contract, receipt);
  const manifestBytes = await bytes(new URL('source-checkpoint-manifest.json', base));
  check(await digest(manifestBytes) === MANIFEST_SHA, 'Pinned trained source manifest mismatch');
  const manifest = parse<{schema_version: string; kind: string; status: string; files: Record<string, Inventory>}>(manifestBytes);
  check(manifest.schema_version === 'jeff.qwen-trained-checkpoint.v1' && manifest.kind === 'trained' &&
    manifest.status === 'complete' && same(manifest.files['model.safetensors'], {sha256: WEIGHTS_SHA, bytes: 1976163472}), 'Trained M10 source binding mismatch');
  const tokenizerStarted = performance.now();
  const tokenizerJson = parse<ConstructorParameters<typeof Qwen2Tokenizer>[0]>(await verified(new URL('assets/tokenizer.json', base), inventory(manifest.files['tokenizer.json'])));
  const config = parse<ConstructorParameters<typeof Qwen2Tokenizer>[1]>(await verified(new URL('assets/tokenizer_config.json', base), inventory(manifest.files['tokenizer_config.json'])));
  check(typeof config.chat_template === 'string' && config.chat_template.length > 0, 'Original chat template required');
  tokenizer = new Qwen2Tokenizer(tokenizerJson, config);
  // HF Python all_special_tokens derives from configured special tokens, including additional tokens.
  const configured: string[] = [];
  const content = (value: unknown): string | undefined => typeof value === 'string' ? value :
    value && typeof value === 'object' && 'content' in value && typeof value.content === 'string' ? value.content : undefined;
  for (const [key, value] of Object.entries(config)) {
    if (key.endsWith('_token')) { const token = content(value); if (token) configured.push(token); }
    if (key === 'additional_special_tokens' && Array.isArray(value)) for (const item of value) {const token = content(item); if (token) configured.push(token);}
  }
  specialTokens = [...new Set([...tokenizer.special_tokens, ...configured])];
  const tokenizerLoadMs = performance.now() - tokenizerStarted;
  ort.env.wasm.numThreads = 1; ort.env.wasm.proxy = false;
  // Importing a network module directly would bypass fetch's redirect:error guard.
  const runtimeSource = await bytes(mjs);
  runtimeModuleUrl = URL.createObjectURL(new Blob([runtimeSource as Uint8Array<ArrayBuffer>], {type: 'text/javascript'}));
  ort.env.wasm.wasmPaths = {mjs: runtimeModuleUrl, wasm: wasm.href};
  const modelEntry = inventory(receipt.artifacts['model.onnx']);
  progress('model-download', 'model.onnx', 0, modelEntry.bytes);
  const model = await bytes(new URL('model.onnx', base), modelEntry.bytes);
  progress('session-initialization', 'model.onnx');
  const modelStarted = performance.now();
  ort.env.webgpu.profiling = { mode: 'default', ondata: data => {
    const key = `${data.kernelType}:${data.inputsMetadata.map(input => input.dataType).join(',')}`;
    gpuKernels[key] = (gpuKernels[key] ?? 0) + 1;
  } };
  // Shape bookkeeping may use CPU; do not select a whole-model WASM provider or retry another backend.
  session = await ort.InferenceSession.create(model, {
    executionProviders: ['webgpu'], graphOptimizationLevel: 'all',
  });
  const modelLoadMs = performance.now() - modelStarted;
  check(same(session.inputNames, ['input_ids']) && same(session.outputNames, ['logits']), 'Loaded session names mismatch');
  device = ort.env.webgpu.device as unknown as Device;
  check(device, 'ORT did not expose actual requested device');
  const deviceMetadata = facts(device);
  const actualAdapter = ort.env.webgpu.adapter as unknown as GPUFacts;
  check(actualAdapter, 'ORT did not expose actual adapter');
  const actualAdapterMetadata = facts(actualAdapter);
  const fatal = (message: string) => {
    dead = true; device?.destroy();
    scope.postMessage({kind: 'error', id: -1, message});
    scope.close();
  };
  device.lost.then(() => { if (!normalDisposal) fatal('Qwen WebGPU device lost; disposed'); });
  device.addEventListener('uncapturederror', () => fatal('Qwen WebGPU uncaptured error; disposed'));
  metadata = {backend: 'webgpu', workerBackend: 'webgpu', initializationMs: performance.now() - started,
    tokenizerLoadMs, modelLoadMs, versions: {transformers: hfEnv.version, onnxruntime: ort.env.versions.web!, browser: navigator.userAgent},
    adapter: actualAdapterMetadata, device: deviceMetadata, requests: requests.map(r => ({...r})),
    checkpointManifestSha256: MANIFEST_SHA, weightsSha256: WEIGHTS_SHA, modelBytes: modelEntry.bytes,
    modelSha256: modelEntry.sha256, modelIdentityMethod: 'Producer/copier inventory attestation and exact fetched byte count; browser does not rehash model'};
  return metadata;
}
async function predict(input: Request & {kind: 'predict'}): Promise<QwenResult> {
  check(session && tokenizer && metadata && !dead, 'Qwen engine not ready');
  const started = performance.now();
  const row = input.input;
  validateDecision(row);
  check(same(Object.keys(row).sort(), ['id', 'options', 'question', 'schema_version', 'state']) &&
    row.options.length <= 6 && row.options.every(o => same(Object.keys(o).sort(), ['id', 'text'])), 'Require decision-only fields and K2..6');
  const raw = [row.state, row.question, ...row.options.map(o => o.text)];
  check(!specialTokens.some(token => raw.some(text => text.includes(token))), 'Special-token string in raw input');
  const user = `State:\n${row.state}\n\nQuestion:\n${row.question}\n\nOptions:\n${row.options.map((o, i) => `${LETTERS[i]}. ${o.text}`).join('\n')}`;
  const renderedPrompt = tokenizer.apply_chat_template([{role: 'system', content: SYSTEM}, {role: 'user', content: user}],
    {chat_template: tokenizer.chat_template, tokenize: false, add_generation_prompt: true, truncation: false});
  check(typeof renderedPrompt === 'string', 'Chat template must render text');
  const promptTokenIds = tokenizer.encode(renderedPrompt, {add_special_tokens: false});
  check(promptTokenIds.length > 0 && promptTokenIds.length <= 1024 && promptTokenIds.every(Number.isSafeInteger), 'Complete prompt must fit 1..1024 tokens; no truncation');
  const answerTokenIds = Array.from(LETTERS, letter => {
    const complete = tokenizer!.encode(renderedPrompt + letter, {add_special_tokens: false});
    check(complete.length === promptTokenIds.length + 1 && complete.slice(0, -1).every((id, i) => id === promptTokenIds[i]), 'Answer must append exactly one token with unchanged prefix');
    return complete[complete.length - 1];
  });
  check(same(answerTokenIds, ANSWERS), 'Actual answer boundaries differ from frozen 32..37 mapping');
  const tokenizerMs = performance.now() - started;
  const tensor = new ort.Tensor('int64', BigInt64Array.from(promptTokenIds, BigInt), [1, promptTokenIds.length]);
  const inferenceStarted = performance.now();
  let output: ort.InferenceSession.ReturnType | undefined;
  let logits: number[];
  try {
    output = await session.run({input_ids: tensor});
    const values = output.logits;
    check(values && values.type === 'float32' && same(values.dims, [1, 6]) && values.data instanceof Float32Array, 'Actual output must be float32[1,6]');
    logits = Array.from(values.data);
    check(logits.length === 6 && logits.every(Number.isFinite), 'Nonfinite six logits');
  } finally {tensor.dispose(); if (output) for (const value of Object.values(output)) value.dispose();}
  const inferenceMs = performance.now() - inferenceStarted;
  const k = row.options.length;
  const selectedLogits = logits.slice(0, k);
  const maximum = Math.max(...selectedLogits);
  const exps = selectedLogits.map(value => Math.exp(value - maximum));
  const sum = exps.reduce((a, b) => a + b, 0);
  const probabilities = exps.map(value => value / sum);
  check(probabilities.every(p => Number.isFinite(p) && p >= 0 && p <= 1) &&
    Math.abs(probabilities.reduce((a, b) => a + b, 0) - 1) <= 1e-6, 'Invalid restricted T1 probabilities');
  const top = Math.max(...probabilities);
  const tiedOptionIds = row.options.filter((_, i) => probabilities[i] === top).map(o => o.id);
  return {prediction: {schema_version: '0.1', id: row.id, probabilities: row.options.map((o, i) => ({option_id: o.id, probability: probabilities[i]}))},
    diagnostics: {backend: 'webgpu', renderedPrompt, promptTokenIds, answerTokenIds, logits, selectedLogits, k,
      optionMapping: row.options.map((o, i) => ({letter: LETTERS[i], tokenId: answerTokenIds[i], optionId: o.id, text: o.text})),
      topOptionId: tiedOptionIds[0], tiedOptionIds, tokenizerMs, inferenceMs, totalMs: performance.now() - started,
      requests: requests.map(r => ({...r})), device: metadata.device,
      observedGpuKernelsCumulative: {...gpuKernels},
      placementQualification: 'WebGPU provider requested; cumulative profiler callbacks show observed GPU kernel types, not a complete CPU/GPU placement audit. Profiling overhead is included.'}};
}
async function dispose() {
  normalDisposal = true; dead = true;
  try {await session?.release();} finally {
    const actualDevice = device ?? ort.env.webgpu.device as unknown as Device | undefined;
    actualDevice?.destroy(); session = undefined; tokenizer = undefined; metadata = undefined;
    if (runtimeModuleUrl) { URL.revokeObjectURL(runtimeModuleUrl); runtimeModuleUrl = undefined; }
  }
}
let queue = Promise.resolve();
scope.onmessage = ({data}) => {
  queue = queue.then(async () => {
    try {
      check(!dead, 'Qwen worker disposed');
      const value = data.kind === 'init' ? await initialize(data.assetBaseUrl) :
        data.kind === 'predict' ? await predict(data as Request & {kind: 'predict'}) : await dispose() ?? null;
      scope.postMessage({kind: 'result', id: data.id, value});
      if (data.kind === 'dispose') scope.close();
    } catch (error) {
      try {await dispose();} catch { /* Parent termination is the final ownership boundary. */ }
      scope.postMessage({kind: 'error', id: data.id, message: error instanceof Error ? error.message : 'Qwen worker failed'});
      scope.close();
    }
  });
};
