"""Regenerate the explicit mobile edition from the shared landing content."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / 'index.html').read_text(encoding='utf-8')
# R3.1 uses the same responsive layout on both URLs; legacy pages retain their fixed mobile viewer.
source = source.replace('class="landing-page"', 'class="landing-page mobile-edition"')
source = source.replace('<title>Mashcore —', '<title>Mashcore 모바일 —')
# Shared root canonical intentionally avoids competing copies in search.
destination = ROOT / 'mobile' / 'index.html'
destination.parent.mkdir(exist_ok=True)
destination.write_text(source, encoding='utf-8')
print('Updated mobile/index.html from the shared landing source.')
