/// <reference lib="webworker" />
import { BertTokenizer, env } from '@huggingface/transformers';
import * as ort from 'onnxruntime-web/wasm';
import { validateDecision } from './types.js';
import type { Decision, Metadata, Progress, RequestRecord, Result, WorkerReply, WorkerRequest } from './types.js';

const scope = self as unknown as DedicatedWorkerGlobalScope;
const send = (reply: WorkerReply) => scope.postMessage(reply);
const progress = (stage: string, message: string) => send({ kind: 'progress', event: { stage, message } });
let assetProgress = new Map<string, Pick<Progress, 'stage' | 'message'>>();
let session: ort.InferenceSession | undefined;
let tokenizer: BertTokenizer | undefined;
let special: { cls: number; sep: number; pad: number };
const records: RequestRecord[] = [];
let allowed = new Set<string>();
const originalFetch = globalThis.fetch.bind(globalThis);

// Worker-local restriction: no Model Hub, CDN, redirects, credentials or cache API.
globalThis.fetch = async (input, init) => {
  const url = new URL(input instanceof Request ? input.url : String(input), scope.location.href);
  if (url.origin !== scope.location.origin || !allowed.has(url.href)) {
    throw new Error(`Asset request outside local allowlist: ${url.pathname}`);
  }
  const record: RequestRecord = {
    url: url.href, startedMs: performance.now(), durationMs: 0,
    bytes: null, status: null, source: 'fetch',
  };
  records.push(record);
  try {
    const response = await originalFetch(url.href, {
      ...init, cache: 'no-store', credentials: 'omit', redirect: 'error', mode: 'same-origin',
    });
    record.status = response.status;
    const asset = assetProgress.get(url.href);
    const length = response.headers.get('content-length');
    const encoding = response.headers.get('content-encoding');
    let totalBytes = length !== null && /^\d+$/.test(length) &&
      (encoding === null || encoding.trim().toLowerCase() === 'identity') &&
      Number.isSafeInteger(Number(length)) && Number(length) > 0 ? Number(length) : undefined;
    let receivedBytes = 0;
    const report = () => {
      if (totalBytes !== undefined && receivedBytes > totalBytes) totalBytes = undefined;
      if (asset) send({ kind: 'progress', event: {
        ...asset, receivedBytes, ...(totalBytes === undefined ? {} : { totalBytes }),
      } });
    };
    report();
    // Count actual response-body bytes; a service worker/cache may supply them without network I/O.
    let body: Uint8Array<ArrayBuffer>;
    if (response.body) {
      const reader = response.body.getReader();
      const chunks: Uint8Array[] = [];
      try {
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;
          chunks.push(value);
          receivedBytes += value.byteLength;
          record.bytes = receivedBytes;
          report();
        }
      } finally {
        reader.releaseLock();
      }
      body = new Uint8Array(receivedBytes);
      let offset = 0;
      for (const chunk of chunks) { body.set(chunk, offset); offset += chunk.byteLength; }
    } else {
      body = new Uint8Array(await response.arrayBuffer());
      receivedBytes = body.byteLength;
      report();
    }
    if (totalBytes !== undefined && receivedBytes !== totalBytes) {
      totalBytes = undefined;
      report();
    }
    record.bytes = body.byteLength;
    record.durationMs = performance.now() - record.startedMs;
    if (!response.ok) throw new Error(`Asset HTTP ${response.status}: ${url.pathname}`);
    return new Response(body, { status: response.status, statusText: response.statusText, headers: response.headers });
  } catch (error) {
    record.durationMs = performance.now() - record.startedMs;
    record.error = String(error);
    throw error;
  }
};

function requests(): RequestRecord[] {
  const result = records.map(record => ({ ...record }));
  // Dynamic .mjs imports bypass fetch(); Resource Timing is best-effort, not a network audit.
  for (const entry of performance.getEntriesByType('resource') as PerformanceResourceTiming[]) {
    if (allowed.has(entry.name) && !result.some(r => r.url === entry.name)) {
      result.push({ url: entry.name, startedMs: entry.startTime, durationMs: entry.duration,
        bytes: entry.encodedBodySize || null, status: null, source: 'resource' });
    }
  }
  return result;
}

async function initialize(assetBaseUrl: string): Promise<Metadata> {
  const start = performance.now();
  const base = new URL(assetBaseUrl, scope.location.href);
  if (base.origin !== scope.location.origin || !['http:', 'https:'].includes(base.protocol) ||
      base.search || base.hash || base.username || base.password || !base.pathname.endsWith('/')) {
    throw new Error('Invalid same-origin asset directory');
  }
  const modelUrl = new URL('model.onnx', base).href;
  const tokenizerUrl = new URL('tokenizer.json', base).href;
  const configUrl = new URL('tokenizer_config.json', base).href;
  const wasmUrl = new URL('/ort/ort-wasm-simd-threaded.wasm', base).href;
  const mjsUrl = new URL('/ort/ort-wasm-simd-threaded.mjs', base).href;
  allowed = new Set([modelUrl, tokenizerUrl, configUrl, wasmUrl, mjsUrl]);
  assetProgress = new Map([
    [modelUrl, { stage: 'model', message: 'Reading local FP32 model asset' }],
    [tokenizerUrl, { stage: 'tokenizer', message: 'Reading local BERT tokenizer asset' }],
    [configUrl, { stage: 'tokenizer', message: 'Reading local BERT tokenizer configuration' }],
  ]);
  env.allowRemoteModels = false;
  env.allowLocalModels = true;
  env.useBrowserCache = false;
  env.useFSCache = false;
  env.useCustomCache = false;
  if (env.version !== '3.8.1' || ort.env.versions.web !== '1.22.0-dev.20250409-89f8206ba4') {
    throw new Error('Runtime dependency versions differ from the B1 pinned contract');
  }
  ort.env.wasm.numThreads = 1;
  ort.env.wasm.proxy = false;
  ort.env.wasm.wasmPaths = { wasm: wasmUrl, mjs: mjsUrl };
  progress('tokenizer', 'Loading original local BERT tokenizer');
  const tokenizerStart = performance.now();
  const json = await (await fetch(tokenizerUrl)).json();
  const config = await (await fetch(configUrl)).json();
  if (json.model?.type !== 'WordPiece' || json.normalizer?.type !== 'BertNormalizer' ||
      json.pre_tokenizer?.type !== 'BertPreTokenizer' ||
      (config.padding_side && config.padding_side !== 'right') ||
      (config.truncation_side && config.truncation_side !== 'right')) {
    throw new Error('Unsupported tokenizer: require original right-padded/right-truncated BERT WordPiece');
  }
  const vocab = json.model.vocab;
  special = { cls: vocab['[CLS]'], sep: vocab['[SEP]'], pad: vocab['[PAD]'] };
  if (!Object.values(special).every(id => Number.isSafeInteger(id) && id >= 0)) {
    throw new Error('Original BERT special token IDs missing');
  }
  const processor = json.post_processor;
  if (processor?.type === 'TemplateProcessing') {
    const pair = processor.pair;
    const expected: Record<string, { id: string; type_id: number }>[] = [
      { SpecialToken: { id: '[CLS]', type_id: 0 } },
      { Sequence: { id: 'A', type_id: 0 } },
      { SpecialToken: { id: '[SEP]', type_id: 0 } },
      { Sequence: { id: 'B', type_id: 1 } },
      { SpecialToken: { id: '[SEP]', type_id: 1 } },
    ];
    // Compare structure, not JSON key ordering.
    if (!Array.isArray(pair) || pair.length !== expected.length || pair.some((item: Record<string, { id: string; type_id: number }>, i: number) => {
      const key = Object.keys(expected[i])[0] as 'SpecialToken' | 'Sequence';
      const wanted = expected[i][key];
      return Object.keys(item).length !== 1 || item[key]?.id !== wanted.id || item[key]?.type_id !== wanted.type_id;
    })) throw new Error('Unsupported BERT pair template');
  } else if (processor?.type !== 'BertProcessing' || processor.cls?.[0] !== '[CLS]' ||
      processor.cls?.[1] !== special.cls || processor.sep?.[0] !== '[SEP]' || processor.sep?.[1] !== special.sep) {
    throw new Error('Unsupported BERT pair processor');
  }
  tokenizer = new BertTokenizer(json, config);
  const tokenizerLoadMs = performance.now() - tokenizerStart;
  progress('model', 'Loading local FP32 model asset');
  const model = await (await fetch(modelUrl)).arrayBuffer();
  progress('session', 'Initializing single-thread WASM session');
  const modelStart = performance.now();
  session = await ort.InferenceSession.create(model, { executionProviders: ['wasm'] });
  const modelLoadMs = performance.now() - modelStart;
  if (session.inputNames.length !== 3 || !['input_ids', 'attention_mask', 'token_type_ids'].every(name => session!.inputNames.includes(name)) ||
      session.outputNames.length !== 1 || session.outputNames[0] !== 'logits') {
    throw new Error('Unexpected ONNX input/output contract');
  }
  progress('ready', 'Local model initialized');
  return {
    backend: 'wasm', workerBackend: 'wasm', threads: 1, modelLoadMs,
    tokenizerLoadMs, initializationMs: performance.now() - start,
    versions: { transformers: env.version, onnxruntime: ort.env.versions.web,
      browser: scope.navigator.userAgent }, requests: requests(),
  };
}

async function predict(input: Decision): Promise<Result> {
  validateDecision(input);
  if (!session || !tokenizer) throw new Error('Engine is not initialized');
  const start = performance.now();
  const first = tokenizer.encode(`State:\n${input.state}\nQuestion:\n${input.question}`, { add_special_tokens: false });
  const input_ids: number[][] = [];
  const token_type_ids: number[][] = [];
  for (const option of input.options) {
    const a = first.slice();
    const b = tokenizer.encode(`Candidate:\n${option.text}`, { add_special_tokens: false });
    if (a.length + b.length + 3 > 256) {
      throw new Error('Input exceeds the M9 limit of 256 tokens per encoded candidate pair; shorten the state, question or options');
    }
    input_ids.push([special.cls, ...a, special.sep, ...b, special.sep]);
    token_type_ids.push([...new Array(a.length + 2).fill(0), ...new Array(b.length + 1).fill(1)]);
  }
  const longest = Math.max(...input_ids.map(row => row.length));
  const attention_mask = input_ids.map((row, i) => {
    const mask = [...new Array(row.length).fill(1), ...new Array(longest - row.length).fill(0)];
    token_type_ids[i].push(...new Array(longest - row.length).fill(0));
    row.push(...new Array(longest - row.length).fill(special.pad));
    return mask;
  });
  const tokenization = { input_ids, attention_mask, token_type_ids };
  const feeds: Record<string, ort.Tensor> = {};
  for (const [name, rows] of Object.entries(tokenization)) {
    feeds[name] = new ort.Tensor('int64', BigInt64Array.from(rows.flat(), n => BigInt(n)), [input.options.length, longest]);
  }
  const tokenizerMs = performance.now() - start;
  const inferenceStart = performance.now();
  let outputs: ort.InferenceSession.ReturnType | undefined;
  try {
    outputs = await session.run(feeds);
    const inferenceMs = performance.now() - inferenceStart;
    const output = outputs.logits;
    if (output.type !== 'float32' || output.dims.length !== 2 || output.dims[0] !== input.options.length || output.dims[1] !== 1) {
      throw new Error('Expected FP32 logits [options,1]');
    }
    const logits = Array.from(output.data as Float32Array);
    if (!logits.every(Number.isFinite)) throw new Error('Non-finite model logits');
    const maximum = Math.max(...logits);
    const exps = logits.map(value => Math.exp(value - maximum));
    const sum = exps.reduce((a, b) => a + b, 0);
    return {
      prediction: { schema_version: '0.1', id: input.id, probabilities: input.options.map((option, i) => ({
        option_id: option.id, probability: exps[i] / sum,
      })) },
      diagnostics: { backend: 'wasm', tokenization, logits, inferenceMs, tokenizerMs,
        totalMs: performance.now() - start, requests: requests() },
    };
  } finally {
    for (const tensor of Object.values(outputs ?? {})) tensor.dispose();
    for (const tensor of Object.values(feeds)) tensor.dispose();
  }
}

let queue = Promise.resolve();
scope.onmessage = ({ data }: MessageEvent<WorkerRequest>) => {
  queue = queue.then(async () => {
    try {
      let value: Metadata | Result | null = null;
      if (data.kind === 'init') value = await initialize(data.assetBaseUrl);
      else if (data.kind === 'predict') value = await predict(data.input);
      else if (data.kind === 'dispose') {
        try { await session?.release(); } finally { session = undefined; tokenizer = undefined; }
      } else throw new Error('Unknown engine message');
      send({ kind: 'result', id: data.id, value });
    } catch (error) {
      try { await session?.release(); } catch { /* client termination is the final cleanup bound */ }
      session = undefined;
      tokenizer = undefined;
      send({ kind: 'error', id: data.id, message: error instanceof Error ? error.message : String(error) });
    }
  });
};
