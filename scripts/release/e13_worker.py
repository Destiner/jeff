"""One E13 candidate in one native process; launched only by e13_batch."""
import argparse
import json
from pathlib import Path
import sys
import time


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--binding', type=Path, required=True)
    p.add_argument('--output-dir', type=Path, required=True)
    a = p.parse_args()
    b = json.loads(a.binding.read_text())
    for key in ('model_activation', 'reservation', 'renewed_window_message'):
        if not isinstance(b.get(key), str) or not b[key].strip():
            raise ValueError('actual Model grant required')
    root = Path(b['source_root'])
    sys.path.insert(0, str(root / 'src'))
    if b['candidate'] == 'p12-nli':
        from jeff.runtime import nli_challenger
        sys.argv = ['nli_challenger', 'predict', '--binding', b['native_binding']['path'],
                    '--output-dir', str(a.output_dir)]
        return nli_challenger.main()
    if b['candidate'] == 'm11':
        from jeff.runtime import external_encoder
        sys.argv = ['external_encoder', '--binding', str(a.binding), '--output-dir', str(a.output_dir)]
        external_encoder.main()
        return 0
    if b['candidate'] not in ('m10', 'm12'):
        raise ValueError('late exploration four only')
    from jeff.runtime import qwen_challenger as q
    a.output_dir.mkdir(exist_ok=False)
    audit = a.output_dir / 'audit'
    run = a.output_dir / 'run'
    args = ['--config', b['config']['path'], '--inputs', b['input_manifest']['path'],
            '--model-dir', b['model_dir'], '--audit-dir', str(audit)]
    if b['checkpoint_manifest'] is not None:
        args += ['--checkpoint-manifest', b['checkpoint_manifest']['path']]
    # Existing CLI main performs audit/evidence; neither phase spawns another Python.
    sys.argv = ['qwen_challenger', 'audit', *args]
    if q.main() != 0:
        return 1
    sys.argv = ['qwen_challenger', 'predict', '--audit-dir', str(audit),
                '--model-dir', b['model_dir'], '--output-dir', str(run), '--device', 'mps']
    return q.main()


if __name__ == '__main__':
    raise SystemExit(main())
