#!/usr/bin/env python3
"""Package the sealed current static release without rebuilding reviewed assets."""
from pathlib import Path, PurePosixPath
import argparse
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'dist'
ALLOWED_CONTEXTS = {'production', 'deploy-preview', 'branch-deploy'}
PUBLIC_DIRS = {'assets', 'about', 'contact', 'explore', 'market-notes', 'mobile',
               'policies', 'research', 'services', 'signal-studio', 'work'}
PUBLIC_ROOT_FILES = {'index.html', 'robots.txt', 'sitemap.xml', 'mashcore-profile.jpg',
                     'favicon.ico', 'favicon.png'}
DENIED_ROOTS = {'.git', '.github', '.netlify', '.codex', '.agents', '.impeccable',
                'docs', 'scripts', 'qa', 'experiments', 'preview', 'content', 'upload',
                'node_modules', 'project_sources', 'source-media', 'source', 'releases',
                'baseline', 'evidence', 'review', 'handoff_private', 'private_refs'}
DENIED_EXTS = {'.py', '.md', '.zip', '.env', '.map', '.pem', '.key', '.crt', '.log',
               '.bak', '.db', '.sqlite', '.sql', '.ps1', '.cmd', '.bat'}
PRODUCTION_HEADERS = (
    '/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n'
    '/mobile/*\n  X-Robots-Tag: noindex, follow\n'
    '/research/method/*\n  X-Robots-Tag: noindex, follow\n'
)
PREVIEW_HEADERS = (
    '/*\n  X-Robots-Tag: noindex, nofollow\n  X-Content-Type-Options: nosniff\n'
    '  Referrer-Policy: strict-origin-when-cross-origin\n'
)
PREVIEW_SITEMAP = ('<?xml version="1.0" encoding="UTF-8"?>\n'
                   '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"></urlset>\n')


def manifest():
    paths = [line.strip() for line in (ROOT / 'scripts/public_manifest.txt').read_text(
        encoding='utf8').splitlines() if line.strip()]
    if not paths or len(paths) != len(set(paths)):
        raise ValueError('Empty or duplicate public manifest')
    if paths != sorted(paths):
        raise ValueError('Public manifest must be sorted for a reviewable release')
    for path in paths:
        p = PurePosixPath(path)
        if (p.is_absolute() or '..' in p.parts or p.as_posix() != path
                or any(x in path for x in ('\\', ':', '\x00', '?', '#'))
                or any(x in DENIED_ROOTS or x.startswith('.') for x in p.parts)
                or p.suffix.lower() in DENIED_EXTS
                or (len(p.parts) == 1 and path not in PUBLIC_ROOT_FILES)
                or (len(p.parts) > 1 and p.parts[0] not in PUBLIC_DIRS)):
            raise ValueError(f'Private/unsafe file in public manifest: {path}')
        src = ROOT.joinpath(*p.parts)
        if not src.is_file() or not src.resolve().is_relative_to(ROOT.resolve()):
            raise ValueError(f'Public file missing or outside repository: {path}')
        if src.is_symlink() or any(x.is_symlink() for x in src.parents if x != ROOT.parent):
            raise ValueError(f'Symlink in public file: {path}')
    return paths


def output_bytes(path, context):
    """Deterministic context transform shared by packaging and the content lock."""
    if context not in ALLOWED_CONTEXTS:
        raise ValueError('Invalid deploy context')
    if path == '_headers':
        return (PRODUCTION_HEADERS if context == 'production' else PREVIEW_HEADERS).encode('utf8')
    data = (ROOT / path).read_bytes()
    if context == 'production':
        return data
    if path == 'sitemap.xml':
        return PREVIEW_SITEMAP.encode('utf8')
    if path == 'robots.txt':
        return b'User-agent: *\nAllow: /\n'
    if path.endswith('.html'):
        text = data.decode('utf8')
        text = re.sub(r'<meta\b[^>]*\bname\s*=\s*["\']robots["\'][^>]*>', '', text, flags=re.I)
        if text.count('</head>') != 1:
            raise ValueError(f'Expected one HTML head: {path}')
        return text.replace('</head>', '<meta name="robots" content="noindex,nofollow"></head>', 1).encode('utf8')
    return data


def validate_output_target():
    """Resolve and verify the exact dedicated target before recursive deletion."""
    root = ROOT.resolve(strict=True)
    expected = root / 'dist'
    resolved = OUT.resolve(strict=False)
    if OUT.is_symlink() or resolved != expected or resolved.parent != root:
        raise ValueError('Refusing to regenerate anything except this repository/dist')
    if not resolved.is_relative_to(root) or resolved == root:
        raise ValueError('Output target escapes the release repository')
    if OUT.exists() and not OUT.is_dir():
        raise ValueError('dist must be a directory')
    return resolved


def prepare(context):
    if context not in ALLOWED_CONTEXTS:
        raise ValueError('Invalid deploy context')
    paths = manifest()
    # A missing/stale lock cannot be silently resealed by CI or by a deploy build.
    from release_lock import validate_source_lock, validate_output_lock
    lock = validate_source_lock(paths)
    destination = validate_output_target()
    if destination.exists():
        shutil.rmtree(destination)
    destination.mkdir()
    for path in paths + ['_headers']:
        target = destination / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(output_bytes(path, context))
    validate_output_lock(context, lock)
    print(f'Prepared sealed current release: context={context}, files={len(paths)}, HTML={sum(x.endswith(".html") for x in paths)}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--context', required=True, choices=sorted(ALLOWED_CONTEXTS))
    args = parser.parse_args()
    try:
        prepare(args.context)
    except Exception as error:
        print('ERROR:', error, file=sys.stderr)
        sys.exit(1)
