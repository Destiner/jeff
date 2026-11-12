import { createEngine as createSdkEngine } from '@jeff/sdk';
import type { Decision, EngineOptions, Metadata, Result } from '@jeff/sdk';
export type { Decision, Prediction, Metadata, Progress, Result, RequestRecord } from '@jeff/sdk';

export type Engine = {
  metadata: Metadata;
  predict(input: Decision): Promise<Result>;
  dispose(): Promise<void>;
};

// Preserve the old host's diagnostic capture API without a second inference path.
// New consumers use @jeff/sdk directly and opt into diagnostics only when needed.
export async function createEngine(options: Omit<EngineOptions, 'ortBaseUrl'> & {
  ortBaseUrl?: string;
}): Promise<Engine> {
  const engine = await createSdkEngine({ ...options, ortBaseUrl: options.ortBaseUrl ?? '/ort/' });
  return { metadata: engine.metadata, predict: engine.predictWithDiagnostics, dispose: engine.dispose };
}
