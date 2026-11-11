#!/usr/bin/env python3
"""Resolve historical paths or verify this actual review artifact collection."""

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / 'review'


def digest(path):
    result = hashlib.sha256()
    with path.open('rb') as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b''):
            result.update(chunk)
    return result.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('original_path', nargs='?')
    group.add_argument('--verify', action='store_true')
    group.add_argument('--list', dest='prefix')
    parser.add_argument('--limit', type=int, default=40)
    args = parser.parse_args()
    manifest = json.loads((REVIEW / 'manifest.json').read_text())
    items = manifest['items']

    if args.verify:
        failures = []
        for item in items:
            path = ROOT / item['path']
            if not path.is_file() or path.is_symlink() or not path.resolve().is_relative_to(REVIEW / 'evidence'):
                failures.append({'path': item['path'], 'reason': 'missing/nonregular/redirected'})
            elif path.stat().st_size != item['bytes'] or digest(path) != item['sha256']:
                failures.append({'path': item['path'], 'reason': 'size/hash mismatch'})
        expected = {item['path'] for item in items}
        actual = {str(path.relative_to(ROOT)) for path in (REVIEW / 'evidence').rglob('*') if path.is_file()}
        failures.extend({'path': path, 'reason': 'unmanifested'} for path in sorted(actual - expected))
        print(json.dumps({'code_commit': manifest['code_commit'], 'cutoff_utc': manifest['cutoff_utc'], 'checked_files': len(items), 'checked_bytes': sum(i['bytes'] for i in items), 'ok': not failures, 'failures': failures}, indent=2))
        return 1 if failures else 0

    if args.prefix is not None:
        matches = [item for item in items if item['source_path'].startswith(args.prefix) or item['path'].startswith(args.prefix)]
        for item in matches[:max(0, args.limit)]:
            print(f"{item['source_path']} -> {item['path']}")
        print(f'{len(matches)} matching artifacts; displayed at most {max(0, args.limit)}.')
        return 0

    value = args.original_path.replace('\\', '/')
    if '..' in Path(value).parts:
        parser.error('Parent traversal is not a historical artifact reference.')
    original_root = manifest['original_repository'].rstrip('/') + '/'
    normalized = value[len(original_root):] if value.startswith(original_root) else value.removeprefix('./')
    if '/artifacts/' in normalized:
        normalized = 'artifacts/' + normalized.split('/artifacts/', 1)[1]
    candidates = {value, normalized, 'artifacts/' + normalized}
    matches = [item for item in items if candidates.intersection({item['source_path'], item['original_absolute_path'], item['path']})]
    if matches:
        for item in matches:
            print(ROOT / item['path'])
        return 0
    if not Path(normalized).is_absolute():
        candidate = ROOT / normalized
        if candidate.is_file() and not candidate.is_symlink() and candidate.resolve().is_relative_to(ROOT):
            print(candidate)
            return 0
    print('Not included. Inspect manifest omissions/evidence-map.md; do not recover excluded assets or sealed final data.')
    return 2


if __name__ == '__main__':
    raise SystemExit(main())
