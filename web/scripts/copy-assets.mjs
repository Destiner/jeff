import { constants, createWriteStream } from 'node:fs';
import { lstat, mkdir, open, writeFile } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import path from 'node:path';
import { Transform } from 'node:stream';
import { pipeline } from 'node:stream/promises';
import { fileURLToPath } from 'node:url';

const web = fileURLToPath(new URL('../', import.meta.url));
const publicRoot = path.join(web, 'public');
const inputHash = '26015911424707f5c9194201d0d9ad3342e0af71399ceefe9e9a4924491e3437';
const cases = [
  ['data:pilot-v1:intent:g01:r01', 3],
  ['data:pilot-v1:sentiment-r2:g01:r01', 4],
  ['data:pilot-v1:rule_application:g01:r01', 4],
];

function options() {
  const args = process.argv.slice(2);
  const result = {};
  for (let i = 0; i < args.length; i += 2) {
    const flag = args[i];
    const value = args[i + 1];
    if (!['--model-dir', '--inputs'].includes(flag) || result[flag] || !value || !path.isAbsolute(value)) {
      throw new Error('Usage: bun scripts/copy-assets.mjs --model-dir ABSOLUTE_NEW_EXPORT_ROOT --inputs ABSOLUTE_ORIGINAL_P11_INPUTS_JSONL');
    }
    result[flag] = path.resolve(value);
  }
  if (!result['--model-dir'] || !result['--inputs']) throw new Error('Both --model-dir and --inputs are required');
  return result;
}

// Inspect every existing component, not just the leaf: a symlinked output root
// would otherwise allow exclusive writes outside this package.
async function inspectPath(filename, allowMissing = false) {
  const absolute = path.resolve(filename);
  let current = path.parse(absolute).root;
  const parts = absolute.slice(current.length).split(path.sep).filter(Boolean);
  let stat;
  for (let i = 0; i < parts.length; i++) {
    current = path.join(current, parts[i]);
    try { stat = await lstat(current); } catch (error) {
      if (allowMissing && error.code === 'ENOENT') return null;
      throw error;
    }
    if (stat.isSymbolicLink()) throw new Error(`Symlink not allowed: ${current}`);
    if (i < parts.length - 1 && !stat.isDirectory()) throw new Error(`Not a directory: ${current}`);
  }
  return stat;
}

async function digest(handle) {
  const hash = createHash('sha256');
  for await (const chunk of handle.createReadStream({ start: 0, autoClose: false })) hash.update(chunk);
  return hash.digest('hex');
}

function validateInputs(buffer) {
  const lines = buffer.toString('utf8').trimEnd().split('\n');
  if (lines.length !== cases.length) throw new Error('P11 must contain exactly three decisions');
  const exactKeys = (value, keys) => value && typeof value === 'object' && !Array.isArray(value)
    && Object.keys(value).length === keys.length && keys.every(key => Object.hasOwn(value, key));
  for (const [i, line] of lines.entries()) {
    const row = JSON.parse(line);
    const [id, count] = cases[i];
    if (!exactKeys(row, ['schema_version', 'id', 'state', 'question', 'options'])
      || row.schema_version !== '0.1' || row.id !== id || typeof row.state !== 'string'
      || typeof row.question !== 'string' || !row.question.trim()
      || !Array.isArray(row.options) || row.options.length !== count) {
      throw new Error(`Invalid input-only P11 decision ${i + 1}`);
    }
    const ids = new Set();
    for (const option of row.options) {
      if (!exactKeys(option, ['id', 'text']) || typeof option.id !== 'string' || !option.id.trim()
        || typeof option.text !== 'string' || !option.text.trim() || ids.has(option.id)) {
        throw new Error(`Invalid P11 option in decision ${i + 1}`);
      }
      ids.add(option.id);
    }
  }
}

async function main() {
  const args = options();
  const modelRoot = args['--model-dir'];
  if (!(await inspectPath(modelRoot)).isDirectory()) throw new Error('Model export root must be a real directory');
  const modelNames = ['model.onnx', 'tokenizer.json', 'tokenizer_config.json', 'special_tokens_map.json', 'vocab.txt', 'config.json'];
  const ortRoot = path.join(web, 'node_modules', 'onnxruntime-web', 'dist');
  const entries = [
    ...modelNames.map(name => ({ source: path.join(modelRoot, name), url: `/models/m9/${name}` })),
    ...['ort-wasm-simd-threaded.wasm', 'ort-wasm-simd-threaded.mjs'].map(name => ({ source: path.join(ortRoot, name), url: `/ort/${name}` })),
    { source: args['--inputs'], url: '/examples/p11-train.jsonl' },
  ];
  const manifestPath = path.join(publicRoot, 'asset-manifest.json');
  try {
    // All source/type/hash and destination checks precede the first write.
    for (const entry of entries) {
      const stat = await inspectPath(entry.source);
      if (!stat.isFile() || stat.size === 0) throw new Error(`Expected nonempty regular file: ${entry.source}`);
      entry.handle = await open(entry.source, constants.O_RDONLY | constants.O_NOFOLLOW | constants.O_NONBLOCK);
      const opened = await entry.handle.stat();
      if (!opened.isFile() || opened.dev !== stat.dev || opened.ino !== stat.ino) throw new Error(`Source changed: ${entry.source}`);
      entry.bytes = opened.size;
      entry.sha256 = await digest(entry.handle);
      entry.destination = path.join(publicRoot, entry.url.slice(1));
    }
    const inputs = entries.at(-1);
    if (inputs.sha256 !== inputHash) throw new Error('P11 inputs SHA-256 does not match the frozen original');
    // Read only the explicit, hash-bound input file, never labels or references.
    const chunks = [];
    for await (const chunk of inputs.handle.createReadStream({ start: 0, autoClose: false })) chunks.push(chunk);
    const inputBuffer = Buffer.concat(chunks);
    if (createHash('sha256').update(inputBuffer).digest('hex') !== inputHash) throw new Error('P11 inputs changed during validation');
    validateInputs(inputBuffer);
    for (const destination of [...entries.map(entry => entry.destination), manifestPath]) {
      if (await inspectPath(destination, true)) throw new Error(`Destination already exists: ${destination}`);
    }
    for (const directory of new Set(entries.map(entry => path.dirname(entry.destination)))) {
      await inspectPath(directory, true);
      await mkdir(directory, { recursive: true });
      if (!(await inspectPath(directory)).isDirectory()) throw new Error(`Invalid output directory: ${directory}`);
    }
    for (const entry of entries) {
      await inspectPath(path.dirname(entry.destination));
      const hash = createHash('sha256');
      let bytes = 0;
      const meter = new Transform({
        transform(chunk, encoding, callback) {
          bytes += chunk.length;
          hash.update(chunk);
          callback(null, chunk);
        },
      });
      await pipeline(entry.handle.createReadStream({ start: 0, autoClose: false }), meter,
        createWriteStream(entry.destination, { flags: 'wx', mode: 0o644 }));
      if (bytes !== entry.bytes || hash.digest('hex') !== entry.sha256) throw new Error(`Source changed while copying: ${entry.source}`);
    }
    const copiedAt = new Date().toISOString();
    await inspectPath(publicRoot);
    const manifest = {
      schema_version: '0.1', copied_at: copiedAt,
      assets: entries.map(({ source, url, bytes, sha256 }) => ({ source, url, bytes, sha256, copied_at: copiedAt })),
    };
    await writeFile(manifestPath, `${JSON.stringify(manifest, null, 2)}\n`, { flag: 'wx', mode: 0o644 });
    console.log(JSON.stringify({ manifest: manifestPath, assets: entries.length, bytes: entries.reduce((sum, entry) => sum + entry.bytes, 0) }));
  } finally {
    await Promise.all(entries.map(entry => entry.handle?.close().catch(() => {})));
  }
}

main().catch(error => {
  // Preserve partial outputs as evidence. A retry requires a fresh destination,
  // or explicit operator cleanup; never silently replace an earlier copy.
  console.error(`Asset copy failed: ${error.message}`);
  process.exitCode = 1;
});
