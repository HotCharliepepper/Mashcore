"""Render the shared public business details into HTML, including the no-JS view."""
from pathlib import Path
import html
import json
import re

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

config = (ROOT / 'assets/js/site-config.js').read_text()
match = re.search(r'Object\.freeze\((\{.*?\})\)\s*;', config, re.S)
if not match:
    raise SystemExit('Business configuration must be a JSON object inside Object.freeze().')
business = json.loads(match.group(1))
labels = {'companyName': '상호', 'representative': '대표자', 'registrationNumber': '사업자등록번호', 'address': '사업장 주소', 'phone': '전화'}
rows = []
for key, label in labels.items():
    value = business.get(key, '')
    if isinstance(value, str) and value.strip():
        rows.append(f'<div><dt>{label}</dt><dd>{html.escape(value.strip())}</dd></div>')
hidden = ' hidden=""' if not rows else ''
replacement = f'<dl class="business-info" data-business-info=""{hidden}>' + ''.join(rows) + '</dl>'
count = 0
for path in sorted(ROOT.rglob('*.html')):
    if '.git' in path.parts:
        continue
    original = path.read_text()
    content, matches = re.subn(r'<dl\b[^>]*\bdata-business-info\b[^>]*>.*?</dl>', lambda _: replacement, original, flags=re.S)
    if matches:
        if original != content:
            path.write_text(content)
        count += 1
print(f'Synchronized public business details across {count} HTML pages.')
