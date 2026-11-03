#!/usr/bin/env python3
"""Append exactly the R3.5 experiment to an already verified Deploy Preview.

Never called in production or branch-deploy. No edits to original release code.
"""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'experiments/sense-r35'
OUT = ROOT / 'dist'
FILES = ('index.html', 'styles.css', 'app.js', 'fonts/gowun-batang.woff2', 'fonts/OFL.txt')

class Links(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.links, self.ids = [], []
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs: self.ids.append(attrs['id'])
        for key in ('href', 'src', 'poster', 'data-src'):
            if attrs.get(key): self.links.append(attrs[key])

def prepare(context):
    if context != 'deploy-preview':
        raise ValueError('R3.5 is exclusively a Deploy Preview experiment')
    assert (OUT / '_headers').is_file(), 'Run original Deploy Preview packaging first'
    assert 'X-Robots-Tag: noindex' in (OUT / '_headers').read_text()
    route = OUT / 'sense-r35'
    assert not route.exists(), 'Build output must be freshly generated'
    for name in FILES:
        src = SOURCE / name
        assert src.is_file() and src.stat().st_size, f'Missing R3.5 file: {name}'
        assert not any(p.is_symlink() for p in (src, *src.parents)), 'No symlinks allowed'
        dst = route / name
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
    page = route / 'index.html'
    sha = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    text = page.read_text(encoding='utf-8')
    assert '<meta name="robots" content="noindex,nofollow">' in text
    text = text.replace('</head>', f'<meta name="r35-commit" content="{sha}"></head>')
    page.write_text(text, encoding='utf-8')
    scan = Links(text)
    assert len(scan.ids) == len(set(scan.ids)), 'Duplicate experiment IDs'
    for ref in scan.links:
        url = urlsplit(ref)
        if url.scheme or url.netloc: continue
        target = OUT / unquote(url.path).lstrip('/') if url.path.startswith('/') else route / unquote(url.path)
        if not url.path: target = page
        target = target.resolve()
        assert target.is_relative_to(OUT.resolve())
        if target.is_dir(): target = target / 'index.html'
        assert target.is_file(), f'Broken R3.5 link: {ref}'
        if url.fragment and target.suffix == '.html':
            assert url.fragment in Links(target.read_text(encoding='utf-8')).ids, ref
    assert set(p.relative_to(route).as_posix() for p in route.rglob('*') if p.is_file()) == set(FILES)
    print(json.dumps({'result':'PASS','route':'/sense-r35/','files':len(FILES),'commit':sha}))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--context', required=True)
    prepare(parser.parse_args().context)
