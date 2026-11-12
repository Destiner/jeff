import type { ModelDescriptor } from './types.js';

export function localDirectory(value: string, origin: string, base: string): URL {
  if (typeof value !== 'string' || !value) throw new Error('Asset directory URL is required');
  const url = new URL(value, base);
  if (url.origin !== origin || !['http:', 'https:'].includes(url.protocol) ||
      url.username || url.password || url.search || url.hash || !url.pathname.endsWith('/')) {
    throw new Error('Assets require same-origin HTTP(S) directory URLs ending in /, without credentials, query or hash');
  }
  return url;
}

export function validateDescriptor(value: unknown, expectedId?: string): ModelDescriptor {
  const object = (x: unknown): x is Record<string, unknown> => !!x && typeof x === 'object' && !Array.isArray(x);
  const text = (x: unknown) => typeof x === 'string' && x.trim().length > 0;
  const sha = (x: unknown) => typeof x === 'string' && /^[0-9a-f]{64}$/.test(x);
  if (!object(value) || value.schema_version !== 'jeff.browser-encoder.v1' ||
      !text(value.id) || !text(value.label) || !sha(value.checkpoint_sha256) ||
      value.format !== 'state-question-candidate-v1' || value.precision !== 'fp32' ||
      value.max_pair_tokens !== 256 || value.scoring !== 'softmax-t1' || !object(value.files)) {
    throw new Error('Unsupported model.json: require the compatible FP32 scalar encoder contract');
  }
  const names = ['model.onnx', 'tokenizer.json', 'tokenizer_config.json'];
  if (Object.keys(value.files).length !== names.length || names.some(name => {
    const pin = (value.files as Record<string, unknown>)[name];
    return !object(pin) || !Number.isSafeInteger(pin.bytes) || (pin.bytes as number) <= 0 || !sha(pin.sha256);
  })) throw new Error('model.json must pin exactly the model and two tokenizer assets');
  if (expectedId !== undefined && value.id !== expectedId) throw new Error('Selected model identity differs from expectedModelId');
  return value as ModelDescriptor;
}
