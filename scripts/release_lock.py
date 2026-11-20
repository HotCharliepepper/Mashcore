#!/usr/bin/env python3
"""Content-addressed release gate. Sealing is explicit; builds only validate."""
import argparse
import hashlib
import json
import sys

from prepare_public import ROOT, OUT, ALLOWED_CONTEXTS, manifest, output_bytes

LOCK_PATH = ROOT / 'scripts/release_lock.json'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def tree_digest(files):
    canonical = json.dumps(files, sort_keys=True, separators=(',', ':'), ensure_ascii=True)
    return digest(canonical.encode('utf8'))


def source_map(paths):
    return {path: digest((ROOT / path).read_bytes()) for path in sorted(paths)}


def expected_output(paths, context):
    return {path: digest(output_bytes(path, context)) for path in sorted(paths + ['_headers'])}


def difference(actual, expected):
    return {'added': sorted(actual.keys() - expected.keys()),
            'missing': sorted(expected.keys() - actual.keys()),
            'changed': sorted(key for key in actual.keys() & expected.keys() if actual[key] != expected[key])}


def validate_source_lock(paths=None):
    paths = paths if paths is not None else manifest()
    if not LOCK_PATH.is_file():
        raise ValueError('Release is not sealed. Complete source review, then explicitly run release_lock.py --seal.')
    lock = json.loads(LOCK_PATH.read_text(encoding='utf8'))
    if lock.get('schema') != 1 or lock.get('release') != 'MASHCORE VALUE FLOW R1 / R070':
        raise ValueError('Unexpected release lock identity')
    expected = lock['source']['files']
    if tree_digest(expected) != lock['source']['tree_sha256']:
        raise ValueError('Invalid source lock digest')
    actual = source_map(paths)
    if actual != expected:
        raise ValueError('Public source changed after seal: ' + json.dumps(difference(actual, expected)))
    for context in sorted(ALLOWED_CONTEXTS):
        record = lock['contexts'][context]
        if record['tree_sha256'] != tree_digest(record['files']):
            raise ValueError('Invalid output lock digest: ' + context)
        if expected_output(paths, context) != record['files']:
            raise ValueError('Packaging behavior changed after seal: ' + context)
    return lock


def validate_output_lock(context, lock=None):
    if context not in ALLOWED_CONTEXTS:
        raise ValueError('Invalid deploy context')
    lock = lock if lock is not None else validate_source_lock()
    if OUT.is_symlink() or OUT.resolve() != ROOT.resolve() / 'dist':
        raise ValueError('Unexpected output path')
    files = [p for p in OUT.rglob('*') if p.is_file()]
    if any(p.is_symlink() or not p.resolve().is_relative_to(OUT.resolve()) for p in files):
        raise ValueError('Symlink/escaped file in output')
    actual = {p.relative_to(OUT).as_posix(): digest(p.read_bytes()) for p in files}
    expected = lock['contexts'][context]['files']
    if actual != expected:
        raise ValueError('Output differs from sealed artifact: ' + json.dumps(difference(actual, expected)))
    return lock['contexts'][context]['tree_sha256']


def seal():
    paths = manifest()
    source = source_map(paths)
    contexts = {}
    for context in sorted(ALLOWED_CONTEXTS):
        files = expected_output(paths, context)
        contexts[context] = {'tree_sha256': tree_digest(files), 'files': files}
    value = {'schema': 1, 'release': 'MASHCORE VALUE FLOW R1 / R070',
             'basis': 'Reviewed local R069 artifact; A20 static packaging contract. See docs/release-provenance.md.',
             'identity': 'Git commit binds this lock and public source; no circular commit hash is embedded in public files.',
             'source': {'tree_sha256': tree_digest(source), 'files': source}, 'contexts': contexts}
    LOCK_PATH.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n', encoding='utf8', newline='\n')
    print(json.dumps({'sealed': True, 'public_files': len(paths), 'source_tree_sha256': tree_digest(source),
                      'production_tree_sha256': contexts['production']['tree_sha256']}, ensure_ascii=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--seal', action='store_true', help='Explicitly seal reviewed source; never invoked by CI/deploy.')
    action.add_argument('--check', action='store_true', help='Validate the committed public source lock.')
    parser.add_argument('--context', choices=sorted(ALLOWED_CONTEXTS), help='Also validate the existing built dist.')
    args = parser.parse_args()
    try:
        if args.seal:
            if args.context:
                raise ValueError('--context is only valid with --check')
            seal()
        else:
            lock = validate_source_lock()
            result = {'result': 'PASS', 'source_tree_sha256': lock['source']['tree_sha256']}
            if args.context:
                result['context'] = args.context
                result['output_tree_sha256'] = validate_output_lock(args.context, lock)
            print(json.dumps(result))
    except Exception as error:
        print('RELEASE LOCK FAILED:', error, file=sys.stderr)
        sys.exit(1)
