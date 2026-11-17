"""Publish only the standard public calendar filenames, never personal calendars."""

import argparse
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from .files import atomic_write

PUBLIC_FILENAME = re.compile(
    r'(?:index\.json|\.build-state\.json|update-status\.json|viet_lunar(?:_en)?_'
    r'(?:latest\.ics|\d{4}(?:_\d{4})?\.ics|yearly_\d{4}_\d{4}\.zip))'
)


def public_paths(root):
    root = Path(root)
    tracked = subprocess.run(
        ['git', 'ls-files', '-z', '--', 'output/'], cwd=root,
        check=True, capture_output=True,
    ).stdout.decode('utf-8').split('\0')
    candidates = {Path(name).name for name in tracked if name}
    output = root / 'output'
    if output.is_symlink():
        raise ValueError('Public output directory must not be a symlink')
    if output.exists():
        candidates.update(path.name for path in output.iterdir())
    index = output / 'index.json'
    if index.is_symlink():
        raise ValueError('Public inventory must not be a symlink')
    if index.is_file():
        inventory = json.loads(index.read_text(encoding='utf-8'))
        expected = {'viet_lunar_latest.ics', 'viet_lunar_en_latest.ics'}
        if (not isinstance(inventory, list) or len(inventory) != 2
                or any(not isinstance(entry, dict) or not isinstance(entry.get('file'), str)
                       for entry in inventory)
                or {entry.get('file') for entry in inventory} != expected):
            raise ValueError('Only the two standard public feeds may be published; keep custom feeds local')
    paths = []
    for name in sorted(candidates):
        if not PUBLIC_FILENAME.fullmatch(name):
            continue
        path = output / name
        if path.is_symlink() or (path.exists() and not path.is_file()):
            raise ValueError('Public exports must be regular files')
        paths.append('output/' + name)
    return paths


def stage_public_outputs(root):
    paths = public_paths(root)
    if paths:
        subprocess.run(['git', 'add', '--', *paths], cwd=root, check=True)


def record_refresh(root):
    raw = json.dumps({
        'updated_at': datetime.now(timezone.utc).isoformat(timespec='seconds'),
        'languages': ['vi', 'en'],
    }, indent=2) + '\n'
    atomic_write(Path(root) / 'output/update-status.json', raw.encode('utf-8'))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--stage', action='store_true')
    group.add_argument('--record', action='store_true')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    if args.stage:
        stage_public_outputs(root)
    else:
        record_refresh(root)


if __name__ == '__main__':
    main()
