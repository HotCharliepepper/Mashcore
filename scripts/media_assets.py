"""Validate the exact review media copied into the public artifact."""
import hashlib
import json
from pathlib import Path, PurePosixPath


def verify_media(root: Path, output: Path) -> None:
    source=root/'source-media'
    manifest=json.loads((source/'manifest.json').read_text())
    for entry in manifest['files']:
        path=PurePosixPath(entry['output'])
        if path.is_absolute() or '..' in path.parts or path.parts[:2]!=('assets','media') or path.suffix not in ('.webp','.mp4','.png'):
            raise ValueError('Unsafe media output path')
        data=(output/str(path)).read_bytes()
        if len(data)!=entry['bytes'] or hashlib.sha256(data).hexdigest()!=entry['sha256']:
            raise ValueError('Media checksum mismatch: '+str(path))
