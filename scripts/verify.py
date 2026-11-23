#!/usr/bin/env python3
"""Check the template's tracked Markdown links and Issue template metadata."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
FILES = [ROOT / 'README.md', ROOT / 'AGENTS.md', ROOT / 'docs/planning-template.md']
FILES += sorted((ROOT / '.github').rglob('*.md'))
errors = []
for path in FILES:
    if not path.is_file():
        errors.append(f'{path.relative_to(ROOT)}: file missing')
        continue
    content = path.read_text(encoding='utf-8')
    for target in re.findall(r'\]\(([^)]+)\)', content):
        if re.match(r'^(?:[a-z][a-z0-9+.-]*:|#)', target, re.I):
            continue
        target = target.split('#', 1)[0]
        if target and not (path.parent / target).exists():
            errors.append(f'{path.relative_to(ROOT)}: missing link {target}')

for path in sorted((ROOT / '.github/ISSUE_TEMPLATE').glob('*.md')):
    content = path.read_text(encoding='utf-8')
    parts = content.split('---\n', 2)
    if len(parts) != 3 or parts[0]:
        errors.append(f'{path.relative_to(ROOT)}: invalid front matter')
        continue
    for field in ('name', 'about', 'title', 'labels', 'assignees'):
        if not re.search(rf'^{field}:', parts[1], re.M):
            errors.append(f'{path.relative_to(ROOT)}: missing {field}')
    for heading in ('目的', '受け入れ条件', 'スコープ外', '依存Issue'):
        if f'## {heading}' not in parts[2]:
            errors.append(f'{path.relative_to(ROOT)}: missing {heading}')

if errors:
    print('\n'.join(errors), file=sys.stderr)
    sys.exit(1)
print(f'OK: {len(FILES)} Markdown files and Issue templates checked')
