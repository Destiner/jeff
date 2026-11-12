import type { Decision, Prediction, Progress, RequestRecord } from '../types';
export type QwenProgress = Progress & { asset?: string; loadedBytes?: number; totalBytes?: number | null };
export type DeviceMetadata = {
  features: string[]; limits: { maxBufferSize: number; maxStorageBufferBindingSize: number };
  info: Record<string, string>; browserMemoryBytes: null;
};
export type QwenMetadata = {
  backend: 'webgpu'; workerBackend: 'webgpu'; initializationMs: number; modelLoadMs: number;
  tokenizerLoadMs: number; versions: { transformers: string; onnxruntime: string; browser: string };
  adapter: DeviceMetadata; device: DeviceMetadata; requests: RequestRecord[];
  checkpointManifestSha256: string; weightsSha256: string; modelBytes: number; modelSha256: string;
  modelIdentityMethod: string;
};
export type QwenResult = {
  prediction: Prediction;
  diagnostics: {
    backend: 'webgpu'; renderedPrompt: string; promptTokenIds: number[]; answerTokenIds: number[];
    logits: number[]; selectedLogits: number[]; k: number;
    optionMapping: { letter: string; tokenId: number; optionId: string; text: string }[];
    topOptionId: string; tiedOptionIds: string[]; tokenizerMs: number; inferenceMs: number; totalMs: number;
    requests: RequestRecord[]; device: DeviceMetadata;
    observedGpuKernelsCumulative: Record<string, number>; placementQualification: string;
  };
};
export type Request = { id: number } & (
  { kind: 'init'; assetBaseUrl: string } | { kind: 'predict'; input: Decision } | { kind: 'dispose' }
);
export type Reply = { kind: 'progress'; event: QwenProgress } |
  { kind: 'result'; id: number; value: QwenMetadata | QwenResult | null } |
  { kind: 'error'; id: number; message: string };
export function requireValue(condition: unknown, message: string): asserts condition {
  if (!condition) throw new Error(message);
}
