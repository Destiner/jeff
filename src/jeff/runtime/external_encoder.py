"""E13 validation-only retained encoder child; external supervision is required."""

import argparse
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import resource
import sys
import time

PROJECT = Path('/Users/destiner/Code/jeff')
ROOT = Path(__file__).absolute().parents[3]
GIB = 1024 ** 3
HELPER = PROJECT / 'artifacts/release/p10-m11-20261112-01/predict.py'
HELPER_SHA = 'c5f57f0a767df16ec57ab4b2dad50616bbfe8b9f1cad43b8c9b0511897bcb3b2'
ROLES = {
    'msmarco-start': ('model/m4-v2-20261111-01/msmarco/baseline',
        'model/m4-v2-20261111-01/checkpoint-inventory.json',
        '856a300705b45ba59690e37d56acf649963578b1225a523c8e9308f9bc5e4d85'),
    'm9': ('model/m9-msmarco-duration-20261111-01/training/checkpoint',
        'release/p11-m9-20261112-01/preparation/checkpoint-plan.json',
        '3052ba633d1b8093a2d9074388268c2714bacc6dca3cccb09284345154fabee4'),
    'm11': ('model/m11-msmarco-duration30-20261112-01/training/checkpoint',
        'release/p10-m11-20261112-01/binding.json',
        'c1c0e9ca2bf368a8f6e361dddf63478cfa5556a1c69eda0c5521a8374ed85f2d'),
}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def safe(value):
    require(isinstance(value, (str, Path)), 'actual path required')
    path = Path(value)
    require(path.is_absolute() and '..' not in path.parts, 'absolute safe path required')
    require(not any(p.is_symlink() for p in (path, *path.parents)), 'symlink forbidden')
    require(not any(word in str(path).lower() for word in ('final', 'reference', 'unreleased')),
            'final/reference/unreleased path forbidden')
    return path


def fingerprint(path):
    path = safe(path)
    require(path.is_file(), 'regular file required')
    digest, size = hashlib.sha256(), 0
    with path.open('rb') as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
            size += len(chunk)
    return {'sha256': digest.hexdigest(), 'bytes': size}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--binding', required=True)
    parser.add_argument('--output-dir', required=True)
    args = parser.parse_args()
    destination = safe(args.output_dir)
    destination.mkdir(exist_ok=False)
    started = time.monotonic()
    receipt = {'status': 'incomplete', 'phase': 'pre_torch_binding',
               'attempted_batches': 0, 'completed_batches': 0, 'written_decisions': 0,
               'native_forward_attempted': 0, 'native_forward_completed': 0,
               'candidate_pairs_attempted': 0, 'candidate_pairs_completed': 0,
               'actual_truncated_pairs': 0, 'batch_calls': [], 'outputs': {},
               'controls': {'batch_decisions': 4, 'device': 'mps', 'dtype': 'float32',
                   'threads': 4, 'temperature': 1.0, 'max_length': 256, 'startup_calls': 0,
                   'scorer_truncation_setting': 'longest_first',
                   'precheck': 'same tokenizer/source _FORMAT; truncation=False; reject >256 before scorer'},
               'memory': {'rss_scope': 'macOS lifetime peak bytes',
                   'mps_scope': 'sampled driver/current; not continuous peaks', 'samples': []}}
    torch = None
    hooks = []
    active = None
    limit = 0

    def persist():
        receipt['elapsed_seconds'] = time.monotonic() - started
        with (destination / 'receipt.json').open('w', encoding='utf-8') as out:
            json.dump(receipt, out, indent=2, allow_nan=False)
            out.write('\n')
            out.flush()
            os.fsync(out.fileno())

    def guard(phase):
        receipt['phase'] = phase
        require(sys.platform == 'darwin', 'macOS required')
        require(time.monotonic() - started <= limit, 'cooperative duration exceeded')
        rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        sample = {'phase': phase, 'rss_bytes': rss}
        receipt['memory']['samples'].append(sample)
        require(rss <= 8 * GIB, 'RSS >8 GiB')
        if torch is not None:
            torch.mps.synchronize()
            driver = torch.mps.driver_allocated_memory()
            recommended = torch.mps.recommended_max_memory()
            sample.update(driver_bytes=driver, current_bytes=torch.mps.current_allocated_memory(),
                          recommended_bytes=recommended, headroom_bytes=recommended - driver)
            require(driver <= 8 * GIB, 'driver >8 GiB')
            require(recommended - driver >= 2 * GIB, 'recommended minus driver <2 GiB')

    try:
        persist()
        # Authenticate the frozen helper before importing its stdlib-only API; never call its main.
        require(fingerprint(HELPER)['sha256'] == HELPER_SHA, 'frozen helper changed')
        spec = importlib.util.spec_from_file_location('_e13_p10_helper', HELPER)
        helper = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(helper)
        decode, same = helper.decode, helper.same
        binding_path = safe(args.binding)
        receipt['binding_file'] = {'path': str(binding_path), **fingerprint(binding_path)}
        binding = decode(binding_path.read_bytes())
        receipt['binding'] = binding
        require(binding['schema_version'] == 'e13.encoder.binding.v1', 'binding schema')
        role = binding['candidate']
        require(role in ROLES, 'only msmarco-start, m9, m11')
        limit = binding['max_seconds']
        require(type(limit) in (int, float) and math.isfinite(limit) and 0 < limit <= 600,
                'actual positive max_seconds <=600 required')
        for key in ('model_activation', 'reservation', 'renewed_window_message'):
            require(isinstance(binding[key], str) and binding[key].strip(), 'actual grant context required')
        guard('pre_torch_verification')

        def reference(pin):
            require(isinstance(pin, dict) and set(pin) == {'path', 'sha256'}, 'path/sha256 required')
            actual = fingerprint(pin['path'])
            require(actual['sha256'] == pin['sha256'], 'reference bytes mismatch')
            return {'path': str(safe(pin['path'])), **actual}

        pins = binding['executable_sources']
        require(isinstance(pins, dict), 'actual executable pins required')
        origins = {'jeff': '__init__.py', 'jeff.model': 'model/__init__.py',
                   'jeff.model.predict': 'model/predict.py', 'jeff.model.scorer': 'model/scorer.py',
                   'jeff.model.cross_encoder': 'model/cross_encoder.py'}
        # Package initializers are executable dependencies too.
        package_sources = {'jeff.runtime': 'runtime/__init__.py'}
        required = {str(Path(__file__).absolute()), str(HELPER), str(ROOT / 'pyproject.toml'),
                    str(ROOT / 'uv.lock')}
        required.update(str(ROOT / 'src/jeff' / relative)
                        for relative in (*origins.values(), *package_sources.values()))
        supervisor = reference(binding['supervisor'])
        require(supervisor['path'] != str(Path(__file__).absolute()), 'separate supervisor required')
        required.add(supervisor['path'])
        require(required <= pins.keys(), 'missing executable/package/source pins')
        receipt['sources'] = {}
        for path, sha in pins.items():
            actual = fingerprint(path)
            require(actual['sha256'] == sha, 'executable source mismatch')
            receipt['sources'][path] = actual
        require(pins[str(HELPER)] == HELPER_SHA and pins[supervisor['path']] == supervisor['sha256'],
                'helper/supervisor source mismatch')
        root_name, metadata_name, metadata_sha = ROLES[role]
        root = safe(PROJECT / 'artifacts' / root_name)
        metadata_path = PROJECT / 'artifacts' / metadata_name
        receipt['checkpoint_metadata'] = reference({'path': str(metadata_path), 'sha256': metadata_sha})
        metadata = decode(metadata_path.read_bytes())
        if role == 'msmarco-start':
            entry = metadata['checkpoints']['msmarco-baseline']
            require(entry['path'] == root_name, 'original M4 root mismatch')
            expected = {item['path']: {'sha256': item['sha256'], 'bytes': item['bytes']}
                        for item in entry['files']}
            receipt['historical_inventory_timing'] = metadata['timing']
            require(expected['encoder/model.safetensors']['sha256'] ==
                    'a6e1fd85181a93a58bc33f65700f2ba34da3af2667f85cc57bcdf0f9f0092200', 'M4 weight pin')
        else:
            expected = metadata['checkpoint_files']
        require(set(expected) == helper.CHECKPOINT_FILES, 'exact seven-file metadata required')
        inventory = {}
        for path in root.rglob('*'):
            safe(path)
            if not path.is_dir():
                inventory[path.relative_to(root).as_posix()] = fingerprint(path)
                guard('pre_torch_checkpoint_hashing')
        require(same(inventory, expected), 'checkpoint exact file/hash/size mismatch')
        receipt.update(checkpoint_dir=str(root), checkpoint_files=inventory)
        manifest_ref = reference(binding['input_manifest'])
        manifest = decode(safe(manifest_ref['path']).read_bytes())
        require(set(manifest) == {'schema_version', 'candidate', 'validation_only_never_train',
                                  'release', 'pair_map', 'datasets'}, 'input manifest fields')
        require(manifest['schema_version'] == 'e13.exploration.inputs.v1' and
                manifest['candidate'] == role and manifest['validation_only_never_train'] is True,
                'validation-only role/schema mismatch')
        receipt['release'] = reference(manifest['release'])
        receipt['pair_map'] = reference(manifest['pair_map'])
        datasets = manifest['datasets']
        require(isinstance(datasets, list) and len(datasets) == 2 and
                [item['name'] for item in datasets] == ['e13-native', 'e13-reversed'], 'ordered E13 suites required')
        for item in datasets:
            require(set(item) == {'name', 'path', 'sha256', 'rows'}, 'dataset fields')
            require(type(item['rows']) is int and item['rows'] == 200, 'exactly 200 rows per orientation required')
            reference({'path': item['path'], 'sha256': item['sha256']})
        require(datasets[0]['rows'] == datasets[1]['rows'], 'orientation row counts differ')
        receipt['inputs'] = {'manifest': manifest_ref, 'content': manifest}
        guard('pre_torch_before_import')
        persist()
        os.environ.update(HF_HUB_OFFLINE='1', TRANSFORMERS_OFFLINE='1', HF_DATASETS_OFFLINE='1',
                          PYTORCH_ENABLE_MPS_FALLBACK='0', TOKENIZERS_PARALLELISM='false',
                          OMP_NUM_THREADS='4', MKL_NUM_THREADS='4')
        sys.path.insert(0, str(ROOT / 'src'))
        import torch as torch_module
        torch = torch_module
        torch.set_num_threads(4)
        require(torch.backends.mps.is_available(), 'MPS unavailable; no fallback')
        from jeff.model.scorer import load_checkpoint
        from jeff.model.predict import _rows, _write_batch
        from jeff.model import cross_encoder
        for name, relative in origins.items():
            path = ROOT / 'src/jeff' / relative
            require(safe(sys.modules[name].__file__) == path and
                    fingerprint(path)['sha256'] == pins[str(path)], 'import source mismatch')
        rows_by_suite = {}
        for item in datasets:
            rows = list(_rows(safe(item['path'])))
            require(len(rows) == item['rows'] and all(len(row['options']) == 2 for row in rows),
                    'actual row count/K2 mismatch')
            rows_by_suite[item['name']] = rows
        expected_calls = sum(math.ceil(item['rows'] / 4) for item in datasets)
        expected_decisions = sum(item['rows'] for item in datasets)
        expected_pairs = sum(len(row['options']) for rows in rows_by_suite.values() for row in rows)
        coverage = {'calls': expected_calls, 'decisions': expected_decisions, 'pairs': expected_pairs}
        require(same(binding['expected'], coverage), 'actual expected counts must be bound')
        receipt['expected'] = coverage
        guard('before_load')
        model = load_checkpoint(root, device='cpu')
        require(type(model) is cross_encoder.RetainedCrossEncoder, 'retained encoder required')
        native = model.classifier_model
        require(type(native) is cross_encoder.BertForSequenceClassification, 'native classifier required')
        guard('after_load')
        model.to('mps')
        model.eval()
        guard('after_transfer')
        parameters = {(str(p.dtype), str(p.device)) for p in model.parameters()}
        require(parameters and all(dtype == 'torch.float32' and device.startswith('mps')
                                   for dtype, device in parameters), 'FP32/MPS required')
        require(model.max_length == 256 and model.temperature == 1.0 and
                torch.get_num_threads() == 4 and not model.training, 'loaded controls mismatch')
        receipt['loaded_controls'] = {'dtype_devices': sorted(parameters), 'threads': torch.get_num_threads()}

        def before_native(module, args, kwargs):
            require(module is native and active is not None and active['precheck_complete'] and
                    not active['native_attempted'], 'unauthorized/duplicate native call')
            require(receipt['native_forward_attempted'] < expected_calls, 'native call cap')
            tokens = kwargs['input_ids']
            lengths = kwargs['attention_mask'].sum(dim=1).tolist()
            require(lengths == active['complete_pair_lengths'] and tokens.shape[1] <= 256 and
                    tokens.shape[0] == active['pairs'], 'native lengths differ from complete precheck')
            guard('before_native_forward')
            active['native_attempted'] = True
            receipt['native_forward_attempted'] += 1
            receipt['candidate_pairs_attempted'] += active['pairs']
            persist()

        def after_native(module, args, kwargs, output):
            torch.mps.synchronize()
            active['native_completed'] = True
            receipt['native_forward_completed'] += 1
            receipt['candidate_pairs_completed'] += active['pairs']
            persist()
            guard('after_native_forward')

        hooks.append(native.register_forward_pre_hook(before_native, with_kwargs=True))
        hooks.append(native.register_forward_hook(after_native, with_kwargs=True))
        with torch.inference_mode():
            for item in datasets:
                path = destination / (item['name'] + '.jsonl')
                receipt['outputs'][item['name']] = {'path': str(path), 'status': 'incomplete'}
                with path.open('x', encoding='utf-8') as output:
                    rows = rows_by_suite[item['name']]
                    for offset in range(0, len(rows), 4):
                        batch = rows[offset:offset + 4]
                        active = {'suite': item['name'], 'ids': [row['id'] for row in batch],
                                  'pairs': sum(len(row['options']) for row in batch),
                                  'precheck_complete': False, 'native_attempted': False,
                                  'native_completed': False, 'write_completed': False}
                        receipt['batch_calls'].append(active)
                        receipt['attempted_batches'] += 1
                        guard('before_complete_pair_precheck')
                        first, second = [], []
                        for row in batch:
                            for option in row['options']:
                                first.append(cross_encoder._FORMAT['first'].format(**row))
                                second.append(cross_encoder._FORMAT['second'].format(**option))
                        complete = model.tokenizer(first, second, padding=False, truncation=False,
                                                   add_special_tokens=True)
                        lengths = [len(ids) for ids in complete['input_ids']]
                        active['complete_pair_lengths'] = lengths
                        persist()
                        require(len(lengths) == active['pairs'] and all(0 < n <= 256 for n in lengths),
                                'complete pair overflow: stopped before scorer/native forward')
                        active['precheck_complete'] = True
                        persist()
                        _write_batch(model, batch, output)
                        require(active['native_attempted'] and active['native_completed'], 'missing native call')
                        output.flush()
                        os.fsync(output.fileno())
                        active['write_completed'] = True
                        receipt['completed_batches'] += 1
                        receipt['written_decisions'] += len(batch)
                        persist()
                        guard('after_batch')
                        active = None
                receipt['outputs'][item['name']]['status'] = 'complete'
        require(all(receipt[key] == expected_calls for key in ('attempted_batches', 'completed_batches',
                'native_forward_attempted', 'native_forward_completed')) and
                receipt['written_decisions'] == expected_decisions and
                receipt['candidate_pairs_attempted'] == receipt['candidate_pairs_completed'] == expected_pairs,
                'coverage mismatch')
        guard('complete')
        receipt['status'] = 'complete'
    except BaseException as error:
        receipt['status'] = 'failed'
        receipt['error'] = {'type': type(error).__name__, 'message': str(error)}
        raise
    finally:
        for hook in hooks:
            hook.remove()
        for info in receipt['outputs'].values():
            path = Path(info['path'])
            if path.exists():
                info['fingerprint'] = fingerprint(path)
                with path.open('rb') as handle:
                    info['physical_lines'] = sum(1 for _ in handle)
        receipt['partial_note'] = 'No retries/cleanup; partial physical writes and native completions are distinct.'
        receipt['supervision'] = 'Cooperative child only; external owner must enforce whole-process deadline and grant.'
        persist()


if __name__ == '__main__':
    main()
