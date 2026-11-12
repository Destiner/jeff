import configuration from '../model-config.json';
export const modelLabel = configuration.label;
export const model = {
  assetBaseUrl: configuration.assetBaseUrl,
  ortBaseUrl: configuration.ortBaseUrl,
  expectedModelId: configuration.expectedModelId,
};
