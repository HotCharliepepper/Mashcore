"""Regenerate the explicit mobile edition from the shared landing content."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# Legacy buildless workflow: preserve its implementation, but never mutate or
# validate the generator project with a different configuration/output contract.
if (ROOT / 'scripts/build_public.py').is_file() and (ROOT / 'content/services-prototype.json').is_file():
    raise SystemExit(
        'LEGACY COMMAND BLOCKED in this generator project. '
        'Use: python3 scripts/build_public.py --context deploy-preview; '
        'python3 scripts/check_public.py. '
        'Runtime checks: node scripts/check_review_interactions.cjs; node scripts/check_spatial.cjs.'
    )

source = (ROOT / 'index.html').read_text()
source = source.replace('class="landing-page"', 'class="landing-page mobile-edition"')
source = source.replace('<title>Mashcore —', '<title>Mashcore 모바일 —')
# Shared root canonical intentionally avoids competing copies in search.
destination = ROOT / 'mobile' / 'index.html'
destination.parent.mkdir(exist_ok=True)
destination.write_text(source)
print('Updated mobile/index.html from the shared landing source.')
