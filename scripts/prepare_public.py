#!/usr/bin/env python3
"""Reproducible, allowlisted A20 static release. No app secrets, server or API."""
from pathlib import Path,PurePosixPath
import argparse, shutil, sys

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'dist'
ALLOWED_CONTEXTS={'production','deploy-preview','branch-deploy'}
DENIED_ROOTS={'.git','.github','docs','scripts','qa','experiments','preview','content','upload','node_modules','project_sources'}
DENIED_EXTS={'.py','.md','.zip','.env','.map','.pem','.key'}


def manifest():
    m=ROOT/'scripts/public_manifest.txt'
    paths=[line.strip() for line in m.read_text(encoding='utf8').splitlines() if line.strip()]
    if not paths or len(set(paths))!=len(paths):raise ValueError('Empty or duplicate public manifest')
    for path in paths:
        p=PurePosixPath(path)
        if p.is_absolute() or '..' in p.parts or p.parts[0] in DENIED_ROOTS or p.suffix in DENIED_EXTS or any(x.startswith('.') for x in p.parts):
            raise ValueError(f'Private/unsafe file in public manifest: {path}')
        src=ROOT.joinpath(*p.parts)
        if not src.is_file():raise ValueError(f'Public file missing: {path}')
        if src.is_symlink() or any(x.is_symlink() for x in src.parents if x!=ROOT.parent):
            raise ValueError(f'Symlink in public file: {path}')
    return paths


def prepare(context):
    if context not in ALLOWED_CONTEXTS:raise ValueError('Invalid deploy context')
    if OUT.is_symlink():raise ValueError('dist may not be symlink')
    paths=manifest()
    if OUT.exists():shutil.rmtree(OUT)
    OUT.mkdir()
    for path in paths:
        src=ROOT/path; dst=OUT/path
        dst.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(src,dst)
    # Netlify's deploy-preview output must be excluded from search indexing.
    # The production source is already indexable except /mobile and /research/method.
    if context=='production':
        header=(
            '/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n'
            '/mobile/*\n  X-Robots-Tag: noindex, follow\n'
            '/research/method/*\n  X-Robots-Tag: noindex, follow\n')
    else:
        (OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n'
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"></urlset>\n',encoding='utf8')
        (OUT/'robots.txt').write_text('User-agent: *\nAllow: /\n',encoding='utf8')
        header='/*\n  X-Robots-Tag: noindex, nofollow\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n'
        for p in OUT.rglob('*.html'):
            s=p.read_text(encoding='utf8')
            import re
            s=re.sub(r'<meta\b[^>]*\bname\s*=\s*["\']robots["\'][^>]*>','',s,flags=re.I)
            s=s.replace('</head>','<meta name="robots" content="noindex,nofollow"></head>',1)
            p.write_text(s,encoding='utf8')
    (OUT/'_headers').write_text(header,encoding='utf8')
    print(f'Prepared A20 public release: context={context}, files={len(paths)}, HTML={sum(x.endswith(".html") for x in paths)}')

if __name__=='__main__':
    pa=argparse.ArgumentParser();pa.add_argument('--context',required=True,choices=sorted(ALLOWED_CONTEXTS));args=pa.parse_args()
    try:prepare(args.context)
    except Exception as ex:print('ERROR:',ex,file=sys.stderr);sys.exit(1)
